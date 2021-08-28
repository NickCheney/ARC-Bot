import os
import sys
import pickle
from orders import OrderList
from time_ranges import TimeRange, TimeRangeList
import book_workout
from datetime import date, time, datetime, timedelta
import time as tm
import copy

class Session:
    def __init__(self,auto=False):
        self.data_folder = "./data/"
        self.user_data_file = self.data_folder + "udata.pickle"
        
        if not os.path.isfile(self.user_data_file):
            if auto:
                print("No user profile, cannot start automatically")
                self.SeshUser = None
                return
            if not os.path.exists(self.data_folder):
                os.mkdir(self.data_folder)
            self.SeshUser = User()
            self.save()
        else:
            with open(self.user_data_file,'rb') as f:
                user = pickle.load(f)
            #self.SeshUser = User(udata)
            self.SeshUser = user
            print(f"Welcome, {self.SeshUser.name}.\n")
        return

    def start(self):
        
        print("Starting program, type CTRL-Z to exit...")
        #start program here 
        
        #make sure list is sorted
        print("Removing expired orders:")
        self.SeshUser.orders.remove_expired_orders()
        self.save()
        while True:
            if len(self.SeshUser.orders.orders) == 0:
                print("No more orders! Add one or more under 'edit'"
                        " option to start")
                return
            next_order = self.SeshUser.orders.next_order()
            next_ord_time = next_order.earliest_datetime()
            #can book area exactly 3 days in advance, get to site a minute
            #early
            next_book_time = next_ord_time - timedelta(days=3,seconds=60)
            diff = next_book_time - datetime.now()
            timestr = "".join(str(diff).split(".")[:-1])
            otimelen = 16 #max len of output time string?
            timelen = otimelen
            while diff.total_seconds() > 0:
                #not time yet, need to wait
                #show time remaining
                print(f"\rHibernating for {timestr} until next booking can be "
                        "made" + " "*(otimelen - timelen),end = "")
                sys.stdout.flush()
                tm.sleep(1.0)
                diff = next_book_time - datetime.now()
                timestr = "".join(str(diff).split(".")[:-1])
                timelen = len(timestr)
            
            print("\nAttempting to book next session...")
            
            success = book_workout.book_workout(self.SeshUser, next_order)
            
            if success:
                print(f"Booked order {next_order.id}")
                self.SeshUser.orders.remove_order(next_order.id)
            else:
                print(f"Failed to book order {next_order.id}")
                #try to push back order's first time range to next "quarter"

        return

    def edit(self):
        self.SeshUser.edit_orders()
        self.save()
        return

    def view(self):
        self.SeshUser.orders.print_orders()
        return

    def save(self):
        with open(self.user_data_file, 'wb') as f:
            pickle.dump(self.SeshUser, f)
        return

class User:
    def __init__(self, data = None):
        print("Local user data not found, please provide the following "
                "(data will only be stored locally):")
        
        self.name = input("Name: ")
        
        gend = None
        while not gend or gend not in 'mf':
            gend = input("Gender (for Women's Fitness Zone exclusion) "
                    "[male/female]: ")[0].lower()
        if gend == 'm':
            self.gender = "male"
        else:
            self.gender = "female"

        self.netid = input("Queen's NetID: ")
        
        self.password = input("Current NetID password: ")
        
        self.orders = OrderList()
        get_ord = input("Add orders [y/n]?: ")
        if get_ord[0].lower() == 'y':
            self.edit_orders()
        print("Setup successful!\n")
        return

    def edit_orders(self):
        print("\nSTARTING ORDER EDITOR\n")
        inp = None
        while not inp or inp in "adm":
            inp = input("Choose an order option [add/delete/modify/quit]: ")[0].lower()
            if inp == 'a':
                self.add_order()
            elif inp == 'd':
                self.delete_order()
            elif inp == 'm':
                self.modify_order()

        print("\nCLOSING EDITOR\n")
        return

    def add_time(self,times):
        added = False
        while not added:
            try:
                trangestr = input("Time range [??:?? ?M - ??:?? ?M]: ")
                t1, t2 = trangestr.split(' - ')
                added = times.add_range(TimeRange(t1, t2))
            except:
                print('Please enter a valid time range '
                        '(e.g. "9:00 AM - 12:00 PM")')
        return

    def remove_time(self,times):
        if len(times.time_ranges) == 0:
            print("No time ranges to remove!")
            return

        removed = False
        while not removed:
            try:
                n = int(input("Number of time range to remove: ").strip(" ."))
                removed = times.delete_range(n-1)
            except:
                print("Please enter a valid time range number")
        return

    def edit_times(self,times):
        if len(times.time_ranges) == 0:
            self.add_time(times)
        action = None
        while not action or action in "ra":
            print("\nCurrent time ranges:")
            times.print_ranges(prefix='\t',numbered=True)
            
            action = input("Select time range action [add/remove/quit]: ")[0].lower()
            if action == 'a':
                self.add_time(times)
            elif action == 'r':
                self.remove_time(times)
            else:
                if len(times.time_ranges) == 0:
                    print("Add at least one time range to quit.")
                    action = None
        return
    
    def add_area(self,areas):      
        area = input("Enter name of workout area or a search term: ")
        if len(areas) == 0:
            areas.append(area)
            return
        place = None
        while not place:
            place = input("Priority [first/last/<n>]: ").strip(" .")
            if place[0].lower() == "f":
                place = 1
            elif place[0].lower() == "l":
                place = len(areas) + 1
            else:
                try:
                    place = int(place)
                    if place < 1:
                        place = 1
                    elif place > len(areas) + 1:
                        place = len(areas) + 1
                except:
                    print('Enter a valid priority (e.g. "first", "last", "3")')
                    place = None
        areas.insert(place - 1, area)
        return

    def remove_area(self,areas):
        if len(areas) == 0:
            print("No areas to remove!")
            return
        
        removed = False
        while not removed:
            try:
                n = int(input("Priority number of area to remove: "))
                if n < 1:
                    raise ValueError
                del areas[n-1]
                removed = True
            except:
                print("Please enter a valid area priority number from above")
        return

    def edit_areas(self,areas):
        if len(areas) == 0:
            self.add_area(areas)
        action = None
        while not action or action in "ra":
            print("\nCurrent workout area search terms (in order):")
            for i in range(len(areas)):
                print(f"\t{i+1}. {areas[i]}")
            
            action = input("Select area list action [add/remove/quit]: ")[0].lower()
            if action == 'a':
                self.add_area(areas)
            elif action == 'r':
                self.remove_area(areas)
            elif len(areas) == 0:
                print("Add at least one area to quit.")
                action = None
        return

    def get_date(self):
        odate = False
        while not odate:
            try:
                datestr = input("Enter the order date [YYYY-MM-DD]: ")
                odate = date.fromisoformat(datestr)
                if odate < date.today():
                    raise ValueError
            except:
                print("Please enter a valid future date")
        return odate

    def add_order(self):
        print("\nAdding a new order")
        
        odate = self.get_date()
        otimes = TimeRangeList()
        self.edit_times(otimes)
        oalist = []
        self.edit_areas(oalist)

        #print(odate,otimes,oalist)
        
        sconf = input("Create weekly series from order [y/n]?: ")
        if sconf[0].lower() == 'y':
            #create recurring weekly series 
            s_end = False
            while not s_end:
                try:
                    datestr = input("Enter the series end date [YYYY-MM-DD]: ")
                    s_end = date.fromisoformat(datestr)
                    if s_end < odate:
                        raise ValueError
                except:
                    print("Please enter a valid date after series start")
            self.orders.add_series(odate, otimes, oalist, s_end)
        else:
            self.orders.add_order(odate, otimes, oalist)
        return
        
    def delete_order(self):
        if len(self.orders.orders) == 0:
            print("No orders to delete!")
            return
        ntype = "Order"
        self.orders.print_orders()
        do_series = input("Delete a series or single order [series/order]?: ")
        series = do_series[0].lower() == 's'
        if series:
            ntype = "Series"

        deleted = False
        while not deleted:
            try:
                nstr = input(f"{ntype} number to delete: ")
                num = int(nstr)
                if series:
                    deleted = self.orders.remove_series(num)
                else:
                    deleted = self.orders.remove_order(num)
            except:
                print(f"Please enter a valid {ntype} number from above")
        return
        
    def modify_order(self):
        if len(self.orders.orders) == 0:
            print("No orders to modify!")
            return
        self.orders.print_orders()
        order = False
        while not order:
            try:
                oid = int(input("Order number to modify: "))
                order = self.orders.get_order(oid)
            except:
                print(f"Please enter a valid order number from above")
        
        do_series = False
        if order.series:
            resp = input("Modify entire series or just this order "
                    "[series/order]?: ")
            do_series = resp[0].lower() == 's'

        if do_series:
            opts = "ta"
            options = "[times/areas]"
        else:
            opts = "dta"
            options = "[date/times/areas]"

        #get the value to modify here
        mtype = None
        while not mtype or mtype not in opts: 
            mtype = input(f"Modify what {options}?: ")[0].lower()

        if mtype == 'a':
            #modify copy then see if it works with order list 
            val = copy.deepcopy(order.areas)
            self.edit_areas(val)

        elif mtype == 't':
            val = copy.deepcopy(order.times)
            self.edit_times(val)

        else:
            val = self.get_date()

        if do_series:
            self.orders.modify_series(order.series, val)
        else:
            self.orders.modify_order(oid, val)
        return

