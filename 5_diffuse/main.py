from wrapper import Vec, Ray, Camera, Point, Color, Vector, Sphere, World, Diffuse
import numpy as np


def main(camera, world, height=1080, width=1920, samples=8, scatter_depth=16, filename="output.ppm"):
    with open(filename, "w") as f:
        f.write(f"P3\n{width} {height}\n255\n")
        for h in range(height):
            for w in range(width):
                colors = Color([0, 0, 0], dtype="float64")
                for i in range(samples):
                    ray = camera.get_ray(
                        (h + np.random.randn()) / (height - 1),
                        (w + np.random.randn()) / (width - 1)
                    )
                    colors += ray_color(ray, world, scatter_depth)
                    color = np.clip(colors / samples, 0, 1)
                f.write(f"{int(255.99 * color[0])} {int(255.99 * color[1])} {int(255.99 * color[2])} ")
                f.write("\n")


def ray_color(ray, world, scatter_depth):
    if scatter_depth <= 0:
        return np.zeros(3)

    hit_context = world.get_nearest_hit(ray)
    if hit_context["distance"] > 0:
        scattered_ray, color = hit_context["material"].scatter(ray_in=ray, context=hit_context)
        return color * ray_color(ray=scattered_ray, world=world, scatter_depth=scatter_depth - 1)
    else:
        unit_direction = Vec.normalize(ray.direction)
        t = 0.5 * (unit_direction[1] + 1.0)
        color = (1.0 - t) * Color([1.0, 1.0, 1.0]) + t * Color([0.5, 0.7, 1.0])
        return color


if __name__ == "__main__":
    heigth = 405
    width = 720

    camera = Camera(focal_length=1, aspect_ratio=(16 / 9), image_width=400)

    mat0 = Diffuse(color=Color([0.2, 0.2, 0]))
    mat1 = Diffuse(color=Color([0.5, 1, 1]))
    mat2 = Diffuse(color=Color([0.75, 0.25, 0.75]))
    mat3 = Diffuse(color=Color([0, 0, 0.75]))
    mat4 = Diffuse(color=Color([1, 1, 0.5]))
    mat5 = Diffuse(color=Color([0.25, 0.5, 0.75]))

    sp0 = Sphere(center=Point([-16, -8, -10]), radius=1, material=mat0)
    sp1 = Sphere(center=Point([-14, -7, -10]), radius=1.75, material=mat1)
    sp2 = Sphere(center=Point([-10, -5, -10]), radius=2.5, material=mat2)
    sp3 = Sphere(center=Point([-4, -2, -10]), radius=3.25, material=mat3)
    sp4 = Sphere(center=Point([2, 2, -10]), radius=4, material=mat4)
    sp5 = Sphere(center=Point([8, 7, -10]), radius=4.75, material=mat5)
    objects = [sp0, sp1, sp2, sp3, sp4, sp5]

    world = World()
    world.add_objects(objects)

    main(camera, world, height=heigth, width=width, samples=8, scatter_depth=1, filename="result1rek.ppm")
    main(camera, world, height=heigth, width=width, samples=8, scatter_depth=2, filename="result2rek.ppm")
    main(camera, world, height=heigth, width=width, samples=8, scatter_depth=4, filename="result4rek.ppm")
    main(camera, world, height=heigth, width=width, samples=8, scatter_depth=8, filename="result8rek.ppm")
    main(camera, world, height=heigth, width=width, samples=8, scatter_depth=16, filename="result16rek.ppm")
