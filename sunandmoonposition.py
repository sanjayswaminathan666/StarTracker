import cv2
import requests
from skyfield.api import Topos, load
from datetime import datetime, timezone
import numpy as np

# Camera specifications
fov_horizontal = 90  # Horizontal FoV in degrees
fov_vertical = 90  # Vertical FoV in degrees
image_width = 1920  # Image width in pixels
image_height = 1080  # Image height in pixels

# Example with ip-api
response = requests.get('http://ip-api.com/json/')
data = response.json()
latitude = data['lat']
longitude = data['lon']
print(f"Latitude: {latitude}, Longitude: {longitude}")

# Get the current system time in UTC
current_time = datetime.now(timezone.utc)
print(f"Current date and time (UTC): {current_time}")

# Load ephemeris data
eph = load('de421.bsp')
earth = eph['earth']
sun = eph['sun']
moon = eph['moon']
ts = load.timescale()

# Convert current time to Skyfield's Time object
skyfield_time = ts.utc(current_time.year, current_time.month, current_time.day,
                       current_time.hour, current_time.minute, current_time.second)

# Define observer's location
location = earth + Topos(latitude_degrees=latitude, longitude_degrees=longitude)

# Calculate celestial positions
sun_position = location.at(skyfield_time).observe(sun).apparent()
moon_position = location.at(skyfield_time).observe(moon).apparent()

# Convert to alt-az coordinates
alt_sun, az_sun, _ = sun_position.altaz()
alt_moon, az_moon, _ = moon_position.altaz()

# Print alt-az results
print(f"Sun: Altitude {alt_sun.degrees:.2f}°, Azimuth {az_sun.degrees:.2f}°")
print(f"Moon: Altitude {alt_moon.degrees:.2f}°, Azimuth {az_moon.degrees:.2f}°")


# Projection function with logging
def project_to_image_plane(alt, az, fov_h, fov_v, img_w, img_h):
    # Center azimuth at 180° and altitude at 0°
    az_centered = az.degrees - 180
    alt_centered = alt.degrees

    # Check if within FoV
    if abs(az_centered) <= fov_h / 2 and -fov_v / 2 <= alt_centered <= fov_v / 2:
        # Convert to image coordinates
        x = (az_centered + fov_h / 2) / fov_h * img_w
        y = (fov_v / 2 - alt_centered) / fov_v * img_h
        print(f"Object at Alt: {alt.degrees:.2f}°, Az: {az.degrees:.2f}° -> Pixel: ({int(x)}, {int(y)})")
        return int(x), int(y)
    else:
        print(f"Object at Alt: {alt.degrees:.2f}°, Az: {az.degrees:.2f}° is outside the screen")
        return None


# Project celestial objects
sun_pixel = project_to_image_plane(alt_sun, az_sun, fov_horizontal, fov_vertical, image_width, image_height)
moon_pixel = project_to_image_plane(alt_moon, az_moon, fov_horizontal, fov_vertical, image_width, image_height)

# Create a blank image
sky_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)

# Draw celestial objects with debugging
if sun_pixel:
    print(f"Drawing Sun at {sun_pixel}")
    cv2.circle(sky_image, sun_pixel, 15, (0, 255, 255), -1)  # Yellow for the Sun

if moon_pixel:
    print(f"Drawing Moon at {moon_pixel}")
    cv2.circle(sky_image, moon_pixel, 10, (200, 200, 255), -1)  # Light Blue for the Moon

# Display the simulated sky
cv2.imshow('Simulated Sky', sky_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
