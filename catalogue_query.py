from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import astropy.units as u


def catalogue_query(ra_centre, dec_centre, search_radius):
    # Initialize Vizier with default settings
    vizier = Vizier(columns=["RA_ICRS", "DE_ICRS"])
    vizier.ROW_LIMIT = -1  # No limit on the number of rows returned

    # Perform the query
    result = vizier.query_region(SkyCoord(ra=ra_centre, dec=dec_centre, unit="deg", frame="icrs"),
                                 radius=f"{search_radius} deg",
                                 catalog="I/259/tyc2")

    #I / 350 / gaiaedr3 , I / 239 / hip_main
    if result:
        catalog = result[0]  # Get the first table
        ra_list = catalog["RA_ICRS"].data  # RA in degrees
        dec_list = catalog["DE_ICRS"].data  # Dec in degrees
        print(f"Retrieved {len(ra_list)} stars from Tycho.")
        return ra_list, dec_list
    else:
        print(f"No stars found in catalog for the specified region.")
        return [], []
