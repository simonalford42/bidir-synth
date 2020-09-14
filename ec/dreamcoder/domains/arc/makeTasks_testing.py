import json
import os
import numpy as np
from numpy.random import default_rng
import random
import math

from dreamcoder.task import Task
from dreamcoder.type import arrow, tint, tlist
from dreamcoder.domains.arc.arcPrimitives import *
import dreamcoder.domains.arc.arcPrimitives as p

def make_rotation_tasks():

    # ---------------------------------------------
    # TASK that draws a line down
    # ---------------------------------------------
    
    array0_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 1, 0, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    array0_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 1, 0, 0, 0], 
                 [0, 1, 0, 0, 0],
                 [0, 1, 0, 0, 0]])
    arc0_in = Grid(array0_in)
    arc0_out = Grid(array0_out)
    should_be = p._draw_line_down(arc0_in)(p._get(p._objects(arc0_in))(0))
    assert arc0_out == should_be, 'incorrect example created'

    array1_in = np.array(
                [[0, 0, 0, 1, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    array1_out = np.array(
                [[0, 0, 0, 1, 0], 
                 [0, 0, 0, 1, 0], 
                 [0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0]])
    arc1_in = Grid(array1_in)
    arc1_out = Grid(array1_out)
    should_be = p._draw_line_down(arc1_in)(p._get(p._objects(arc1_in))(0))
    assert arc1_out == should_be, 'incorrect example created'

    examples0 = [((arc0_in,), arc0_out), ((arc1_in,), arc1_out)]
    task_drawlinedown = Task(
            "drawLineDown",
            arrow(tgrid, tgrid),
            examples0
        )

    # ---------------------------------------------
    # TASK that draws a line to the left
    # ---------------------------------------------
    
    array0_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    array0_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    arc0_in = Grid(array0_in)
    arc0_out = Grid(array0_out)
    should_be = p._rotate_ccw(p._rotate_ccw(p._rotate_ccw(
                    p._draw_line_down(
                        p._rotate_ccw(arc0_in)
                    )(p._get(
                        p._objects(
                            p._rotate_ccw(arc0_in)
                        )
                        ) (0)
                    )
                )))
    assert arc0_out == should_be, 'incorrect example created'

    array1_in = np.array(
                [[0, 0, 0, 1, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    array1_out = np.array(
                [[1, 1, 1, 1, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    arc1_in = Grid(array1_in)
    arc1_out = Grid(array1_out)
    should_be = p._rotate_ccw(p._rotate_ccw(p._rotate_ccw(
                p._draw_line_down(
                    p._rotate_ccw(arc1_in)
                )(p._get(
                    p._objects(
                        p._rotate_ccw(arc1_in)
                    )
                    ) (0)
                )
            )))
    assert arc1_out == should_be, 'incorrect example created'

    examples0 = [((arc0_in,), arc0_out), ((arc1_in,), arc1_out)]
    task_drawlineleft = Task(
            "drawLineLeft",
            arrow(tgrid, tgrid),
            examples0
        )

    # ---------------------------------------------
    # TASK that draws a line up
    # ---------------------------------------------
    
    array0_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 0]])
    array0_out = np.array(
                [[0, 0, 0, 1, 0], 
                 [0, 0, 0, 1, 0], 
                 [0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0]])
    arc0_in = Grid(array0_in)
    arc0_out = Grid(array0_out)
    should_be = p._rotate_ccw(p._rotate_ccw(
                    p._draw_line_down(
                        p._rotate_ccw(p._rotate_ccw(arc0_in))
                    )(p._get(
                        p._objects(
                            p._rotate_ccw(p._rotate_ccw(arc0_in))
                        )
                        ) (0)
                    )
                ))
    assert arc0_out == should_be, 'incorrect example created'

    array1_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    array1_out = np.array(
                [[1, 0, 0, 0, 0], 
                 [1, 0, 0, 0, 0], 
                 [1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    arc1_in = Grid(array1_in)
    arc1_out = Grid(array1_out)
    should_be = p._rotate_ccw(p._rotate_ccw(
                    p._draw_line_down(
                        p._rotate_ccw(p._rotate_ccw(arc1_in))
                    )(p._get(
                        p._objects(
                            p._rotate_ccw(p._rotate_ccw(arc1_in))
                        )
                        ) (0)
                    )
                ))
    assert arc1_out == should_be, 'incorrect example created'

    examples0 = [((arc0_in,), arc0_out), ((arc1_in,), arc1_out)]
    task_drawlineup = Task(
            "drawLineUp",
            arrow(tgrid, tgrid),
            examples0
        )


 # ---------------------------------------------
    # TASK that draws a line to the right
    # ---------------------------------------------
    
    array0_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 0]])
    array0_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 1]])
    arc0_in = Grid(array0_in)
    arc0_out = Grid(array0_out)
    # should_be = p._rotate_ccw(
    #                 p._draw_line_down(
    #                     p._rotate_ccw(p._rotate_ccw(p._rotate_ccw(arc0_in)))
    #                 )(p._get(p._objects(arc0_in))(0))
    #             )
    # assert arc0_out == should_be, 'incorrect example created'

    array1_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    array1_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [1, 1, 1, 1, 1],
                 [0, 0, 0, 0, 0]])
    arc1_in = Grid(array1_in)
    arc1_out = Grid(array1_out)
    # should_be = p._rotate_ccw(
    #                 p._draw_line_down(
    #                     p._rotate_ccw(p._rotate_ccw(p._rotate_ccw(arc1_in)))
    #                 )(p._get(p._objects(arc0_in))(0))
    #             )
    # assert arc1_out == should_be, 'incorrect example created'

    examples0 = [((arc0_in,), arc0_out), ((arc1_in,), arc1_out)]
    task_drawlineright = Task(
            "drawLineRight",
            arrow(tgrid, tgrid),
            examples0
        )

    # ---------------------------------------------
    # TASK that moves an object down
    # ---------------------------------------------
    
    
    array0_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 1, 1, 0, 0], 
                 [0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0]])
    array0_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 1, 1, 0, 0],
                 [0, 0, 1, 0, 0]])
    arc0_in = Grid(array0_in)
    arc0_out = Grid(array0_out)
    should_be = p._move_down(arc0_in)(p._get(p._objects(arc0_in))(0))
    assert arc0_out == should_be, 'incorrect example created'

    array1_in = np.array(
                [[0, 1, 1, 1, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    array1_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 1, 1, 1, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    arc1_in = Grid(array1_in)
    arc1_out = Grid(array1_out)
    should_be = p._move_down(arc1_in)(p._get(p._objects(arc1_in))(0))
    assert arc1_out == should_be, 'incorrect example created'

    examples0 = [((arc0_in,), arc0_out), ((arc1_in,), arc1_out)]
    task_moveobjectdown = Task(
            "moveObjectDown",
            arrow(tgrid, tgrid),
            examples0
        )


    # ---------------------------------------------
    # TASK that moves an object to the left
    # ---------------------------------------------
    
    array0_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 1, 0, 0], 
                 [0, 1, 1, 0, 0],
                 [0, 0, 0, 0, 0]])
    array0_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 1, 0, 0, 0], 
                 [1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    arc0_in = Grid(array0_in)
    arc0_out = Grid(array0_out)
    should_be = p._rotate_ccw(p._rotate_ccw(p._rotate_ccw(
                    p._move_down(
                        p._rotate_ccw(arc0_in)
                    )(p._get(
                        p._objects(
                            p._rotate_ccw(arc0_in)
                        )
                        ) (0)
                    )
                )))
    assert arc0_out == should_be, 'incorrect example created'

    array1_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 1, 1, 0], 
                 [0, 0, 1, 1, 0],
                 [0, 0, 1, 1, 0]])
    array1_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 1, 1, 0, 0], 
                 [0, 1, 1, 0, 0],
                 [0, 1, 1, 0, 0]])
    arc1_in = Grid(array1_in)
    arc1_out = Grid(array1_out)
    should_be = p._rotate_ccw(p._rotate_ccw(p._rotate_ccw(
                p._move_down(
                    p._rotate_ccw(arc1_in)
                )(p._get(
                    p._objects(
                        p._rotate_ccw(arc1_in)
                    )
                    ) (0)
                )
            )))
    assert arc1_out == should_be, 'incorrect example created'

    examples0 = [((arc0_in,), arc0_out), ((arc1_in,), arc1_out)]
    task_moveobjectleft = Task(
            "moveObjectLeft",
            arrow(tgrid, tgrid),
            examples0
        )

    # ---------------------------------------------
    # TASK that moves an object up
    # ---------------------------------------------
    
    array0_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 1, 1, 1, 0], 
                 [0, 1, 0, 1, 0],
                 [0, 0, 0, 1, 0]])

    array0_out = np.array(
                [[0, 1, 1, 1, 0], 
                 [0, 1, 0, 1, 0], 
                 [0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0]])
    arc0_in = Grid(array0_in)
    arc0_out = Grid(array0_out)
    should_be = p._rotate_ccw(p._rotate_ccw(
                    p._move_down(
                        p._rotate_ccw(p._rotate_ccw(arc0_in))
                    )(p._get(
                        p._objects(
                            p._rotate_ccw(p._rotate_ccw(arc0_in))
                        )
                        ) (0)
                    )
                ))
    assert arc0_out == should_be, 'incorrect example created'

    array1_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [1, 1, 1, 0, 0],
                 [0, 0, 0, 0, 0]])
    array1_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [1, 1, 1, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    arc1_in = Grid(array1_in)
    arc1_out = Grid(array1_out)
    should_be = p._rotate_ccw(p._rotate_ccw(
                    p._move_down(
                        p._rotate_ccw(p._rotate_ccw(arc1_in))
                    )(p._get(
                        p._objects(
                            p._rotate_ccw(p._rotate_ccw(arc1_in))
                        )
                        ) (0)
                    )
                ))
    assert arc1_out == should_be, 'incorrect example created'

    examples0 = [((arc0_in,), arc0_out), ((arc1_in,), arc1_out)]
    task_moveobjectup = Task(
            "moveObjectUp",
            arrow(tgrid, tgrid),
            examples0
        )



    # ---------------------------------------------
    # TASK that moves an object to the right
    # ---------------------------------------------
    
    array0_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 1, 1, 1, 0], 
                 [0, 1, 0, 1, 0],
                 [0, 0, 0, 1, 0]])

    array0_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 1, 1, 1], 
                 [0, 0, 1, 0, 1],
                 [0, 0, 0, 0, 1]])
    arc0_in = Grid(array0_in)
    arc0_out = Grid(array0_out)
    # should_be = p._rotate_ccw(
    #                 p._move_down(
    #                     p._rotate_ccw(p._rotate_ccw(p._rotate_ccw(arc0_in)))
    #                 )(p._get(p._objects(arc0_in))(0))
    #             )
    # assert arc0_out == should_be, 'incorrect example created'

    array1_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [1, 1, 1, 0, 0],
                 [0, 0, 0, 0, 0]])
    array1_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0]])
    arc1_in = Grid(array1_in)
    arc1_out = Grid(array1_out)
    # should_be = p._rotate_ccw(
    #                 p._move_down(
    #                     p._rotate_ccw(p._rotate_ccw(p._rotate_ccw(arc1_in)))
    #                 )(p._get(p._objects(arc0_in))(0))
    #             )
    # assert arc1_out == should_be, 'incorrect example created'

    examples0 = [((arc0_in,), arc0_out), ((arc1_in,), arc1_out)]
    task_moveobjectright = Task(
            "moveObjectRight",
            arrow(tgrid, tgrid),
            examples0
        )


    # ---------------------------------------------
    # TASK that moves object right and draws line right
    # ---------------------------------------------
    
    array0_in = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0]])

    array0_out = np.array(
                [[0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 0, 1, 1, 1],
                 [0, 0, 0, 0, 0]])
    arc0_in = Grid(array0_in)
    arc0_out = Grid(array0_out)
    # print(arc0_out)
    # print(should_be)
    # assert arc0_out == should_be, 'incorrect example created'

    array1_in = np.array(
                [[1, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    array1_out = np.array(
                [[0, 1, 1, 1, 1], 
                 [0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])
    arc1_in = Grid(array1_in)
    arc1_out = Grid(array1_out)
    # assert arc1_out == should_be, 'incorrect example created'

    examples0 = [((arc0_in,), arc0_out), ((arc1_in,), arc1_out)]
    task_moveAndDrawLineRight = Task(
            "moveAndDrawLineRight",
            arrow(tgrid, tgrid),
            examples0
        )


    # ---------------------------------------------
    # PRINT
    # ---------------------------------------------
    training= [task_drawlinedown, task_moveobjectdown, 
            task_drawlineleft, task_moveobjectleft,
            task_drawlineup, task_moveobjectup,
            task_drawlineright, task_moveobjectright,
            task_moveAndDrawLineRight
            ]

    return training



