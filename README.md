# How to start using Dreamcoder to solve ARC

# Setup

## Clone this repo

Ideally, clone it to openmind…
```
ssh [username]@openmind7.mit.edu
cd /om2/user/[username]
git clone https://github.com/anshula/neurosymbolic-modules.git
```

...but if you don’t have access to openmind, clone it to another linux machine.  The machine probably needs to be linux in order for singularity to run on it smoothly.

## Clone the submodules of this repo

First make sure you are in the `neurosymbolic-modules` folder, then:

```
cd ec
git clone https://github.com/insperatum/pinn.git
cd pinn
git checkout 1878ef5

cd ..
git clone https://github.com/insperatum/pregex.git
cd pregex
git checkout b5eab11

cd ..
git clone https://github.com/hans/pyccg.git
cd pyccg
git checkout c465a23
```

## Add the singularity container

Download the singularity `container.img` file, and put it directly inside the `neurosymbolic modules/ec` folder.
- Quick way: copy it from Anshula’s openmind folder: `srun cp /cbcl/cbcl01/anshula/shared/container.img /om2/user/$USER/neurosymbolic-modules/ec/container.img`
- Longer way: Install it from source using the instructions here: https://github.com/ellisk42/ec

## Install singularity 

If using openmind:
- `openmind module add openmind/singularity`

If not using openmind:
- https://singularity.lbl.gov/install-linux

## Run the main file

```srun singularity exec container.img python bin/arc_simon.py```

You should see some output enumerating solved tasks.

# Editing the files

## Editing files from scratch
To learn how to solve your own tasks from scratch, follow the tutorial from https://github.com/ellisk42/ec/blob/master/docs/creating-new-domains.md

## Editing our ARC files

For more on the ARC-specific infrastructure.
- To change the _primitives_ or _tasks_ used in a given run, edit the main file: e.g. `neurosymbolic-modules/ec/bin/arc_simon.py` (or another similarly structured file)
- To change the _implementation of the primitives_ or _implementations of tasks_, edit `neurosymbolic-modules/ec/dreamcoder/domains/arc/arcPrimitives.py` and `neurosymbolic-modules/ec/dreamcoder/domains/arc/makeTasks.py`
- To change the  _implementation of the primitives_  in OCaml, edit `neurosymbolic-modules/ec/solvers/program.ml`

# Potential errors and fixes

ongoing
