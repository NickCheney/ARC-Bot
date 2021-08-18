

class RequestedOrder:
        def __init__(self, date, times, atype, alist, idn, series=None):
            self.date = date
            self.times = sorted(times, key = x[0])
            self.areas = {"type": atype, "alist" : alist}
            self.id = idn
            self.series = series
