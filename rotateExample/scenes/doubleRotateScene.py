from simple3D import display, Mesh, DisplayObject, Scene, ViewPort
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


class DoubleRotateScene:
    def __init__(self):
        self.axis1_1 = self.get_axis(0)
        self.axis1_2 = self.get_axis(1)
        self.axis2_1 = self.get_axis(0)
        self.axis2_2 = self.get_axis(1)

        self.axis1_2.transform.parent = self.axis1_1.transform
        # self.axis1_2.transform.pos = [0, 1, 0]
        self.axis2_2.transform.parent = self.axis2_1.transform
        # self.axis2_2.transform.pos = [0, 1, 0]

        width, height = 1280, 720
        scene = Scene(width, height, use_default_viewport=False)
        viewports = ViewPort.get_aranged_viewports(width, height, 1, 2)
        scene.add(*viewports)

        viewports[0].add(self.axis1_1, self.axis1_2)
        viewports[1].add(self.axis2_1, self.axis2_2)

        mouseMover = MouseRotate(scene)
        mouseMover.add(self.axis1_1, self.axis1_2)

        scene.add(mouseMover)
        self.scene = scene

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
        self.scene.render_scene()

if __name__ == "__main__":
    rotateScene = DoubleRotateScene()

    def func():
        rm1 = rotateScene.axis1_1.transform.rotation
        rotateScene.axis2_1.transform.rotation = rm1
        rm2 = rotateScene.axis1_2.transform.rotation
        rotateScene.axis2_2.transform.rotation = rm2

    rotateScene.scene.add(func)
    rotateScene.start()