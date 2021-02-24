from typing import NamedTuple, Sequence, Tuple, Callable, Set, Optional, List

import gym

from bidir.utils import SynthError
from bidir.task_utils import Task

from rl.ops.operations import Op
from rl.program_search_graph import ProgramSearchGraph


class SynthEnvAction(NamedTuple):
    op_idx: int
    arg_idxs: Tuple[int, ...]


class SynthEnvObservation(NamedTuple):
    psg: ProgramSearchGraph

    # Hidden state for debugging agents
    action_count_: int


class SynthEnv(gym.Env):
    """
    OpenAI-compatible implementation of an RL environment for solving synthesis
    tasks.
    """

    metadata = {"render.modes": ["matplotlib", "text"]}

    def __init__(
        self,
        ops: Sequence[Op],
        task: Task = None,
        task_sampler: Callable[[], Task] = None,
        max_actions=100,
        solve_reward=100,
        synth_error_penalty=-1,
        timeout_penalty=0,
    ):
        """
        Initialize the environment for given task.
        All ops are provided at the beginning as well.

        You can either provide a single task, or a task-sampling function that
        generates a task to solve for a given episode

        If max_actions=-1, then unlimited actions allowed.
        """
        # TODO: incorporate test examples
        self.ops = ops
        self.max_actions = max_actions

        self.solve_reward = solve_reward
        self.synth_error_penalty = synth_error_penalty
        self.timeout_penalty = timeout_penalty

        if task:
            assert not task_sampler, ("Provided conflicting task retrieval",
                                      "mechanisms")
            self.task_sampler = lambda: task
        else:
            assert task_sampler, "Need to provide task or task sampler"
            self.task_sampler = task_sampler

        self.synth_error_steps: Set[int] = set()

        self.reset()

    def reset(self) -> SynthEnvObservation:
        self.action_count = 0
        task = self.task_sampler()
        self.psg = ProgramSearchGraph(task)
        self.synth_error_steps = set()
        return self.observation()

    def observation(self) -> SynthEnvObservation:
        return SynthEnvObservation(
            psg=self.psg,
            action_count_=self.action_count,
        )

    def render(self, mode="text"):
        if mode == "text":
            print(f"Solved: {self.is_solved()}")
            print(f"Number of actions: {self.action_count}")
            print(f"Number of nodes: {len(self.psg.get_value_nodes())}")
        elif mode == "matplotlib":
            self.psg.draw()
        else:
            raise NotImplementedError

    def done(self) -> bool:
        if self.max_actions != -1 and self.action_count >= self.max_actions:
            return True
        return self.psg.solved()

    def episode_rewards(self) -> Optional[List[int]]:
        """
        If episode is not done, returns None.
        Otherwise, returns the reward for each action done throughout the
        episode.
        """

        if not self.done():
            return None

        rewards = [-1 if i in self.synth_error_steps else 0
                   for i in range(self.action_count)]
        if self.psg.solved():
            action_steps = self.psg.actions_in_program()
            assert action_steps is not None

            for action_step in action_steps:
                assert action_step not in self.synth_error_steps
                rewards[action_step] = self.solve_reward / len(action_steps)

        return rewards

    def is_solved(self) -> bool:
        return self.psg.solved()

    def step(
        self, action: SynthEnvAction
    ) -> Tuple[SynthEnvObservation, float, bool, dict]:
        """
        (1) Apply the action
        (2) Update environment's state

        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        reward = 0

        try:
            op = self.ops[action.op_idx]
            nodes = self.psg.get_value_nodes()
            arg_nodes = tuple(nodes[arg_idx] for arg_idx in action.arg_idxs)
            op.apply_op(self.psg, arg_nodes, self.action_count)
        except SynthError as e:
            # this covers a lot of possible errors:
            # 1. args to op's fn cause a syntax/type error
            # 2. args to forward op aren't grounded, etc.
            # 3. forward op creates a value that already exists and is
            #    grounded, etc.
            reward = self.synth_error_penalty
            self.synth_error_steps.add(self.action_count)

        if self.psg.solved():
            reward = self.solve_reward
        elif self.action_count == self.max_actions:
            reward = self.timeout_penalty

        self.action_count += 1

        return self.observation(), reward, self.done(), dict()
