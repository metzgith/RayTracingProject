from wrapper import Vec, Ray, Camera, Point, Color, Vector, Sphere, World, Diffuse, Specular, Transmissive
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


def ray_color(ray: Ray, world: World, scatter_depth: int):
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


def add_random_scene(world: World):
    ground_material = Diffuse(color=Color([0.5, 0.5, 0.5]))
    world.add_object(Sphere(center=Point([0, -1000, 0]), radius=1000, material=ground_material))

    for a in range(-6, 6):
        for b in range(-6, 6):
            choose_mat = np.random.random()
            center = Point([a + 0.9 * np.random.random(), 0.2, b + 0.9 * np.random.random()])

            if (np.linalg.norm(center - Point([4, 0.2, 0])) > 0.9):
                if choose_mat < 0.7:
                    color = Color([np.random.random(), np.random.random(), np.random.random()])
                    mat = Diffuse(color=color)
                elif choose_mat < 0.9:
                    color = Color([np.random.uniform(0.6, 1), np.random.uniform(0.6, 1), np.random.uniform(0.6, 1)])
                    fuzz = np.random.uniform(0, 0.5)
                    mat = Specular(color=color)
                else:
                    mat = Transmissive(1.5)

            world.add_object(Sphere(center=center, radius=0.2, material=mat))

    material1 = Transmissive(1.5)
    world.add_object(Sphere(center=Point([0, 1, 0]), radius=1.0, material=material1))

    material2 = Diffuse(color=Color([0.4, 0.2, 0.1]))
    world.add_object(Sphere(center=Point([-4, 1, 0]), radius=1.0, material=material2))

    material3 = Specular(color=Color([0.7, 0.6, 0.5]))
    world.add_object(Sphere(center=Point([4, 1, 0]), radius=1.0, material=material3))


if __name__ == "__main__":
    heigth = 405
    width = 720

    cam1 = Camera(vfov=20, lookfrom=Point([0, 0, -1]), lookat=Point([0, 0, 1]))
    cam2 = Camera(vfov=20, lookfrom=Point([0, 0, -1]), lookat=Point([0, 1, 0]))
    cam3 = Camera(vfov=20, lookfrom=Point([0, 0, -1]), lookat=Point([0, 1, 1]))
    cam4 = Camera(vfov=20, lookfrom=Point([0, 0, -1]), lookat=Point([1, 0, 0]))
    cam5 = Camera(vfov=20, lookfrom=Point([0, 0, -1]), lookat=Point([1, 0, 1]))

    world = World()

    spec0 = Specular(color=Color([0.2, 0.2, 0]))
    spec1 = Specular(color=Color([0.5, 1, 1]))
    diff0 = Diffuse(color=Color([0, 0, 0.75]))
    diff1 = Diffuse(color=Color([1, 1, 0.5]))
    trans0 = Transmissive(ior=1.5)
    trans1 = Transmissive(ior=1.1)

    sp0 = Sphere(center=Point([0, -51, 0]), radius=50, material=spec0)
    sp1 = Sphere(center=Point([-14, -7, -10]), radius=1.75, material=diff0)
    sp2 = Sphere(center=Point([-10, -5, -10]), radius=2.5, material=trans0)
    sp3 = Sphere(center=Point([-4, -2, -10]), radius=3.25, material=spec1)
    sp4 = Sphere(center=Point([2, 2, -10]), radius=4, material=diff0)
    sp5 = Sphere(center=Point([8, 7, -10]), radius=4.75, material=trans1)
    objects = [sp0, sp1, sp2, sp3, sp4, sp5]

    world = World()
    world.add_objects(objects)

    main(cam1, world, height=heigth, width=width, samples=8, scatter_depth=8, filename="result_cam1.ppm")
    main(cam2, world, height=heigth, width=width, samples=8, scatter_depth=8, filename="result_cam2.ppm")
    main(cam3, world, height=heigth, width=width, samples=8, scatter_depth=8, filename="result_cam3.ppm")
    main(cam4, world, height=heigth, width=width, samples=8, scatter_depth=8, filename="result_cam4.ppm")
    main(cam5, world, height=heigth, width=width, samples=8, scatter_depth=8, filename="result_cam5.ppm")
