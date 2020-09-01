from simple3D import display, Mesh, DisplayObject
from simple3D.mats.lineMeterial import LineMeterial
from simpleRotate.numpy import *
import numpy as np

vertices = [0.0, 0.0, 0.0,
            1, 0, 0.0,
            0, 0, 0,
            0, 1, 0,
            0, 0, 0,
            0, 0, 1]

vertices_color = [1, 0, 0,
                  1, 0, 0,
                  0, 1, 0,
                  0, 1, 0,
                  1, 1, 1,
                  1, 1, 1]

indices = [0, 1, 2, 3, 4, 5]


class RotateScene:
    def __init__(self):
        self.axis1 = self.get_axis()
        self.axis2 = self.get_axis()

        self.scene = display(self.axis1, self.axis2, rows=1, cols=2)

    def set_convert_func(self, func):
        self.scene.add(func)

    def get_axis(self):
        mesh = Mesh(vertices, indices, vectices_color=vertices_color)
        material = LineMeterial()
        axis = DisplayObject(mesh, material)
        return axis


if __name__ == "__main__":
    rotateScene = RotateScene()


    def func():
        rm = rotateScene.axis1.transform.rotation
        euler = RM2euler(rm)
        RM = euler2RM(euler)
        rotateScene.axis2.transform.rotation = RM


    rotateScene.set_convert_func(func)
