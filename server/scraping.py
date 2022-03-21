# helper functions for web scraping
import requests
import json
from course import Course

BASE_URL = "https://classes.cornell.edu/api/2.0/search/classes.json?"


class Scraper:
    def __init__(self, subject, course_number, roster="SP22"):
        self.subject = subject
        self.course_number = course_number
        self.roster = roster

    def is_valid_course(self):
        API_URL = BASE_URL + f"roster={self.roster}&subject={self.subject}"
        response = requests.get(API_URL)
        response_JSON = json.loads(response.text)
        if response_JSON.get("status") != "success" or response_JSON.get("status") is None:
            return (False, None)
        classes_list = response_JSON.get("data").get("classes")
        for c_class in classes_list:
            for enrollGroups in c_class.get("enrollGroups"):
                for offered_options in enrollGroups.get("classSections"):
                    if offered_options.get("classNbr") == self.course_number:
                        return (True, offered_options)
        return (False, None)

    def parse_course_details(self):
        course_tuple = self.is_valid_course()
        course_details = course_tuple[1].get("meetings")[0]
        if course_tuple == (False, None):
            return None
        return {
            "start_time": course_details.get("timeStart"),
            "end_time": course_details.get("timeEnd"),
            "building_location": course_details.get("bldgDescr"),
            "pattern": course_details.get("pattern")
        }

    def get_details(self):
        return Course(self.parse_course_details())
