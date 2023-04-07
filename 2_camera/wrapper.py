import numpy as np
from numpy import array as Vector
from numpy import array as Point
from numpy import array as Color


class Vec(np.ndarray):
    @staticmethod
    def normalize(vec):
        return vec / np.linalg.norm(vec)


class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def calculate_position(self, t):
        return self.origin + t * self.direction


class Camera():
    def __init__(self, focal_length, aspect_ratio, image_width, origin=Point([0, 0, 0])):
        self.image_heigth = int(image_width / aspect_ratio)
        self.image_width = image_width
        self.focal_length = focal_length
        self.aspect_ratio = aspect_ratio
        self.origin = origin

        self.viewport_height = 2.0
        self.viewport_width = aspect_ratio * self.viewport_height

    def get_ray(self, h, w):
        horizontal = Vector([self.viewport_width, 0, 0])
        vertical = Vector([0, self.viewport_height, 0])
        dz = Vector([0, 0, self.focal_length])
        lower_left_corner = self.origin - horizontal / 2 - vertical / 2 - dz
        direction = lower_left_corner + w * horizontal + h * vertical - self.origin
        return Ray(origin=self.origin, direction=direction)
