class Course:
    def __init__(self, course_details):
        self.start_time = course_details.get("start_time")
        self.end_time = course_details.get("end_time")
        self.building_location = course_details.get("building_location")
        self.pattern = course_details.get("pattern")
