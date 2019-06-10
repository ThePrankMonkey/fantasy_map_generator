#!../venv/bin/python

'''
Random Map Generator
'''


from PIL import Image
import random
import numpy


JUMP=10000


def make_noise(width, height):
    max_elevation = 0
    min_elevation = 0
    noise_map = []
    # make empty array
    for y in range(height):
        row = []
        for x in range(width):
            row.append(0)
        noise_map.append(row)
    # find noise
    for y in range(height):
        for x in range(width):
            if y == 0 and x ==0:
                elevation = random.randint(-JUMP, JUMP)
            elif y == 0:
                elevation = noise_map[y][x-1] + random.randint(-JUMP, JUMP)
            elif x == 0:
                elevation = noise_map[y-1][x] + random.randint(-JUMP, JUMP)
            else:
                average = (noise_map[y][x-1] + noise_map[y-1][x]) / 2.0
                elevation = average + random.randint(-JUMP, JUMP)
            # update min and max
            if elevation > max_elevation: max_elevation = elevation
            if elevation < min_elevation: min_elevation = elevation
            noise_map[y][x] = elevation
    # normalize noise
    diff_elevation = max_elevation - min_elevation
    for y in range(height):
        for x in range(width):
            noise_map[y][x] = (noise_map[y][x] - min_elevation) / diff_elevation
    return noise_map


def select_biomes(noise_map):
    new_map = []
    for row in noise_map:
        new_row = []
        for elevation in row:
            # water
            if elevation < 0.3:
                # deep water
                if elevation < 0.1:
                    pixel = (0, 0, 100)
                else:
                    pixel = (50,50,255)
            # land
            elif elevation >= 0.3 and elevation <= 0.6:
                pixel = (50,255,50)
            # mountain
            else:
                # snowcap
                if elevation > 0.9:
                    pixel = (255,255,255)
                else:
                    pixel = (255,200,100)
            new_row.append(pixel)
        new_map.append(new_row)
    return new_map


def add_borders(noise_map, empires, step):
    return noise_map


def show_map(noise_map):
    pixel_map = select_biomes(noise_map)
    map_numpy = numpy.array(pixel_map, dtype=numpy.uint8)
    map_image = Image.fromarray(map_numpy)
    map_image.format = "PNG"
    map_image.save("tmp.png")
    map_image.show()


def main(width, height, seed, empires=2, step=0, temperature=3):
    print("""Generating a map with the following settings:
    Height: {0}
    Width:  {1}
    Seed:   {2}
    """.format(width, height, seed))
    random.seed(seed)
    noise_map = make_noise(width, height)
    show_map(noise_map)
    # biome_map = select_biomes(noise_map)
    # border_map = add_borders(biome_map, empires, step)


if __name__ == "__main__":
    main(40, 30, random.randint(0,50))