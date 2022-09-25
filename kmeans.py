"""
This program runs the kmeans algorithm
on data from 3 different .csv files. 

The kmeans algorithm works as follows...
1) Choose the amount of cluster centres to work with.
2) Create cluster centres by calculating the mean of the data points
   from data in the .csv file.
3) Calculate the euclidean distance between each data point
   from the .csv file and the cluster centres.
4) Assign each datapoint to the cluster centre that has the shortest
   distance to it.
5) Repeat these steps for all data points in the given input data
   until iteration amount by user has been met (or ultimately until
   convergence is reached).

"""

import matplotlib.pyplot as plt
import math
import csv
import random


# Define read_from_file() that takes in user file choice and tries to open
def read_from_file(file):
    
    # Open csv file chosen by user and add each value to country_data list
    with open(data_set) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        for row in readCSV:
            if row[0] != 'Countries':
                birth_int = float(row[1])
                life_int = float(row[2])

                country_data.append([birth_int, life_int])


# Define calculate_means() to calculate mean of x and y data
def calculate_means(points):
    y_sum = 0
    x_sum = 0

    for p in points:
        x_sum += p[0]
        y_sum += p[1]

    return [x_sum / len(points), y_sum / len(points),]


# Define euclidean_distance() to calculate euclidean distance between points
def euclidean_distance(point1, point2):

    return math.sqrt((point2[1] - point1[1]) ** 2 + (point2[0] - point1[0]) ** 2)


# Define find_centroid() calculate centre point of cluster and compare it to
# data points to find those with smallest distnace then return its index
def find_centroid(center_points, point):
    closest_point = 0
    distance_to_closest_center_point = euclidean_distance(center_points[0], point)

    for center_point_idx, center_point in enumerate(center_points):
        this_distance = euclidean_distance(center_point, point)

        if this_distance < distance_to_closest_center_point:
            distance_to_closest_center_point = this_distance
            closest_point = center_point_idx

    return closest_point


# Define build_clusters() to sort data into clusters
# This function stores (in a dictionary) number of clusters input by the user
# Data is then compared to centroids and clusters are built
def build_clusters(center_points, points):
    clusters = [{'center_point': center_point, 'data_points': []}
                for center_point in center_points]

    # place each data-point into the cluster with the nearest centroid
    for point in points:
        nearest_center_point_idx = find_centroid(center_points, point)
        clusters[nearest_center_point_idx]['data_points'].append(point)

    return clusters


# Start the main execution of the program.
if __name__ == '__main__':

    # Create list to store x (birth-rate) and y axis (life expectancy) values
    country_data = []

    # Welcome message
    print('\nWelcome to the K-Means Algorithm Program.')

    # Request file choice from user, ensure correct file name with while loop
    loop = True
    while loop:
        data_set = input('''Plese enter the file name you want to use
(ensure correct spelling and .csv extension):
\n\ndata1953.csv\ndata2008.csv\ndataBoth.csv \n''' )

        # Call read_from_file method
        try:
            read_from_file(data_set)
            loop = False

        except FileNotFoundError as err:
            print(f"File '{data_set}' not found. Please try again.\n")
            loop = True

    cluster_amount = int(input('\nHow many clusters would you like to include?'))
    iterations = int(input('\nHow many iterations would you like to run? '))

    # Create built_cluster list to store clusters
    built_clusters = []

    """
    For loop runs the number of iterations specified by the user.
    For the first loop, no mean has been set, therefore when 'i == 0',
    random points are drawn, depending on the number of clusters
    specified by the user. They are then stored in the list 'cluster_centroid'.

    """
    for i in range(iterations):
        if i == 0:
            # First iteration draws random mean point
            cluster_centroid = random.sample(country_data, cluster_amount)

        else:
            # New means are calculated within the clusters and added to the list.
            cluster_centroid = [calculate_means(c['data_points'])
                                for c in built_clusters]

        # Set list values with  number of built clusters specified by user 
        # and place the data points in the correct clusters.
        built_clusters = build_clusters(cluster_centroid, country_data)

    # Create graph figure and set appropriate headings and labels
    figure = plt.figure()
    plt.title('Birth Rates and Life Expectancies in Countries Across the World')
    plt.xlabel('Birth Rates')
    plt.ylabel('Life Expectancies')

    # Setting variables to store the number of countries, cluster count and list
    # of country names
    cluster_count = 1
    country_list = []

    # Randomly choose color for each built cluster
    for cluster in built_clusters:
        r = random.random()
        b = random.random()
        g = random.random()

        # Color list created with random choices.
        color = [[r, g, b]]
        country_number = 0

        # Loop through data-points within each cluster
        # Seperate to x and y and calculate sum and average for each cluster.
        for point in cluster['data_points']:
            x = point[0]
            y = point[1]
            sum_x = 0
            sum_y = 0
            sum_x += x
            sum_y += y

            # Scatter each point in it's chosen color.
            plt.scatter(point[0], point[1], c=color)

            # Increment country count for each point in a cluster.
            country_number += 1

            # Open csv again to match cluster points in list to countries in
            # file and add them to country_data list
            with open(data_set) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    if row[0] != 'Countries' and x == float(row[1]) and y == float(row[2]):
                        country_name = str(row[0])
                        country_list.append(country_name)

        # Display information about csv and cluster data to the user
        print(f"\nCluster {cluster_count} contains {country_number} countries.")
        print(f"\nCountries in cluster {cluster_count} are {country_list}")
        print(f"\nCluster {cluster_count}'s mean Birth Rate is: {sum_x / country_number}")
        print(f"\nCluster {cluster_count}'s mean Life Expectancy is: {sum_y / country_number}")

        # Clear country_list and increment cluster_count between each iteration
        country_list.clear()
        cluster_count += 1

    # Display the scatter graph.
    plt.show()
