from datetime import datetime, timezone
from pytz import timezone


class ClassTime:
    eastern = timezone('US/Eastern')

    def __init__(self, time_int):
        # base UNIX time is 21 March 2022 08:00:00 GMT-04:00
        self._base_UNIX_time = 1647864000
        self._hours = time_int//100
        self._minutes = time_int % 100
        self._assertCorrectTime()

    def _assertCorrectTime(self):
        assert(self._hours >= 0 and self._hours <= 23)
        assert(self._minutes >= 0 and self._minutes <= 59)

    def getEpochRepr(self):
        return datetime(2022, 3, 21, self._hours,
                        self._minutes, 0, tzinfo=self.eastern).timestamp()

    def getDifference(self):
        return self.getEpochRepr()-self._base_UNIX_time
