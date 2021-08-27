from datetime import date, time, datetime, timedelta
import copy

class RequestedOrder:
    def __init__(self, date, times, alist, idn, series):
        self.date = date
        self.times = times
        self.areas = alist
        self.id = idn
        self.series = series

    def print_details(self):
        print(f"ORDER {self.id}",end="")
        if self.series:
            print(f" | Series {self.series}")
        else:
            print()
        print(self.date.isoformat() + " | ",end="")
        print("/".join(self.areas))
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

    def earliest_datetime(self):
        earliest_time = self.times.time_ranges[0].t1
        return datetime.combine(self.date, earliest_time)

    def expired(self):
        #checks whether order can possibly be completed at current time
        latest_time = self.times.time_ranges[-1].t2
        latest_dt = datetime.combine(self.date, latest_time)
        latest_book_dt = latest_dt - timedelta(hours=1)
        return datetime.now() >= latest_book_dt
            


class OrderList:
    def __init__(self):
        self.orders = []
        self.next_order_id = 1
        self.next_series_id = 1
        return

    def conflicts_with(self, order2, excluding = None):
        #below code cannot be performed when only sorting after modifying 
        #or creating a new series, less efficient than searching entire list
        '''
        if (order2.date < self.orders[0].date 
                or order2.date > self.orders[-1].date):
            #before earliest current order date or after latest
            return False
        '''
        for order in self.orders:
            if order2.conflicts_with(order):
                if excluding == order:
                    continue
                return True
        return False

    def next_order(self):
        return self.orders[0]
    
    def get_order(self, order_id):
        for order in self.orders:
            if order.id == order_id:
                return order
        print(f"Order {order_id} not found")
        return False

    def get_series(self, series_id):
        ids = [o.id for o in self.orders if o.series == series_id]
        if len(ids) == 0:
            print(f"Series {series_id} not found")
            return False
        return ids

    def add_order(self, date, times, alist, series = None):
        new_order = RequestedOrder(date, times, alist, self.next_order_id, series)
        #print(date,times,alist,new_order.date,new_order.times)
        if self.conflicts_with(new_order):
            print("New order conflicts with existing one, could not be added.")
            print("New:")
            new_order.print_details()
            print("Old:")
            order.print_details()
            return
        self.orders.append(new_order)
        print(f"Order {self.next_order_id} successfully added!")

        if not series:
            self.sort_orders()

        self.next_order_id += 1
        return

    def add_series(self, sdate, times, alist, until,repeat=timedelta(days=7)):
        currDate = sdate
        while currDate <= until:
            self.add_order(currDate, times, alist, self.next_series_id)
            currDate += repeat
        
        print(f"Series {self.next_series_id} successfully added!")
        self.sort_orders()
        self.next_series_id += 1
        return

    def sort_orders(self):
        self.orders.sort(key = lambda x: x.earliest_datetime())
        return

    def remove_order(self, order_id):
        order = self.get_order(order_id)

        if order:
            self.orders.remove(order)
            print(f"Order {order_id} removed.")
            return True
        return False
    
    def remove_series(self, series_id):
        ids = self.get_series(series_id)

        if ids:
            #keep first order, delete rest of series
            self.get_order(ids[0]).series = None
            for _id in ids[1:]:
                self.remove_order(_id)
            print(f"Series {series_id} removed.")
            return True

        return False

    def remove_expired_orders(self):
        exp_orders = []
        for order in self.orders:
            if order.expired():
                exp_orders.append(order.id)
            else:
                break
        if len(exp_orders) == 0:
            print("None found")
        for _id in exp_orders:
            self.remove_order(_id)
        return

    def modify_order(self, order_id, val, series = False):
        order = self.get_order(order_id)

        if not order:
            return
        
        if type(val) == list:
            order.areas = val
            print(f"Order {order_id} workout areas successfully changed")

        elif type(val) == TimeRangeList:
            #create a copy of the order, modify and check for conflicts
            mod_order = copy.deepcopy(order)
            mod_order.times = val
            
            if self.conflicts_with(mod_order, excluding = order):
                print("Requested time changes create conflicts, no changes made")
                return
            order.times = val
            print(f"Order {order_id} time ranges successfully changed")

        elif type(val) == date:
            mod_order = copy.deepcopy(order)
            mod_order.date = val

            if self.conflicts_with(mod_order, excluding = order):
                print("Requested date change creates conflicts, no changes made")
                return
            order.date = val
            print(f"Order {order_id} date successfully changed")

        else:
            print("Invalid value type, no changes made")
            return
        
        if not series:
            self.sort_orders()
        return
        

    def modify_series(self, series_id, val):
        if type(val) == date:
            print("Cannot modify series dates, no changes made")
            return
        ids = self.get_series(series_id)

        if ids:
            for _id in ids:
                self.modify_order(_id, val, True)
            print(f"Series {series_id} modified.")
            self.sort_orders()
        return

    def print_orders(self):
        print("ORDER LIST")
        for order in self.orders:
            order.print_details()
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
        return

    def conflicts_with(self, TR2):
        if ((self.t2 >= TR2.t1 and self.t2 <= TR2.t2) 
                or (self.t1 >= TR2.t1 and self.t1 <= TR2.t2)):
            return True
        return False
    
    def print_range(self):
        t1str = self.t1.strftime(self.format)
        t2str = self.t2.strftime(self.format)
        print(f"{t1str} - {t2str}")
        return

class TimeRangeList:
    def __init__(self):
        self.time_ranges = []
        self.sort_ranges()
        return

    def print_ranges(self,prefix="", numbered=False):
        if len(self.time_ranges) == 0:
            print(prefix+'None\n')
            return
        for i in range(len(self.time_ranges)):
            print(prefix, end="")
            if numbered:
                print(str(i+1) + '. ',end="")
            self.time_ranges[i].print_range()
        print()
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

