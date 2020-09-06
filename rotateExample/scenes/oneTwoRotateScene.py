"""
    鼠标端只有一个轴，跟随端有两个轴
"""

from simple3D import Mesh, DisplayObject, Window, ViewPort
from simple3D.components.mouseRotate import MouseRotate
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
                  1, 0, 0,
                  1, 0, 0,
                  1, 0, 0,
                  1, 0, 0]

vertices_color2 = [0, 1, 0,
                  0, 1, 0,
                  1, 1, 1,
                  1, 1, 1,
                  0, 1, 0,
                  0, 1, 0]

indices = [0, 1, 2, 3, 4, 5]


class OneTwoRotateScene:
    def __init__(self):
        self.axis1 = self.get_axis(1)
        self.axis2_1 = self.get_axis(0)
        self.axis2_2 = self.get_axis(1)

        self.axis2_2.transform.parent = self.axis2_1.transform

        width, height = 1280, 720
        window = Window(width, height)
        viewports = ViewPort.get_aranged_viewports(width, height, 1, 2)
        window.add(*viewports)

        viewports[0].add(self.axis1)
        viewports[1].add(self.axis2_1, self.axis2_2)

        mouseMover = MouseRotate(window)
        mouseMover.add(self.axis1)

        window.add(mouseMover)
        self.scene = window

    def set_convert_func(self, func):
        self.scene.add(func)

    def get_axis(self, color=0):
        if color == 0:
            mesh = Mesh(vertices, indices, vectices_color=vertices_color)
        else:
            mesh = Mesh(vertices, indices, vectices_color=vertices_color2)
        material = LineMeterial()
        axis = DisplayObject(mesh, material)
        return axis

    def start(self):
        self.scene.render()

if __name__ == "__main__":
    rotateScene = OneTwoRotateScene()

    def func():
        rm1 = rotateScene.axis1.transform.rotation
        rotateScene.axis2_2.transform.rotation = rm1

    rotateScene.scene.add(func)
    rotateScene.start()