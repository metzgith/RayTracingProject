from wrapper import Vec, Ray, Camera, Point, Color, Vector


def main(camera, height=1080, width=1920, filename="output.ppm"):
    with open(filename, "w") as f:
        f.write(f"P3\n{width} {height}\n255\n")
        for h in range(height):
            for w in range(width):
                dw = w / (width - 1)
                dh = h / (height - 1)
                ray = camera.get_ray(dh, dw)
                color = ray_color(ray)
                f.write(f"{int(255.99 * color[0])} {int(255.99 * color[1])} {int(255.99 * color[2])} ")
            f.write("\n")


def ray_color(ray):
    unit_direction = Vec.normalize(ray.direction)
    t = 0.5 * (unit_direction[1] + 1.0)
    color = (1.0 - t) * Color([1.0, 1.0, 1.0]) + t * Color([0.3, 0.5, 0.9])
    return color


if __name__ == "__main__":
    height = 1080
    width = 1920

    camera = Camera(focal_length=1, aspect_ratio=(16 / 9), image_width=400)

    main(camera, height=height, width=width, filename="result.ppm")
