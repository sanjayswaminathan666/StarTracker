import numpy as np
from astropy.io import fits
from astropy.wcs import WCS

from write_into_text_file import write_to_file


def calculate_ra_dec_from_centroids(centroids, fits_file_with_wcs,output_filepath):
    # Load the FITS file with WCS information
    with fits.open(fits_file_with_wcs) as hdulist:
        wcs = WCS(hdulist[0].header)

    # Convert centroids (pixel coordinates) to world coordinates (RA, Dec)
    centroids_array = np.array(centroids)  # Convert list to NumPy array
    world_coordinates = wcs.pixel_to_world(centroids_array[:, 0], centroids_array[:, 1])

    # Extract RA and Dec from the result
    ra_dec_list = [(coord.ra.degree, coord.dec.degree) for coord in world_coordinates]

    # Print and return the result
    for i, (ra, dec) in enumerate(ra_dec_list):
        write_to_file(output_filepath, f"Star {i + 1}: RA = {ra:.6f}°, Dec = {dec:.6f}°")
        #output_file.write(f"Star {i + 1}: RA = {ra:.6f}°, Dec = {dec:.6f}°")

    return ra_dec_list
