from matplotlib import pyplot as plt


def plot_detectedstars(image_with_stars,image,blurred_image,thresholded_image,save_path=None):
    plt.figure()
    plt.subplot(144)
    plt.imshow(image_with_stars)
    plt.title("Detected Stars with Centroids")
    plt.axis("off")
    plt.subplot(141)
    plt.imshow(image, cmap="gray")
    plt.title("Gray Scale")
    plt.axis("off")
    plt.subplot(142)
    plt.imshow(blurred_image, cmap="gray")
    plt.title("Blurred Image")
    plt.axis("off")
    plt.subplot(143)
    plt.imshow(thresholded_image, cmap="gray")
    plt.title("Threshold Image")
    plt.axis("off")
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    plt.close()

def plot_centroids(image_with_stars,ra_vals, dec_vals,save_path=None):
    # Create a new plot to visualize both centroids in pixel space and RA/Dec values
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Show the image with detected centroids
    ax[0].imshow(image_with_stars)
    ax[0].set_title('Detected Stars (Centroids)')
    ax[0].axis('off')

    # Plot 2: Plot RA vs Dec (sky plot)
    ax[1].scatter(ra_vals, dec_vals, color='red', marker='o', label='Stars')
    ax[1].set_xlabel('Right Ascension (Degrees)')
    ax[1].set_ylabel('Declination (Degrees)')
    ax[1].set_title('Sky Plot (RA vs Dec)')
    ax[1].invert_xaxis()
    ax[1].grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    plt.close()

def plot_detectedstars_with_catalogue(ra_vals,dec_vals,catalog_ra,catalog_dec,save_path=None):
    # Plot detected stars (from your earlier centroid detection)
    plt.figure(figsize=(8, 6))
    plt.scatter(ra_vals, dec_vals, color='red', label='Detected Stars', s=10)

    # Plot catalog stars
    plt.scatter(catalog_ra, catalog_dec, color='blue', label='Catalog Stars', s=10)

    # Set plot details
    plt.gca().invert_xaxis()  # Invert RA axis (astronomical convention)
    plt.xlabel("Right Ascension (Degrees)")
    plt.ylabel("Declination (Degrees)")
    plt.title("Detected Stars and Catalog Overlay")
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    plt.close()

def plot_matched_stars(matched_detected_coords,matched_catalog_coords,matched_names,save_path=None):
    # Plot only matched stars
    plt.figure(figsize=(8, 6))
    plt.scatter(matched_detected_coords.ra.deg, matched_detected_coords.dec.deg,
                 color='red', label='Matched Detected Stars', s=10, marker='o')
    plt.scatter(matched_catalog_coords.ra.deg, matched_catalog_coords.dec.deg,
                 color='blue', label='Matched Catalog Stars', s=10, marker='x')
    # Annotate matched star names if provided
    for ra, dec, name in zip(matched_detected_coords.ra.deg, matched_detected_coords.dec.deg, matched_names):
        plt.annotate(name, (ra, dec), textcoords="offset points", xytext=(0, 10), ha='center', color='red',fontsize=8)

    # Customize plot
    plt.gca().invert_xaxis()  # Invert RA axis (astronomical convention)
    plt.xlabel("Right Ascension (Degrees)")
    plt.ylabel("Declination (Degrees)")
    plt.title("Matched Stars (Detected vs Catalog)")
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    plt.close()

def show_plots():
    plt.show()
