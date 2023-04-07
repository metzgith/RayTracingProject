import numpy as np
from numpy import array as Vector
from numpy import array as Point
from numpy import array as Color


class Vec(np.ndarray):
    @staticmethod
    def normalize(vec: Vector):
        return vec / np.linalg.norm(vec)


class Ray():
    def __init__(self, origin: Point, direction: Vector):
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


class Sphere():
    def __init__(self, center=Point([0, 0, -1]), radius=0.5, color=Color([1, 0, 0])):
        self.color = color
        self.center = center
        self.radius = radius

    def hit_spehere(self, ray: Ray):
        context = {"distance": -1}
        oc = ray.origin - self.center
        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if (discriminant >= 0):
            t = (-b - np.sqrt(discriminant)) / (2.0 * a)
            if t > 0:
                context["distance"] = t
                context["intersection_point"] = ray.calculate_position(t)
                normal = Vec.normalize(context["intersection_point"] - self.center)
                context["front_face"] = (np.dot(ray.direction, normal) < 0)
                context["normal"] = normal if context["front_face"] else -normal
                context["color"] = self.color
        return context


class World():
    def __init__(self):
        self.objects = list()

    def add_objects(self, objs: list):
        for ob in objs:
            self.add_object(ob)

    def add_object(self, obj: Sphere):
        self.objects.append(obj)

    def get_nearest_hit(self, ray: Ray, t1=0.001, t2=np.inf):
        nearest_context = {"distance": -1}
        nearest_hit = t2
        for s in self.objects:
            context = s.hit_spehere(ray)
            if (context["distance"] < nearest_hit and context["distance"] > t1):
                nearest_hit = context["distance"]
                nearest_context = context
        return nearest_context
