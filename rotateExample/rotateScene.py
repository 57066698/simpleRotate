from simple3D import Scene, DisplayObject, Mesh
from simple3D.components.moseMoveDisplayObject import MouseMoveDisplayObject
from simple3D.mats.lineMeterial import LineMeterial
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

        self.axis2.transform.pos += np.array([1, 0, 0])
        self.axis1.transform.pos += np.array([-1, 0, 0])

        scene = Scene()
        scene.add(self.axis1, self.axis2)
        mouseMove = MouseMoveDisplayObject(scene)
        mouseMove.add(self.axis1)  #
        scene.add(mouseMove)

        def func():
            euler = self.axis1.transform.euler
            self.axis2.transform.euler = euler

        scene.add(func)

        scene.render()

    def get_axis(self):
        mesh = Mesh(vertices, indices, vectices_color=vertices_color)
        material = LineMeterial()
        axis = DisplayObject(mesh, material)
        return axis


if __name__ == "__main__":
    rotateScene = RotateScene()
