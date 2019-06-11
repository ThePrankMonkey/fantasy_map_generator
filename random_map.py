#!../venv/bin/python

'''
Random Map Generator
'''


from PIL import Image
import getopt
import numpy
import random
import sys

JUMP=10000


class Point(object):
    def __init__(self, y, x):
        self.y = y
        self.x = x
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.y == other.y and self.x == other.x
        else:
            return False
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        return "({}, {})".format(self.y, self.x)


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
            if elevation == "B":
                pixel = (0, 0, 0)
            # water
            elif elevation < 0.3:
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


def add_borders(noise_map, empires=2, step=0):
    height = len(noise_map)
    width = len(noise_map[0])
    # find border points
    border_points = []
    for _empire in range(empires):
        start_side = random.choice(["N", "S", "E", "W"])
        print("Finding a point on the {} side".format(start_side))
        while True:
            if start_side == "N":
                start_point = Point(0, random.randint(0, width - 1))
            if start_side == "S":
                start_point = Point(height - 1, random.randint(0, width - 1))
            if start_side == "E":
                start_point = Point(random.randint(0,height - 1), width - 1)
            if start_side == "W":
                start_point = Point(random.randint(0,height - 1), 0)
            if start_point not in border_points:
                border_points.append(start_point)
                print(start_point)
                # set start point on map
                # noise_map[start_point[0]][start_point[1]] = "B"
                break
    # add border lines
    center_point_x = int(width * random.randint(350,650)/1000.0)
    center_point_y = int(height * random.randint(350,650)/1000.0)
    center_point = Point(center_point_y, center_point_x)
    noise_map[center_point.y][center_point.x] = "B"
    for border_point in border_points:
        cur_point = border_point
        while cur_point != center_point:
            # print("Working from {} to center at {}".format(cur_point, center_point))
            # print(noise_map)
            # mark point
            noise_map[cur_point.y][cur_point.x] = "B"
            # move closer to center
            if random.randint(0,1) == 0:
                # work on y direction
                if cur_point.y != center_point.y:
                    if cur_point.y < center_point.y:
                        cur_point.y += 1
                    else:
                        cur_point.y -= 1
            else:
                # work on x direction
                if cur_point.x != center_point.x:
                    if cur_point.x < center_point.x:
                        cur_point.x += 1
                    else:
                        cur_point.x -= 1
    return noise_map

def test():
    array = []
    for _i in range(10):
        array.append([0]*8)
    print_map(add_borders(array))
    #test()

def print_map(noise_map):
    for row in noise_map:
        print(row)

def show_map(pixel_map):
    map_numpy = numpy.array(pixel_map, dtype=numpy.uint8)
    map_image = Image.fromarray(map_numpy)
    map_image.format = "PNG"
    map_image.save("tmp.png")
    map_image.show()


def main(argv):
    width = 30
    height = 20
    seed = 0
    empires = 2
    step = 0
    _temperature = 0
    try:
        opts, args = getopt.getopt(argv,"?w:h:s:e:",["width=","height=", "seed=", "empires="])
    except getopt.GetoptError:
        print("random_map.py -w <int> -h <int> -s <int> -e <int>")
        print("  -w --width=")
        print("  -h --height=")
        print("  -s --seed=")
        print("  -e --empires=")
        print("  -? --help")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-?', "--help"):
            print ('random_map.py -w <int> -h <int> -s <int> -e <int>')
            sys.exit()
        elif opt in ("-w", "--width"):
            width = int(arg)
        elif opt in ("-h", "--height"):
            height = int(arg)
        elif opt in ("-s", "--seed"):
            seed = int(arg)
        elif opt in ("-e", "--empires"):
            empires = int(arg)
    print("""Generating a map with the following settings:
    Height:  {0}
    Width:   {1}
    Seed:    {2}
    Empires: {3}
    """.format(width, height, seed, empires))
    random.seed(seed)
    noise_map = make_noise(width, height)
    noise_map = add_borders(noise_map, empires, step)
    noise_map = select_biomes(noise_map)
    show_map(noise_map)


if __name__ == "__main__":
    main(sys.argv[1:])
