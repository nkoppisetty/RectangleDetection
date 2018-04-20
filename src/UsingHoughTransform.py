import csv
import os
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'Nandita Koppisetty'
__email__ = 'nandita.iitkgp@gmail.com'

def find_correction_angle(binary_image):
    try:
        with open(binary_image, newline='') as csvfile:
            all_rows = csv.reader(csvfile, delimiter=',', quotechar='|')
            raw_image_data = list(all_rows)
    except FileNotFoundError:
        print('Error: File Not Found')

    raw_image_data = raw_image_data[1:]

    # Searching and storing all the edge points of the rectangle into rectangle_data array
    rectangle_data = []
    for i, row in enumerate(raw_image_data):
        for j, element in enumerate(row):
            if element == '1' and rectangle_data:
                rectangle_data.append([i, j])
                break

    for i, row in enumerate(raw_image_data):
        for j, element in enumerate(reversed(row)):
            if element == '1':
                rectangle_data.append([i, len(row) - j - 1])
                break

    # Applying Hough Transform Algorithm to find the lines with maximum points

    # Maximum distance of a line from origin, i.e. diagonal of the entire data-set region
    pmax = np.sqrt(np.square(len(raw_image_data))+np.square(len(raw_image_data[0])))

    # For storing distance (p) and theta space and the count of number of points contributing to the lines
    accumulator_array = [[0 for i in range(-90,91)] for j in range(int(pmax)+1)]

    # For every point, calculating p for every theta in -90 to 90, updating point count of (p,theta)
    for point in rectangle_data:
        for theta in range(-90, 91):
            p = round((point[0] * (np.cos(theta * np.pi / 180.0))) + (point[1] * (np.sin(theta * np.pi / 180.0))),1)
            accumulator_array[int(p)][theta] += 1;

    # Finding the line with maximum points and finding correction angle
    # Finding lines with number of points greater than 5 for plotting graph
    lines = []
    max_count = 0
    correction_angle = 0
    for i, row in enumerate(accumulator_array):
        for j, count in enumerate(row):
            if max_count < count:
                max_count = count
                correction_angle = 90-j
            # for plotting
            if count > 5:
                lines.append([p, 90-j, count])

    # Plotting theta vs number of points graph
    lines_transpose = list(map(list, zip(*lines)))
    plt.plot(lines_transpose[1], lines_transpose[2], ".");
    plt.show()

    return correction_angle

if __name__ == '__main__':
    image_path = os.path.abspath("rotated.csv")
    print("Correction Angle = ", find_correction_angle(binary_image=image_path))
