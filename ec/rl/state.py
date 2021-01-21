from typing import Any, List, Set

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from operations import Op, Function, ValueNode, ProgramNode



class State():
    """
    The state is (1) a tree corresponding to a given ARC task and (2) a dictionary

    The tree:
        Left is input is leaf
        Right is output is root

    The dictionary:
        Maps nodes in the tree to the action that connects them
    """
    def __init__(self, start_grids, end_grids):
        """
        Initialize the DAG
        For more, see https://mungingdata.com/python/dag-directed-acyclic-graph-networkx/
        """

        self.graph = nx.DiGraph()

        assert len(start_grids) == len(end_grids)
        self.num_grid_pairs = len(start_grids) # number of training examples

        # Forward graph. Should be a DAG.
        self.graph = nx.MultiDiGraph()

        # The start and end nodes are the only program nodes that don't have an associated function
        self.start = ValueNode(start_grids)
        self.end = ValueNode(end_grids)
        self.graph.add_node(self.start)#ProgramNode(fn=None, in_values=[self.start]))
        self.graph.add_node(self.end)#ProgramNode(fn=None, in_values=[self.end]))

    def check_invariants(self):
        assert nx.algorithms.dag.is_directed_acyclic_graph(self.fgraph)
        #


    # from state_interface import add_hyperedge#, update_groundedness
    def add_hyperedge(
        self,
        in_nodes: List[ValueNode],
        out_nodes: List[ValueNode],
        fn: Function
    ):
        """
        Adds the hyperedge to the data structure.
        This can be represented underneath however is most convenient.
        This method itself could even be changed, just go change where it's called

        Each ValueNode is really just an edge (should have one input, one output)
        Each ProgramNode is a true node
        """
        p = ProgramNode(fn, in_values=in_nodes, out_values=out_nodes)
        for in_node in in_nodes:
            self.graph.add_edge(in_node,out_nodes[0],label=str(in_node.value)) # the graph infers new nodes from a collection of edges



    # # def extend_forward(self, fn: Function, inputs: List[ValueNode]):
    # def extend_forward(self, fn, inputs):
    #     assert len(fn.arg_types) == len(inputs)
    #     p = ProgramNode(fn, in_values=inputs)
    #     for inp in inputs:
    #         self.graph.add_edge(inp,p,label=str(inp.value)) # the graph infers new nodes from a collection of edges

    # # def extend_backward(self, fn: InvertibleFunction, inputs: List[ValueNode]):
    # def extend_backward(self, fn, inputs):
    #     assert len(fn.arg_types) == len(inputs)
    #     p = ProgramNode(fn, out_values=inputs)
    #     for inp in inputs:
    #         self.graph.add_edge(p, inp)


    def done(self):
        # how do we know the state is done?
        # everytime we connect a part on the left to the part on the right
        # we check that the part on the right has all its siblings completed.  if so, go up the tree one more step
        # then go up one more, and check all siblings completed.
        # if you reach the root, you're done.
        pass

    def draw(self):
        pos = nx.random_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        edge_labels = nx.get_edge_attributes(self.graph,'label')
        # nx.draw_networkx_edge_labels(self.graph,pos,edge_labels=edge_labels,font_color='red')
        plt.show()


def arcexample_old():

    import sys; sys.path.append("..") # hack to make importing bidir work
    from bidir.primitives.functions import rotate_ccw, rotate_cw
    from bidir.primitives.types import Grid

    from operations import take_forward_op

    start_grids = [np.array([[0, 0], [1, 1]])]
    end_grids = [np.array([[0, 1], [1, 0]])]
    state = State(start_grids, end_grids)

    state.draw()

    rotate_ccw_func = Function("rotateccw", rotate_ccw, [Grid], [Grid])

    state.extend_forward(rotate_ccw_func, (state.start,))

    state.draw()


def arcexample():

    import sys; sys.path.append("..") # hack to make importing bidir work
    from bidir.primitives.functions import rotate_ccw, rotate_cw
    from bidir.primitives.types import Grid

    from operations import take_forward_op

    start_grids = [
        Grid(np.array([[0, 0], [1, 1]])),
        Grid(np.array([[2, 2], [2, 2]]))
    ]
    
    end_grids = [
        Grid(np.array([[0, 1], [1, 0]])),
        Grid(np.array([[2, 2], [2, 2]]))
    ]
    state = State(start_grids, end_grids)

    # state.draw()

    # create operation
    rotate_ccw_func = Function("rotateccw", rotate_ccw, [Grid], [Grid])
    rotate_cw_func = Function("rotatecw", rotate_cw, [Grid], [Grid])
    op = Op(rotate_ccw_func, rotate_cw_func, 'forward')

    # extend in the forward direction using fn and tuple of arguments that fn takes
    take_forward_op(state, op, [state.start])   
    state.draw()


if __name__ == '__main__':

    # arcexample_old()
    arcexample()
