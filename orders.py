from datetime import date, time, datetime, timedelta
import copy
from time_ranges import TimeRange, TimeRangeList

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
            print(f" | Series {self.series}",end="")
        print(f" | {self.date.isoformat()} | ",end="") 
        print(" / ".join(self.areas) + " | ",end="")
        self.times.print_ranges(sep=" / ")
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
            self.add_order(currDate, copy.deepcopy(times), copy.deepcopy(alist), self.next_series_id)
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
                self.modify_order(_id, copy.deepcopy(val), True)
            print(f"Series {series_id} modified.")
            self.sort_orders()
        return

    def print_orders(self):
        print("\nORDER LIST\n")
        for order in self.orders:
            order.print_details()
        print()
        return
