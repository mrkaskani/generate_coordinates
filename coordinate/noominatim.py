import re

import numpy as np
from OSMPythonTools.nominatim import Nominatim


class RandomCoordinate(Nominatim):
    def __init__(self, location, quantity, **kwargs):
        super().__init__(**kwargs)
        self.quantity = quantity
        self.location = location

    @staticmethod
    def _get_lat(coordinate):
        return float(coordinate[0])

    @staticmethod
    def _get_lon(coordinate):
        return float(coordinate[1])

    @staticmethod
    def split_with_space(coordinate: str) -> list:
        split_pattern = re.compile(r"\s")
        return re.split(split_pattern, coordinate)[::-1]

    def find_geo_text(self):
        geotext = self.query(self.location, wkt=True)
        return geotext.toJSON()[0]["geotext"]

    def _generate_polygon(self):
        geotext = self.find_geo_text()
        pattern = re.compile(r"\d{2}.\d{1,7}\s\d{2}.\d{1,7}")
        return re.findall(pattern=pattern, string=geotext)

    def clean_polygon_data(self):
        polygon_data = self._generate_polygon()
        return list(map(self.split_with_space, polygon_data))

    def find_max_and_min_latitude(self):
        latitude_values = self.clean_polygon_data()
        split_latitude = list(map(self._get_lat, latitude_values))
        return min(split_latitude), max(split_latitude)

    def find_max_and_min_longitude(self):
        longitude_values = self.clean_polygon_data()
        split_longitude = list(map(self._get_lon, longitude_values))
        return min(split_longitude), max(split_longitude)

    def generate_random_coordinate(self):
        coordinate_list = []
        latitude = self.find_max_and_min_latitude()
        longitude = self.find_max_and_min_longitude()

        while len(coordinate_list) < self.quantity:
            random_latitude = np.random.uniform(latitude[0], latitude[1])
            random_longitude = np.random.uniform(longitude[0], longitude[1])
            coordinate = self.query(random_latitude, random_longitude, reverse=True, zoom=20)
            if coordinate:
                point = coordinate.toJSON()[0]
                address = point.get("address")
                if address:
                    country_code = address.get("country_code")
                    if country_code == "ir":
                        coordinate_list.append(point)
        return coordinate_list
