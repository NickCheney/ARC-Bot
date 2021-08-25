import os
import pickle
from orders import OrderList, TimeRange, TimeRangeList
from datetime import date, time, datetime

class Session:
    def __init__(self):
        self.data_folder = "./data/"
        self.user_data_file = self.data_folder + "udata.pickle"

        if not os.path.isfile(self.user_data_file):
            if not os.path.exists(self.data_folder):
                os.mkdir(self.data_folder)
            self.SeshUser = User()
            self.save()
        else:
            with open(self.user_data_file,'rb') as f:
                user = pickle.load(f)
            #self.SeshUser = User(udata)
            self.SeshUser = user
            print("Welcome, {}.".format(self.SeshUser.name))
        return

    def start(self):
        if len(self.SeshUser.orders.orders) == 0:
            print("You don't have any orders! Add one or more to get started")
            self.edit()
            return
        
        print("Starting program, type CTRL-Z to exit...")
        #start program here
        '''
        while True:
            #make sure list is sorted
            remove_obselete orders()
            not = get_next_order_time()
            while not xmin before not:
                hibernate
            attempt_to_book()
            #should refresh until desired time
            #then try and book in all areas
            print(success/failure)
            if success:
                remove order from orderlist
        '''
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
            #pickle.dump(self.SeshUser.get_data(), f)
            pickle.dump(self.SeshUser, f)
        return

class User:
    def __init__(self, data = None):
        print("Local user data not found, please provide the following "
                "(data will only be stored locally):")
        
        self.name = input("Name: ")
        
        gend = "none"
        while gend[0].lower() != 'm' and gend[0].lower() != 'f':
            gend = input("Gender (for Women's Fitness Zone exclusion) "
                    "[male/female]: ")
        if gend[0].lower() == 'm':
            self.gender = "male"
        else:
            self.gender = "female"

        self.netid = input("Queen's NetID: ")
        
        self.password = input("Current NetID password: ")
        
        self.orders = OrderList()
        get_ord = input("Add orders [y/n]?: ")
        if get_ord[0].lower() == 'y':
            self.edit_orders()
        print("Setup successful!")
        return

    def edit_orders(self):
        print("\nSTARTING ORDER EDITOR\n")
        inp = "none"
        while inp[0].lower() != 'q':
            inp = input("Choose an order option [add/delete/modify/quit]: ")
            if inp.lower()[0] == 'a':
                self.add_order()
            elif inp.lower()[0] == 'd':
                self.delete_order()
            elif inp.lower()[0] == 'm':
                self.modify_order()

        print("\nCLOSING EDITOR\n")
        return

    def add_time(times):
        added = False
        while not added:
            try:
                trangestr = input("Time range [??:?? ?M - ??:?? ?M]: ")
                t1, t2 = trangestr.split(' - ')
                added = times.add_range(TimeRange(t1, t2))
            except:
                print('Please enter a valid time range "
                        "(e.g. "9:00 AM - 12:00 PM")')
        return

    def remove_time(times):
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

    def edit_times(times):
        action = None
        while not action or action not in "ra":
            print("\n Current time ranges:")
            times.print_ranges(prefix='\t',numbered=True)
            
            action = input("Select action [add/remove/quit]: ")[0].lower()
            if action == 'a':
                self.add_time(times)
            elif action == 'r':
                self.remove_time(times)
        return
    
    def add_area(areas):      
        area = input("Enter name of workout area or a search term: ")
        place = None
        while not place:
            place = input("Priority [first/last/<n>]: ").strip(" .")
            if place[0].lower() == "f":
                place = 0
            elif place[0].lower() == "l":
                place = len(areas)
            else:
                try:
                    place = int(place)
                    if place < 0:
                        place = 0
                    elif place > len(areas):
                        place = len(areas)
                except:
                    print('Enter a valid priority (e.g. "first", "last", 3)')
                    place = None
        areas.insert(place, area)
        return

    def edit_areas(areas):
        action = None
        while not action or action not in "ra":
            print("\n Current workout area search terms (in order):")
            for i in range(len(areas)):
                print(f"\t{i}. {areas[i]}")
            
            action = input("Select action [add/remove/quit]: ")[0].lower()
            if action == 'a':
                self.add_area(areas)
            elif action == 'r':
                self.remove_area(areas)

    def get_date():
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
        otimes = self.get_times()
        oalist = self.get_areas()
        
        sconf = input("Create weekly series from order [y/n]?: ")
        if sconf[0].lower() == 'y':
            #create recurring weekly series (add option to adjust interval later)
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
        ntype = "Order"
        self.orders.print_orders()
        do_series = input("Delete a series or single order [series/order]?: ")
        series = do_series[0].lower() == 's'
        if series:
            ntype = "Series"
        num = False
        while not num:
            try:
                nstr = input("{} number to delete: ".format(ntype))
                num = int(nstr)
            except:
                print("Please enter a valid {} number from above".format(ntype))
        if series:
            self.orders.remove_series(num)
        else:
            self.orders.remove_order(num)
        
    def modify_order(self):
        self.orders.print_orders()
        do_series = input("Modify a series or single order [series/order]?: ")
        series = do_series[0].lower() == 's'
        if series:
            ntype = "Series"
        else:
            ntype = "Order"
        num = False
        while not num:
            try:
                nstr = input("{} number to delete: ".format(ntype))
                num = int(nstr)
            except:
                print("Please enter a valid {} number from above".format(ntype))

        #get the value to modify here
        mtype = None
        while not mtype or mtype not in 'dta':
            mtype = input("Modify what [date/times/areas]?: ")[0].lower()

        if mtype == 'a':
            pass
        elif mtype == 'd':
            pass
        else:
            pass

        if series:
            self.orders.modify_series(num, val = None)
        else:
            self.orders.modify_order(num, val = None)
        self.orders.print_orders()

    #def get_data(self):
    #    return vars(self)
