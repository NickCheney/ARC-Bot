from datetime import date, time, datetime, timedelta
import copy

class TimeRange:
    def __init__(self, t1str, t2str, frmt = "%I:%M %p"):
        t1 = datetime.strptime(t1str, frmt).time()
        t2 = datetime.strptime(t2str, frmt).time()
        if t1 >= t2:
            raise ValueError
        self.t1 = t1
        self.t2 = t2
        self.format = frmt
        return

    def conflicts_with(self, TR2):
        if ((self.t2 >= TR2.t1 and self.t2 <= TR2.t2) 
                or (self.t1 >= TR2.t1 and self.t1 <= TR2.t2)):
            return True
        return False
    
    def to_str(self):
        t1str = self.t1.strftime(self.format)
        t2str = self.t2.strftime(self.format)
        return f"{t1str} - {t2str}"

class TimeRangeList:
    def __init__(self):
        self.time_ranges = []
        self.sort_ranges()
        return

    def print_ranges(self, prefix="", sep = "\n", numbered=False):
        if len(self.time_ranges) == 0:
            print(prefix+'None')
            return

        rangestrs = [r.to_str() for r in self.time_ranges]
        if numbered:
            rangestrs = [f"{i+1}. " + rangestrs[i] for i in range(len(rangestrs))]

        rangestrs = [prefix + r for r in rangestrs]
        outstr = sep.join(rangestrs)
        print(outstr)
        return

    def delete_range(self, ndx):
        try:
            if ndx < 0:
                raise ValueError
            del self.time_ranges[ndx]
            return True
        except:
            print("Invalid time range number, see above")
        return False

    def add_range(self, new_range):
        for rng in self.time_ranges:
            if new_range.conflicts_with(rng):
                print("New time range has conflicts and could not be added")
                return False
        self.time_ranges.append(new_range)
        self.sort_ranges()
        return True
    
    def sort_ranges(self):
        self.time_ranges.sort(key=lambda x: x.t1)
        return

