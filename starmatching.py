# Query SIMBAD for catalog stars
import requests
from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
import astropy.units as u
import time

"""
    def query_simbad(ra, dec, radius, retries=3, delay=5):
    Query SIMBAD for stars around the given coordinates within a radius.
    coord = SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg), frame='icrs')
    result_table = Simbad.query_region(coord, radius=(radius) * u.arcminute)
    if result_table is None:
        print("No stars found in the catalog for the given region.")
        return [], []
    catalog_coords = SkyCoord(result_table['RA'], result_table['DEC'], unit=(u.hourangle, u.deg), frame='icrs')
    # Extract star names/IDs
    catalog_names = result_table['MAIN_ID']
    return catalog_coords.ra.deg, catalog_coords.dec.deg , catalog_names
    """

def query_simbad(ra, dec, radius, retries=3, delay=5):
    coord = SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg), frame='icrs')

    for attempt in range(retries):
        try:
            # Query SIMBAD region
            result_table = Simbad.query_region(coord, radius=(radius) * u.arcminute)

            # If no stars are found
            if result_table is None:
                print(f"No stars found in the catalog for the region centered at RA={ra}, Dec={dec}.")
                return [], [], []

            # Extract star coordinates and names
            catalog_coords = SkyCoord(result_table['RA'], result_table['DEC'], unit=(u.hourangle, u.deg), frame='icrs')
            catalog_names = result_table['MAIN_ID']

            return catalog_coords.ra.deg, catalog_coords.dec.deg, catalog_names

        except requests.exceptions.ReadTimeout:
            if attempt < retries - 1:
                print(f"Timeout occurred. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
                time.sleep(delay)
            else:
                print("Query failed after multiple attempts.")
                return [], [], []

        except Exception as e:
            print(f"An error occurred: {e}")
            return [], [], []
