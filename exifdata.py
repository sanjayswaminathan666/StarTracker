from PIL import Image
from PIL.ExifTags import TAGS
from geopy import distance  # To convert GPS coordinates if needed


def get_exif_data(image_path):
    """Extract EXIF data from an image file."""
    image = Image.open(image_path)
    exif_data = image._getexif()

    if not exif_data:
        print("No EXIF data found.")
        return None

    exif = {}
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        exif[tag_name] = value

    return exif


def get_gps_coordinates(exif_data):
    """Extract GPS coordinates from EXIF data."""
    if not exif_data or 'GPSInfo' not in exif_data:
        print("No GPS data found.")
        return None

    gps_info = exif_data['GPSInfo']

    if 1 not in gps_info or 2 not in gps_info:
        print("Incomplete GPS data.")
        return None

    # Latitude and Longitude are stored in DMS (Degrees, Minutes, Seconds) format
    latitude = gps_info[2]  # Latitude (degrees, minutes, seconds)
    longitude = gps_info[4]  # Longitude (degrees, minutes, seconds)

    # Convert DMS to Decimal Degrees
    lat_decimal = latitude[0] + (latitude[1] / 60.0) + (latitude[2] / 3600.0)
    lon_decimal = longitude[0] + (longitude[1] / 60.0) + (longitude[2] / 3600.0)

    if gps_info[3] == 'S':  # South latitude
        lat_decimal = -lat_decimal
    if gps_info[1] == 'W':  # West longitude
        lon_decimal = -lon_decimal

    return lat_decimal, lon_decimal


# Example usage
image_path = 'night_sky_image_1.jpg'
exif_data = get_exif_data(image_path)
gps_coordinates = get_gps_coordinates(exif_data)

if gps_coordinates:
    latitude, longitude = gps_coordinates
    print(f"Observer's Position: Latitude = {latitude}, Longitude = {longitude}")
else:
    print("No GPS data found in image.")
