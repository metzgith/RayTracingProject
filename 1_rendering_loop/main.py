import numpy as np
import matplotlib.pyplot as plt

def main(height=1080, width=1920, color=(128, 64, 255), filename="output.ppm"):
    #writing into file to render multiple pictures with different params
    with open(filename, "w") as f:
        f.write(f"P3\n{width} {height}\n255\n")
        for i in range(height):
            for j in range(width):
                f.write(f"{color[0]} {color[1]} {color[2]} ")
            f.write('\n')

if __name__ == "__main__":
    height = 1080
    width = 1920

    main(height=height, width=width, filename="result.ppm")

