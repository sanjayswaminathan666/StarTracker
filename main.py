import glob
import os
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
#from catalogue_query import catalogue_query
from detectstar import detectstar
from fov import calculate_fov
from nonfitstofitsandwcs import getwcsinfo
from pixeltocelestial import calculate_ra_dec_from_centroids
from starmatching import query_simbad
from plot_results import plot_centroids,plot_detectedstars,plot_detectedstars_with_catalogue,plot_matched_stars
""",show_plots"""
from write_into_text_file import write_to_file
# Input and output directories
input_folder = "images"
output_dir = "output_plots"
os.makedirs(output_dir, exist_ok=True)
# Get all image files in the folder
image_list = glob.glob(os.path.join(input_folder, "*.jpg"))  # Change "*.jpg" to match your image format (e.g., "*.png")
for image_name in image_list:
   print(f"Processing {image_name}...")
   # Define output folder for this image
   base_name = os.path.splitext(os.path.basename(image_name))[0]  # Get the base file name
   image_output_dir = os.path.join(output_dir, base_name)
   os.makedirs(image_output_dir, exist_ok=True)
   output_file_name = f"{base_name}_output.txt"
   output_file_path = os.path.join("output_plots", output_file_name)
   with open(output_file_path, "w") as output_file:
      write_to_file(output_file_path,f"Processing image: {image_name}")
   # Generate the FITS filename
   fits_file_name = f"{base_name}.fits"
   centroids,image_with_stars,image,blurred_image,thresholded_image = detectstar(image_name,output_file_path)
   if centroids:
      plot_detectedstars(image_with_stars, image, blurred_image, thresholded_image,
                         save_path=os.path.join(image_output_dir, "detected_stars.png"))
      getwcsinfo(image_name,fits_file_name)
      fov_width, fov_height, search_radius,ra_centre,dec_centre= calculate_fov(fits_file_name,output_file_path)
      if ((search_radius == None) or (ra_centre == None)):
         print(f"Skipping {image_name} due to failed FoV calculation.")
         continue
      else:
         write_to_file(output_file_path,f"FoV: {fov_width:.2f}' x {fov_height:.2f}' (arcminutes) Search Radius: {search_radius:.2f} arcminutes")
         ra_dec_list = calculate_ra_dec_from_centroids(centroids,fits_file_name,output_file_path)
         ra_vals = [ra for ra, dec in ra_dec_list]
         dec_vals = [dec for ra, dec in ra_dec_list]
         plot_centroids(image_with_stars, ra_vals, dec_vals, save_path=os.path.join(image_output_dir, "centroids.png"))
         #catalog_ra , catalog_dec = catalogue_query(ra_centre,dec_centre,search_radius)
         #print(f"Catalog RA: {catalog_ra}, Catalog Dec: {catalog_dec}")
         #catalog_ra = [catalog_ra]
         #catalog_dec =[catalog_dec]
         catalog_ra, catalog_dec ,catalog_names= query_simbad(ra_centre, dec_centre, search_radius)
         if len(catalog_ra) == 0 or len(catalog_dec) == 0 or len(catalog_names) == 0:
            print(f"No catalog stars found for {image_name}, skipping this image.")
            continue  # Skip this image and move to the next one
         else:
            plot_detectedstars_with_catalogue(ra_vals, dec_vals, catalog_ra, catalog_dec,
                                              save_path=os.path.join(image_output_dir, "stars_with_catalogue.png"))
            # Define a matching threshold (in degrees), e.g., 1 arcsecond = 1/3600 degree
            matching_threshold_deg = 5 / 3600  # 5 arcsecond
            # Matching detected stars to catalog stars
            detected_coords = SkyCoord(ra=ra_vals, dec=dec_vals, unit=(u.deg, u.deg), frame='icrs')
            catalog_coords = SkyCoord(ra=catalog_ra, dec=catalog_dec, unit=(u.deg, u.deg), frame='icrs')
            idx, d2d, _ = detected_coords.match_to_catalog_sky(catalog_coords)
            matches = d2d < matching_threshold_deg * u.deg
            if np.sum(matches) == 0:
               print(f"No matching stars found for {image_name}, skipping this image.")
               continue  # Skip this image and move to the next one
            else:
               matched_ra = detected_coords[matches].ra.deg
               matched_dec = detected_coords[matches].dec.deg
               matched_names = catalog_names[idx[matches]]
               write_to_file(output_file_path,f"Number of matched stars: {np.sum(matches)}")
               write_to_file(output_file_path,"Matched stars and their names:")
               for ra, dec, name in zip(matched_ra, matched_dec, matched_names):
                  write_to_file(output_file_path,f"RA: {ra:.6f}, Dec: {dec:.6f}, Name: {name}")
               # Extract matched detected stars
               matched_detected_coords = detected_coords[matches]
               # Extract matched catalog stars using the indices
               matched_catalog_coords = catalog_coords[idx[matches]]
               #plot_matched_stars(matched_detected_coords,matched_catalog_coords)
               plot_matched_stars(matched_detected_coords,matched_catalog_coords,matched_names,save_path=os.path.join(image_output_dir, "matched_stars.png"))
      print(f"Results saved in {image_output_dir}")
      print(f"Results for {image_name} saved to {output_file_path}")
      #show_plots()
   else:
      print(f"No centroid Detected for {image_name},Skipping this image")
      continue
