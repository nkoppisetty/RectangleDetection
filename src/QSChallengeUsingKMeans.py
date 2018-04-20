import csv
import os
import random
import math
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
            if element == '1' and [i,j] not in rectangle_data:
                rectangle_data.append([i,j])
                break

    for i, row in enumerate(raw_image_data):
        for j, element in enumerate(reversed(row)):
            if element == '1' and [i,j] not in rectangle_data:
                rectangle_data.append([i, len(row)-j-1])
                break

    # Applying K means to segregate the rectangle into 4 clusters
    num_of_centers = 4
    centers, center_assignments = kmeans(num_of_centers, rectangle_data)

    centers_transpose = list(map(list, zip(*centers)))
    center_assignments_transpose = [[0 for i in range(2)] for j in range(num_of_centers)]

    # Plotting the four clusters
    for i in range(num_of_centers):
        center_assignments_transpose[i] = list(map(list, zip(*center_assignments[i])))
        plt.plot(center_assignments_transpose[i][0], center_assignments_transpose[i][1])

    # Plotting centers
    plt.plot(centers_transpose[0], centers_transpose[1],"o")
    plt.show()

    # The 4 centers obtained after applying k-means form a rectangle with parallel lines to original rectangle
    # calculating the slopes of the edges of the rectangle formed by the 4 points
    slopes = get_slopes(centers_transpose)

    # correction angles from the slopes obtained
    correction_angle1 = round(math.degrees(math.atan(slopes[0])),0)
    correction_angle2 = round(math.degrees(math.atan(slopes[1])),0)

    return correction_angle1

def kmeans(num_of_centers, data):
    # Step 1. Choose 4 Random centers from the dataset.
    centers = random.sample(data, num_of_centers)
    converged = False

    # Iterating until there is no change in centers
    while not converged:
        center_assignments = { i: [] for i in range(num_of_centers)}
        center_means = [[0 for i in range(2)] for j in range(num_of_centers)]
        num_data_points = [0] * num_of_centers

        # Step 2. Assigning each data point to a cluster by calculating its distance from each center
        for data_point in data:
            min = math.inf
            for i in range(num_of_centers):
                distance = math.sqrt(np.square((data_point[0] - centers[i][0])) + np.square((data_point[1] - centers[i][1])))
                if min > distance:
                    min = distance
                    center = i

            center_assignments[center].append([data_point[0], data_point[1]])
            center_means[center][0] += data_point[0]
            center_means[center][1] += data_point[1]
            num_data_points[center] += 1

        # Step 3. Calculating new centers by calculating mean of data points belonging to that cluster
        new_centers = [[0 for i in range(2)] for j in range(num_of_centers)]
        for i in range(num_of_centers):
            new_centers[i][0] = center_means[i][0] / num_data_points[i]
            new_centers[i][1] = center_means[i][1] / num_data_points[i]

        # checking and updating centers if there is any change in centers
        converged = is_converged(centers, new_centers, num_of_centers)
        centers = new_centers[:]

    return centers, center_assignments

# function to find if old and new centers are same
def is_converged(old_centers, new_centers,num_of_centers):
    for i in range(num_of_centers):
        if new_centers[i][0] != old_centers[i][0] or new_centers[i][1] != old_centers[i][1]:
            return False
    return True

# function to find the slopes of the edges of rectangle formed by the 4 points
def get_slopes(points):
    x = points[0]
    y = points[1]

    allslopes = []
    for i in range(len(x)):
        for j in range(i+1, len(x)):
            if (x[j]-x[i]) == 0:
                allslopes.append(math.inf)
            else:
                allslopes.append(round(-(y[j]-y[i])/(x[j]-x[i]),2))

    slopes = []
    for i in range(len(allslopes)):
        for j in range(i+1, len(allslopes)):
            if round(allslopes[j],1) == round(allslopes[i],1):
                slopes.append((allslopes[i]+allslopes[j])/2)

    return slopes

if __name__ == '__main__':
    image_path = os.path.abspath("rotated.csv")
    print("Correction Angle =", find_correction_angle(binary_image=image_path))