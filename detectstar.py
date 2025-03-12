import cv2
import numpy as np
from scipy.spatial import distance

from write_into_text_file import write_to_file


def detectstar(image_name,output_filepath):
        # Load the image in grayscale
    image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Use thresholding to isolate bright spots (stars)
    _, thresholded_image = cv2.threshold(blurred_image, 50, 200, cv2.THRESH_BINARY)

    # Detect contours, which represent the stars
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Show the detected stars on the image
    image_with_stars = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2RGB)

    # Initialize a list to hold centroids
    centroids = []
    for contour in contours:
        # Draw bounding rectangles around each star (as in the original code)
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image_with_stars, (x, y), (x + w, y + h), (0, 255, 0), 1)

        # Calculate the centroid of each contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroids.append((cx, cy))

            # Draw a small circle at the centroid position
            cv2.circle(image_with_stars, (cx, cy), 3, (0, 0, 255), -1)  # blue circle for centroids
           # for i in range(len(centroids) - 1):
                # Draw a line between consecutive centroids
            #    cv2.line(image_with_stars, centroids[i], centroids[i + 1], (255, 255, 0), 1)  # yellow line
    # Use scipy.spatial to connect centroids based on proximity
    if centroids:  # Ensure there are centroids to process
        centroid_array = np.array(centroids) # Convert list of centroids to a NumPy array
        pairwise_distances = distance.cdist(centroid_array, centroid_array, metric='euclidean')

        # Iterate over each centroid
        if len(centroid_array)> 1:
            for i, centroid in enumerate(centroid_array):
                # Find the closest centroid to the current one (excluding itself)
                distances_to_other = pairwise_distances[i]
                closest_index = np.argsort(distances_to_other)[1]  # [0] is the point itself, so take [1]
                closest_centroid = tuple(centroid_array[closest_index])

                # Draw a line between the current centroid and its closest centroid
                cv2.line(image_with_stars, tuple(centroid), closest_centroid, (255, 255, 0), 1)  # Yellow line
        else:
            write_to_file(output_filepath, "Only one star detected; no neighbors to connect.")
            # Optionally, draw something unique for the single centroid:
            cv2.circle(image_with_stars, tuple(centroid_array[0]), 5, (0, 255, 255), -1)  # Cyan circle

    # Print the pixel coordinates (centroids) of the detected stars
    if centroids:
        for i, (cx, cy) in enumerate(centroids):
            write_to_file(output_filepath,f"Star {i+1}: x = {cx}, y = {cy}")
            #output_file.write(f"Star {i+1}: x = {cx}, y = {cy}")
        # Display the result

        return centroids,image_with_stars,image,blurred_image,thresholded_image

    else:
        write_to_file(output_filepath, "No stars detected in this image.")
        return [],image_with_stars,image,blurred_image,thresholded_image

