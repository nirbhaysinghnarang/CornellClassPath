from days import Day
from nav import Navigation
from course import Course
from classtime import ClassTime


class Scheduler:
    def __init__(self, courses, home_base):
        self.courses = courses
        self.home_base = home_base

    def getClassesForDay(self, day: Day):
        return [course for course in self.courses if day.name in course.pattern]

    def getWeeklySchedule(self):
        return {Day(i).name: self.getClassesForDay(Day(i)) for i in range(0, 5)}

    def buildDailySchedule(self, day: Day):
        directions = []
        courses = self.getClassesForDay(day=day)
        directions.append(self.startDay(day=day))
        for course in courses:
            try:
                nextCourse = self.getNextCourse(course, courses)
            except:
                break
            directions.append(
                self.goFrom(course_1=course, course_2=nextCourse)
            )
        directions.append(self.endDay(day=day))
        return directions

    def buildWeeklySchedule(self):
        return {Day(i).name: self.buildDailySchedule(Day(i)) for i in range(0, 5)}

    def isLast(self, obj, arr):
        return obj == arr[-1]

    def isFirst(self, obj, arr):
        return obj == arr[0]

    def getNextCourse(self, obj, arr):
        for i, nested_obj in enumerate(arr):
            if obj == nested_obj:
                return arr[i+1]

    def goFrom(self, course_1: Course, course_2: Course):
        depart_time = ClassTime(
            self.parse_time(
                time=course_1.end_time
            )
        ).getEpochRepr()
        return Navigation(course_1.building_location, course_2.building_location, departure_time=int(depart_time)+600).get_directions()

    def startDay(self, day: Day):
        firstCourse = self.getClassesForDay(day=day)[0]
        depart_time = ClassTime(
            self.parse_time(
                time=firstCourse.start_time
            )
        ).getEpochRepr()

        return Navigation(start=self.home_base, end=firstCourse.building_location, departure_time=int(depart_time)-1200).get_directions()

    def endDay(self, day: Day):
        lastCourse = self.getClassesForDay(day=day)[-1]
        depart_time = ClassTime(
            self.parse_time(
                time=lastCourse.end_time
            )
        ).getEpochRepr()
        return Navigation(start=lastCourse.building_location, end=self.home_base, departure_time=int(depart_time)+600).get_directions()

    def parse_time(self, time):
        print(time)
        if "AM" in time:
            return int(time.split("A")[0].replace(":", ""))
        return int(time.split("P")[0].replace(":", ""))
