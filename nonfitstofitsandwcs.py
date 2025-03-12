from astropy.io import fits
from PIL import Image
import numpy as np
from astroquery.astrometry_net import AstrometryNet

def getwcsinfo(image_name,fits_file_name):
    # Set your Astrometry.net API key
    AstrometryNet.api_key = 'jfctggeewgfnbxhk'

    # Path to the input non-FITS image (e.g., PNG, JPEG)
    image_path = "C:/Users/lichu/PycharmProjects/StarTracker/pythonProject1/"+ image_name  # Replace with your image file path

    # Load the image and convert to grayscale
    image = Image.open(image_path)
    image_gray = image.convert('L')  # Convert to grayscale for simplicity

    # Convert to a NumPy array
    image_data = np.array(image_gray)

    # Create a FITS HDU (Header Data Unit) with the image data
    hdu = fits.PrimaryHDU(image_data)

    # Save the image as a FITS file
    fits_filename = fits_file_name
    hdu.writeto(fits_filename, overwrite=True)

    print(f"Image saved as {fits_filename}")

    # Optional: settings for solving the image
    settings = {
        'force_image_upload': False,  # Set to True if you want to force upload
    }

    # Solve the image to get WCS header
    try:
        print("Solving image using Astrometry.net...")

        # Solve the image, this will automatically upload and get the WCS solution
        wcs_header = AstrometryNet.solve_from_image(fits_filename, **settings)

        if wcs_header:
            print("WCS Solution Found!")

            # Optional: Check the WCS header (you can print it or inspect it)
            print(wcs_header)

            # Update the FITS file with the new WCS information
            with fits.open(fits_filename, mode='update') as hdulist:
                # hdulist[0] is the primary HDU (Header Data Unit) where the image data is stored
                # Add WCS information to the header (primary HDU header)
                hdulist[0].header.update(wcs_header)

                # Save the updated FITS file with the WCS header information
                output_fits_file = fits_file_name
                hdulist.flush()  # Write the changes to the file

            print(f"WCS information saved to {output_fits_file}")
        else:
            print("No WCS solution found.")
    except Exception as e:
        print(f"Error during WCS solving: {e}")
