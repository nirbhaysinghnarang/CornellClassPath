
import unittest
from scraping import Scraper
from scheduler import Scheduler
from days import Day


class Tests(unittest.TestCase):
    def testScraping(self):
        MEDVL_scraper = Scraper("MEDVL", 19691)
        MEDVL_res = MEDVL_scraper.get_details()
        self.assertEqual(MEDVL_res.pattern, "MWF")
        self.assertEqual(MEDVL_res.building_location, "Goldwin Smith Hall")
        self.assertEqual(MEDVL_res.start_time, "09:05AM")
        self.assertEqual(MEDVL_res.end_time, "09:55AM")

        CS_2800_Scraper = Scraper("CS", 10026)
        CS_2800_res = CS_2800_Scraper.get_details()
        self.assertEqual(CS_2800_res.pattern, "MWF")
        self.assertEqual(CS_2800_res.building_location, "Statler Hall")
        self.assertEqual(CS_2800_res.start_time, "10:10AM")
        self.assertEqual(CS_2800_res.end_time, "11:00AM")

        CS_2110_Scraper = Scraper("CS", 10006)
        CS_2110_res = CS_2110_Scraper.get_details()
        self.assertEqual(CS_2110_res.pattern, "TR")
        self.assertEqual(CS_2110_res.building_location, "Statler Hall")
        self.assertEqual(CS_2110_res.start_time, "10:10AM")
        self.assertEqual(CS_2110_res.end_time, "11:00AM")

    def testScheduler(self):
        c1 = Scraper("MEDVL", 19691).get_details()
        c2 = Scraper("CS", 10026).get_details()
        c3 = Scraper("CS", 10006).get_details()
        scheduler = Scheduler([
            c1,
            c2,
            c3,
        ], home_base="High Rise 5")
        self.assertEqual(scheduler.getClassesForDay(Day.M), [c1, c2])
        self.assertEqual(scheduler.getClassesForDay(Day.T), [c3])
        self.assertEqual(scheduler.getClassesForDay(Day.W), [c1, c2])
        self.assertEqual(scheduler.getClassesForDay(Day.R), [c3])
        self.assertEqual(scheduler.getClassesForDay(Day.F), [c1, c2])

        self.assertEqual(scheduler.getWeeklySchedule(), {
            "M": [c1, c2],
            "T": [c3],
            "W": [c1, c2],
            "R": [c3],
            "F": [c1, c2]
        })
        print(scheduler.buildWeeklySchedule())


if __name__ == '__main__':
    unittest.main()
