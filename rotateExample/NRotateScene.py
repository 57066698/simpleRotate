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
                  0, 1, 0,
                  0, 1, 0,
                  0, 1, 0,
                  0, 1, 0]

vertices_color3 = [1, 1, 1,
                  1, 1, 1,
                  1, 1, 1,
                  1, 1, 1,
                  1, 1, 1,
                  1, 1, 1]

indices = [0, 1, 2, 3, 4, 5]


class NRotateScene:
    def __init__(self, n=4):

        self.n = n
        self.axises1 = self.get_axises(n)
        self.axises2 = self.get_axises(n)

        width, height = 1280, 720
        scene = Scene(width, height, use_default_viewport=False)
        viewports = ViewPort.get_aranged_viewports(width, height, 1, 2)
        scene.add(*viewports)

        viewports[0].add(*self.axises1)
        viewports[1].add(*self.axises2)

        mouseMover = MouseRotate(scene)
        mouseMover.add(*self.axises1[:2])

        scene.add(mouseMover)
        self.scene = scene

    def set_convert_func(self, func):
        self.scene.add(func)

    def get_axises(self, n):
        axises = []

        for i in range(n):
            axis = self.get_axis(min(i, 2))
            axises.append(axis)
            if i > 0:
                axis.transform.parent = axises[0].transform
            if i > 1:
                axis.transform.euler = (0.1*i, 0.2*i, 0.3*i)

        return axises

    def get_axis(self, color=0):
        if color == 0:
            mesh = Mesh(vertices, indices, vectices_color=vertices_color)
        elif color == 1:
            mesh = Mesh(vertices, indices, vectices_color=vertices_color2)
        elif color == 2:
            mesh = Mesh(vertices, indices, vectices_color=vertices_color3)
        else:
            ValueError()
        material = LineMeterial()
        axis = DisplayObject(mesh, material)
        return axis

    def start(self):
        self.scene.render_scene()


if __name__ == "__main__":
    rotateScene = NRotateScene()

    def func():
        for i in range(rotateScene.n):
            rm = rotateScene.axises1[i].transform.rotation
            rotateScene.axises2[i].transform.rotation = rm

    rotateScene.scene.add(func)
    rotateScene.start()