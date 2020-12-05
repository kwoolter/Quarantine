

class QTimer:
    def __init__(self, ticks_per_hour = 60, hours_per_day:int = 24):
        self.ticks = 0
        self.ticks_per_hour = ticks_per_hour
        self.hours_per_day = hours_per_day

    def tick(self, increment : int = 1):
        self.ticks += increment

    @property
    def minutes(self):
        return self.ticks % (self.ticks_per_hour)

    @property
    def hour(self):
        return (self.ticks // (self.ticks_per_hour)) %  self.hours_per_day

    @property
    def day(self):
        return self.ticks // (self.ticks_per_hour * self.hours_per_day)

    def __str__(self):
        return f"Days {self.day:02} Hours {self.hour:02} Minutes {self.minutes:02}"


if __name__ == "__main__":

    q1 = QTimer()
    print(q1)

    q1.tick(137)
    print(q1)

    q1.tick(60* 34)
    print(q1)

    q1.tick(60)
    print(q1)

