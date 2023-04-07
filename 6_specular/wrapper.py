import numpy as np
from numpy import array as Vector
from numpy import array as Point
from numpy import array as Color


class Vec():
    @staticmethod
    def normalize(vec: np.ndarray):
        return vec / np.linalg.norm(vec)

    @staticmethod
    def random_in_unit_sphere():
        while True:
            p = np.random.uniform(low=-1, high=1, size=(3))
            if np.linalg.norm(p) ** 2 >= 1:
                return Vec.normalize(p)

    @staticmethod
    def near_zero(vektor: Vector):
        # Return true if the vector is close to zero in all dimensions.
        if max(abs(vektor)) < 1e-8:
            return True
        return False

    @staticmethod
    def length_squared(vec: Vector):
        return (np.linalg.norm(vec)) ** 2


class Ray():
    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        self.direction = direction

    def calculate_position(self, t):
        p = self.origin + t * self.direction
        return p


class Camera():
    def __init__(self, focal_length, aspect_ratio, image_width, origin=np.zeros(3)):
        self.image_heigth = int(image_width / aspect_ratio)
        self.image_width = image_width
        self.focal_length = focal_length
        self.aspect_ratio = aspect_ratio
        self.origin = origin

        self.viewport_height = 2.0
        self.viewport_width = aspect_ratio * self.viewport_height

    def get_ray(self, h, w):
        horizontal = Vector([self.viewport_width, 0, 0])
        vertical = Vector([0, -self.viewport_height, 0])
        dz = Vector([0, 0, self.focal_length])
        lower_left_corner = self.origin - horizontal / 2 - vertical / 2 - dz
        direction = lower_left_corner + w * horizontal + h * vertical - self.origin

        return Ray(origin=self.origin, direction=direction)


class Material():
    def __init__(self, color: Color):
        self.color = color

    def scatter(self, ray_in, context: dict):
        print("Specify scatter")
        pass

    def reflect(self, vector: Vector, normal: Vector):
        return vector - 2 * np.dot(vector, normal) * normal


class Diffuse(Material):
    def __init__(self, color: Color):
        super().__init__(color)

    def scatter(self, ray_in: Ray, context: dict):
        new_direction = context["normal"] + Vec.random_in_unit_sphere()
        if Vec.near_zero(new_direction):
            new_direction = context["normal"]
        scattered_ray = Ray(origin=context["intersection_point"], direction=new_direction)
        return scattered_ray, self.color


class Specular(Material):
    def __init__(self, color: Color):
        super().__init__(color)

    def scatter(self, ray_in: Ray, context: dict):
        reflected = self.reflect(Vec.normalize(ray_in.direction), context["normal"])
        scattered = Ray(origin=context["intersection_point"], direction=reflected)
        return scattered, self.color

    def reflect(self, vector: Vector, normal: Vector):
        return vector - 2 * np.dot(vector, normal) * normal


class Sphere():
    def __init__(self, center=Point([0, 0, -1]), radius=0.5, color=Color([1, 0, 0]),
                 material=Material(color=Color([1, 1, 1]))):
        self.color = color
        self.center = center
        self.radius = radius
        self.material = material

    def hit_spehere(self, ray):
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

                context["material"] = self.material
        return context


class World():
    def __init__(self):
        self.objects = list()

    def add_objects(self, objs: list):
        for ob in objs:
            self.add_object(ob)

    def add_object(self, obj: Sphere):
        self.objects.append(obj)

    def get_nearest_hit(self, ray, t1=0.001, t2=np.inf):
        nearest_context = {"distance": -1}
        nearest_hit = t2
        for s in self.objects:
            context = s.hit_spehere(ray)
            if (context["distance"] < nearest_hit and context["distance"] > t1):
                nearest_hit = context["distance"]
                nearest_context = context
        return nearest_context
