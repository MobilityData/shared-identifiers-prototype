from constants import (
    STOPS_CSV,
)
import pandas as pd


def load_stops():
    return pd.read_csv(STOPS_CSV, delimiter=";")


def save_stops(stops):
    stops.to_csv(STOPS_CSV, sep=";", index=False)
    return stops


def generate_id(prefix, latitude, longitude):
    latitude_str = format_coordinate(latitude)
    latitude_direction = "N" if latitude >= 0 else "S"
    longitude_str = format_coordinate(longitude)
    longitude_direction = "E" if latitude >= 0 else "W"
    return f"{prefix}_{latitude_str}_{latitude_direction}_{longitude_str}_{longitude_direction}"


def format_coordinate(coordinate):
    coordinate_str = format(coordinate, ".6f")
    coordinate_str = coordinate_str.replace(".", "_")
    coordinate_str = coordinate_str.replace("-", "")
    return coordinate_str
