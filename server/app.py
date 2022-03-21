from flask import Flask
from flask import request
from scraping import Scraper
from course import Course
from scheduler import Scheduler
import json
import os
app = Flask(__name__)


@app.route("/build/", methods=["POST"])
def buildSchedule():
    body = json.loads(request.data)
    courses = body.get("courses")
    home_base = body.get("home_base")
    course_list = []
    if home_base is None:
        return failure_response("Missing home base.")
    if courses is None:
        return failure_response("Missing courses.")
    for subject in courses.keys():
        for numbers in courses.values():
            for number in numbers:
                print(f"Subject: {subject}, course: {number}")
                try:
                    course_list.append(Scraper(
                        course_number=number,
                        subject=subject
                    ).get_details())
                except:
                    return failure_response("Invalid course code and subject combination")
    scheduler = Scheduler(courses=course_list, home_base=home_base)
    return success_response(scheduler.buildWeeklySchedule())


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
