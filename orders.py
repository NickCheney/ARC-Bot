from datetime import date, time, datetime, timedelta

class RequestedOrder:
        def __init__(self, date, times, alist, idn, series):
            self.date = date
            self.times = times
            self.areas = alist
            self.id = idn
            self.series = series

        def print_details(self):
            print("ORDER {}".format(self.id),end="")
            if self.series != None:
                print(" | Series {}".format(self.series))
            else:
                print()
            print(self.date.isoformat() + " | ",end="")
            print("/".join(areas))
            self.times.print_ranges(prefix="\t")
            return

        def conflicts_with(self, order2):
            if self.date != order2.date:
                return False
            
            for rng in self.times.time_ranges:
                for rng2 in order2.times.time_ranges:
                    if rng.conflicts_with(rng2):
                        return True
            return False

        def sort_key(self):
            earliest_time = self.times.time_ranges[0].t1
            return datetime.combine(self.date, earliest_time)


class OrderList:
    def __init__(self):
        self.orders = []
        self.next_order_id = 0
        self.next_series_id = 0

    def add_order(self, date, times, alist, series = None):
        new_order = RequestedOrder(date, times, alist, self.next_order_id, series)

        for order in self.orders:
            if date > order.date:
                #past latest date in sorted list
                break
            elif new_order.conflicts_with(order):
                print("New order conflicts with existing order, could not be added.")
                print("New:")
                new_order.print_details()
                print("Old:")
                order.print_details()
                return
        print("Order successfully added!")
        self.orders.append(new_order)

        if not series:
            self.sort()

        self.next_order_id += 1

    def add_series(self, start_date, times, alist, until,repeat=timedelta(days=7)):
        currDate = start_date
        while currDate <= until:
            self.add_order(currDate, times, alist, self.next_series_id)
            currDate += repeat

        self.sort()
        self.next_series_id += 1

    def sort(self):
        self.orders.sort(key = lambda x: x.sort_key())

    def remove_order(self, order_id):
        for order in self.orders:
            if order.id == order_id:
                self.orders.remove(order)
                print("Order {} removed.".format(order_id))
                return
        print("Order {} not found".format(order_id))
    
    def remove_series(self, series_id):
        ids = [o.id for o in self.orders if o.series == series_id]
        if len(ids) == 0:
            print("Series {} not found".format(series_id))
            return
        for _id in ids:
            self.remove_order(_id)
        print("Series {} removed.".format(series_id))

    def modify_order(self):
        pass

    def print_orders(self):
        print("ORDER LIST")
        for order in self.orders:
            print('\n')
            order.print_details()

    
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
        if ((self.t2 >= TR2.t1 and self.t2 <= TR2.t2) 
                or (self.t1 >= TR2.t1 and self.t1 <= TR2.t2)):
            return True
        return False
    
    def print_range(self):
        t1str = self.t1.strftime(self.format)
        t2str = self.t2.strftime(self.format)
        print("{0} - {1}".format(t1str, t2str))

class TimeRangeList:
    def __init__(self, ranges=[]):
        self.time_ranges = ranges
        self.sort_ranges()
        return

    def print_ranges(self,prefix=""):
        for tr in self.time_ranges:
            print(prefix, end="")
            tr.print_range()
        return

    def delete_range(self, ndx):
        del self.time_ranges[ndx]

    def add_range(self, new_range):
        for rng in self.time_ranges:
            if new_range.conflicts_with(rng):
                print("New time range has conflicts and could not be added")
                return
        self.time_ranges.append(new_range)
        self.sort_ranges()
        return
    
    def sort_ranges(self):
        self.time_ranges.sort(key=lambda x: x.t1)
        return

