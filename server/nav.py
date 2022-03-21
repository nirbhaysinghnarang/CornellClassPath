from lib2to3.pytree import type_repr
from key import key
import requests
from bs4 import BeautifulSoup
import json


class Navigation:

    API_KEY = key()
    BASE_URL = "https://maps.googleapis.com/maps/api/directions/json?"

    def __init__(self, start, end, departure_time=1647874217):
        self.start = start
        self.end = end
        self.departure_time = departure_time

    def query_api(self):
        API_URL = self.BASE_URL + \
            f"origin={self.start}&destination={self.end}&mode=transit&transit_mode=bus&departure_time={self.departure_time}&key={self.API_KEY}"
        print(API_URL)
        return json.loads(requests.get(API_URL).text)

    def parse_directions(self, directions_json):
        routes = directions_json.get("routes")
        if (self.typecheck(routes)):
            route = routes[0]
            legs = route.get("legs")
            if (self.typecheck(legs)):
                leg = legs[0]
                steps = leg.get("steps")
                return self.parse_steps(steps)

    def parse_steps(self, steps):
        steps_parsed = []
        for step in steps:
            if(step.get('travel_mode') == "WALKING"):
                steps_parsed.append(self.clean_html(
                    step.get("html_instructions")))
            elif(step.get('travel_mode') == "TRANSIT"):
                step_details = step.get('transit_details')
                arrival_stop = step_details.get("arrival_stop").get("name")
                arrival_time = step_details.get("arrival_time").get("text")
                depart_stop = step_details.get("departure_stop").get("name")
                depart_time = step_details.get("departure_time").get("text")
                num_stops = step_details.get("num_stops")
                line = step_details.get("line").get("short_name")
                steps_parsed.append(
                    f"From {depart_stop}, get on the {line} at {depart_time}. Ride for {num_stops} stops. Get off at {arrival_stop} at {arrival_time}."
                )
        return steps_parsed

    def get_directions(self):
        return self.parse_directions(
            directions_json=self.query_api()
        )

    def clean_html(self, html_string):
        return BeautifulSoup(html_string, "lxml").text

    def typecheck(self, arr):
        return arr is not None and type(arr) is list
