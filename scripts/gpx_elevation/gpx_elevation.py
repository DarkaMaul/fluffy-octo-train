import gpxpy
import googlemaps
from gpxpy.gpx import GPX, GPXTrackPoint
from typing import List
from pathlib import Path


API_KEY: str = ""


def clean_trace(gpx: GPX):
    """Removes points from a GPX trace that are less than 10 meters apart.

    Args:
        trace: The GPX trace to clean.
    """
    
    # Réduire le nombre de points de la trace GPX en supprimant ceux qui sont espacés de moins de 10 mètres
    gpx.reduce_points(min_distance=10)

    # Supprimer les données d'altitude dans chaque point
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                point.elevation = None


def get_elevations(gpx: GPX, client: googlemaps.Client):
    """
    Get the elevation data for all the points in a GPX using the Google Maps Elevation API
    with batch requests of 500 locations at a time.

    Args:
        gpx (gpxpy.gpx.GPX): The GPX object to get the elevation data for.
        gmaps (googlemaps.Client): The Google Maps Client object to use for API requests.

    Returns:
        None. The function updates the GPX object in place with the elevation data for each point.
    """

    # Get all the points in the GPX
    points = [point for track in gpx.tracks for segment in track.segments for point in segment.points]
    # Split the points into batches of 500
    point_batches = [points[i:i+500] for i in range(0, len(points), 500)]

    # Iterate over each batch of points
    for batch in point_batches:
        # Extract the latitude and longitude for each point
        locations = [(point.latitude, point.longitude) for point in batch]
        # Call the Google Maps Elevation API
        elevations = client.elevation(locations)

        # Update the elevation data for each point in the batch
        for i, point in enumerate(batch):
            point.elevation = elevations[i]['elevation']
            

def work(gpx_file: Path, output_dir: Path):
    """Cleans and enhances a GPX trace by removing points that are less than 10 meters apart
    and adding elevation data using the Google Maps Elevation API.

    Args:
        gpx_file: The input GPX file.
        output_dir: The output directory to save the new GPX file.

    Returns:
        None. The function saves the cleaned and enhanced GPX trace to the output directory.
    """
    
    print(f"Chargement de la trace GPX depuis {gpx_file}...")
    with open(gpx_file, "r") as f:
        gpx = gpxpy.parse(f)

    print("Nettoyage de la trace...")
    clean_trace(gpx)

    print("Récupération des élévations...")
    gmaps = googlemaps.Client(key=API_KEY)
    get_elevations(gpx, gmaps)

    # Save the cleaned trace with up to date elevations
    output_file = output_dir / gpx_file.name
    print(f"Sauvegarde de la nouvelle trace dans {output_file}...")
    with open(output_file, "w") as f:
        f.write(gpx.to_xml())

def print_data(gpx: gpxpy.gpx.GPX, track_name: str) -> None:
    """Print the data in the format used by the blog.

    Args:
        gpx: The GPX trace
        track_name: Name of the track (used for the Name field).

    Returns:
        None.
    """
    moving_data = gpx.get_moving_data()
    moving_time = round(moving_data.moving_time / 3600)  # round to hour
    length_2d = gpx.length_2d() / 1000
    elevation_gain, elevation_loss = gpx.get_uphill_downhill()
    print(f"* **Name**: {track_name}")
    print(f"* **Length**: {length_2d:.0f} km")
    print(f"* **Elevation**: {elevation_gain:.0f} m D+ / {elevation_loss:.0f} m D-")
    print(f"* **Hiking time**: {moving_time:.0f} h")


def main():
    pass
