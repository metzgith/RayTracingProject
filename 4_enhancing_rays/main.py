from wrapper import Vec, Ray, Camera, World, Sphere, Point, Color, Vector
import numpy as np


def main(camera, world, samples, height=1080, width=1920, filename="output.ppm"):
    with open(filename, "w") as f:
        f.write(f"P3\n{width} {height}\n255\n")
        for h in range(height):
            for w in range(width):
                colors = np.array([0, 0, 0], dtype="float64")
                for i in range(samples):
                    dw = (w + np.random.random()) / (width - 1)
                    dh = (h + np.random.random()) / (height - 1)
                    ray = camera.get_ray(dh, dw)
                    colors += ray_color(ray, world)
                    color = np.clip(colors / samples, 0, 1)
                f.write(f"{int(255.99 * color[0])} {int(255.99 * color[1])} {int(255.99 * color[2])} ")
            f.write("\n")


def ray_color(ray, world):
    hit_context = world.get_nearest_hit(ray)
    if hit_context["distance"] > 0:
        return hit_context["color"]
    else:
        unit_direction = Vec.normalize(ray.direction)
        t = 0.5 * (unit_direction[1] + 1.0)
        color = (1.0 - t) * Color([1.0, 1.0, 1.0]) + t * Color([0.5, 0.7, 1.0])
        return color


if __name__ == "__main__":
    height = 720
    width = 1280

    #define camera
    camera = Camera(focal_length=1, aspect_ratio=(16 / 9), image_width=400)

    #define object
    sp0 = Sphere(center=Point([-16, -8, -10]), radius=1, color=Color([0, 0, 0]))
    sp1 = Sphere(center=Point([-14, -7, -10]), radius=1.75, color=Color([0, 0, 1]))
    sp2 = Sphere(center=Point([-10, -5, -10]), radius=2.5, color=Color([0, 1, 0]))
    sp3 = Sphere(center=Point([-4, -2, -10]), radius=3.25, color=Color([0, 1, 1]))
    sp4 = Sphere(center=Point([2, 2, -10]), radius=4, color=Color([1, 0, 0]))
    sp5 = Sphere(center=Point([8, 7, -10]), radius=4.75, color=Color([1, 0, 1]))
    objects = [sp0, sp1, sp2, sp3, sp4, sp5]

    world = World()
    world.add_objects(objects)

    main(camera, world, 1, height=height, width=width, filename="result1pps.ppm")
    main(camera, world, 2, height=height, width=width, filename="result2pps.ppm")
    main(camera, world, 4, height=height, width=width, filename="result4pps.ppm")
    main(camera, world, 8, height=height, width=width, filename="result8pps.ppm")
    main(camera, world, 16, height=height, width=width, filename="result16pps.ppm")