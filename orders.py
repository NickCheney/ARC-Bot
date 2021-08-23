from datetime import date, time, datetime

class RequestedOrder:
        def __init__(self, date, times, alist, idn, series=None):
            self.date = date
            self.times = sorted(times, key = x[0])
            self.areas = alist
            self.id = idn
            self.series = series

        def print_details():
            print("ORDER {} SUMMARY".format(self.id))
            print("\t Date: {}".format(self.date.isoformat()))
            for t1, t2 in times:
                pass
            return

class TimeRange:
    def __init__(self, t1str, t2str, frmt = "%I:%M %p"):
        t1 = datetime.strptime(t1str, frmt).time()
        t2 = datetime.strptime(t2str, frmt).time()
        if t1 >= t2:
            raise ValueError
        self.t1 = t1
        self.t2 = t2
        self.format = frmt

    def conflicts_with(self, TR2):
        if (self.t2 >= TR2.t1 and self.t2 <= TR2.t2) or (self.t1 >= TR2.t1 and self.t1 <= TR2.t2):
            return True
        return False
    
    def print_range(self):
        t1str = self.t1.strftime(self.format)
        t2str = self.t2.strftime(self.format)
        print("{0} - {1}".format(t1str, t2str))

class TimeRangeList:
    def __init__(self, ranges=[]):
        self.time_ranges = ranges
        self.time_ranges.sort()
        return

    def print_ranges(self,prefix=""):
        for tr in self.time_ranges:
            print(prefix + tr.print_range())
        return

    def delete_range(self, ndx):
        pass

    def add_range(self, new_range):
        for rng in self.time_ranges:
            if new_range.conflicts_with(rng):
                print("New time range conflicts with an existing range")
                return
        self.time_ranges.append(new_range)
        self.sort_ranges()
        return
    
    def sort_ranges(self):
        self.time_ranges.sort(lambda x: x.t1)
        return

