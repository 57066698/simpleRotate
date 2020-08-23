from simple3D import Scene, DisplayObject, Mesh, Camera, MouseMove
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

        self.axis2.transfrom.pos += np.array([1, 0, 0])
        self.axis1.transfrom.pos += np.array([-1, 0, 0])

        scene = Scene()
        scene.add(self.axis1, self.axis2)
        mouseMove = MouseMove(scene) # 集中到scene
        camera = scene.default_camera
        mouseMove.set_camera(camera) #
        scene.add(mouseMove)
        scene.render()

    def get_axis(self):
        mesh = Mesh(vertices, indices, vectices_color=vertices_color)
        material = LineMeterial()
        axis = DisplayObject(mesh, material)
        return axis

if __name__ == "__main__":
    rotateScene = RotateScene()