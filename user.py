from orders import OrderList
from time_ranges import TimeRange, TimeRangeList
from datetime import date, time, datetime, timedelta
import time as tm
import copy

class User:
    def __init__(self, data = None):
        print("Local user data not found, please provide the following "
                "(data will only be stored locally):")
        
        self.name = self.input("Name",quit=False)
        
        self.gender = self.get_gender()

        self.username = self.input("Queen's NetID",quit=False)
        
        self.password = self.input("Current NetID password",quit=False)
        
        self.orders = OrderList()
        
        print("Setup successful!\n")
        return

    def get_gender(self):
        prompt = "Gender (for Women's Fitness Zone exclusion)"
        gend = self.input(prompt,["male","female"],False)

        if gend == 'm':
            return "male"
        return "female"

    def input(self, text, options = None, quit = True):
        if options:
            text += ' [' + '/'.join(options) + ']'
            req = "".join([o[0] for o in options])
            if quit:
                req += 'q'
        text += ': '
        
        resp = None
        while not resp or (options and not resp in req):
            resp = input(text)
            if resp == '':
                resp = None
            elif options:
                resp = resp[0].lower()
        if quit and resp == 'q' or resp == 'quit':
            #flag to quit current section of program
            return None
        return resp
    
    def edit(self):
        what = self.input("Edit what",["user","orders"])
        if not what:
            print("Quitting edit mode")
            return
        if what == 'o':
            self.edit_orders()
        else:
            self.edit_info()
        return

    def edit_info(self):
        opts = ["name","gender","username","password"]
        field = self.input("Edit what",opts)
        
        if not field:
            print("Quitting user info editor")
            return

        if field == 'n':
            self.name = self.input("Name",quit=False)
        elif field == 'g':
            self.gender = self.get_gender()
        elif field == 'u':
            self.username = self.input("Queen's NetID",quit=False)
        else:
            self.password = self.input("Current NetID password",quit=False)
        return

    def edit_orders(self):
        print("\nSTARTING ORDER EDITOR\n")
        opts = ["add","delete","modify","quit"]
        inp = True
        while inp:
            inp = self.input("Choose an order option",opts)
            if inp == 'a':
                self.add_order()
            elif inp == 'd':
                self.delete_order()
            elif inp == 'm':
                self.modify_order()

        print("\nQUITTING ORDER EDITOR\n")
        return

    def add_time(self,times):
        added = False
        while not added:
            try:
                trangestr = self.input("Time range [??:?? ?M - ??:?? ?M]: ")
                if not trangestr:
                    print("Aborting time range addition")
                    return
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
                num = self.input("Number of time range to remove")
                if not num:
                    print("Aborting time range removal")
                    return
                n = int(num.strip(" ."))
                removed = times.delete_range(n-1)
            except:
                print("Please enter a valid time range number")
        return

    def edit_times(self,times):
        if len(times.time_ranges) == 0:
            self.add_time(times)
        action = True
        while action:
            print("\nCurrent time ranges:")
            times.print_ranges(prefix='\t',numbered=True)
            
            opts = ["add","remove","quit"]
            action = self.input("Select time range action",opts)
            if action == 'a':
                self.add_time(times)
            elif action == 'r':
                self.remove_time(times)
        return
    
    def add_area(self,areas):      
        area = self.input("Enter name of workout area or a search term")
        if not area:
            print("Aborting area addition")
            return
        if len(areas) == 0:
            areas.append(area)
            return

        opts = ["first","last","<n>"]
        valid = False
        while not valid:
            placestr = self.input("Priority",opts)
            if not placestr:
                print("Aborting area addition")
                return
            place = placestr.strip(" .")
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
                    continue
            valid = True

        areas.insert(place - 1, area)
        return
    
    def remove_area(self,areas):
        if len(areas) == 0:
            print("No areas to remove!")
            return
        
        removed = False
        while not removed:
            try:
                num = self.input("Priority number of area to remove: ")
                if not num:
                    print("Aborting area removal")
                    return
                n = int(num)
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
        opts = ["add","remove","quit"]
        action = True
        while action:
            print("\nCurrent workout area search terms (in order):")
            for i in range(len(areas)):
                print(f"\t{i+1}. {areas[i]}")
            
            action = self.input("Select area list action",opts)
            if action == 'a':
                self.add_area(areas)
            elif action == 'r':
                self.remove_area(areas)
        return

    def get_date(self,dtype = "order"):
        odate = False
        while not odate:
            try:
                datestr = self.input(f"Enter the {dtype} date [YYYY-MM-DD]")
                if not datestr:
                    print("Aborting date input")
                    return None
                odate = date.fromisoformat(datestr)
                if odate < date.today():
                    raise ValueError
            except:
                print("Please enter a valid future date")
        return odate

    def add_order(self):
        print("\nAdding a new order")
        
        odate = self.get_date()
        if not odate:
            print("No date, aborting order addition")
            return
        otimes = TimeRangeList()
        self.edit_times(otimes)
        if len(otimes.time_ranges) == 0:
            print("No times, aborting order addition")
            return
        oalist = []
        self.edit_areas(oalist)
        if len(oalist) == 0:
            print("No areas, aborting order addition")
            return

        sconf = self.input("Create weekly series from order", ['y','n'])
        if not sconf:
            print("Aborting order addition")
            return
        elif sconf == 'y':
            #create recurring weekly series 
            s_end = False
            while not s_end:
                try:
                    oedate = self.get_date("series end")
                    if not oedate:
                        print("No date, aborting order addition")
                        return
                    if oedate < odate:
                        raise ValueError
                    s_end = True
                except:
                    print("Please enter a date after series start")
            self.orders.add_series(odate, otimes, oalist, oedate)
        else:
            self.orders.add_order(odate, otimes, oalist)
        return
        
    def delete_order(self):
        if len(self.orders.orders) == 0:
            print("No orders to delete!")
            return
        ntype = "Order"
        self.orders.print_orders()
        do_series = self.input("Delete a series or single order?",["series","order"])
        if not do_series:
            print("Aborting order deletion")
            return
        series = do_series == 's'
        if series:
            ntype = "Series"

        deleted = False
        while not deleted:
            try:
                nstr = self.input(f"{ntype} number to delete")
                if not nstr:
                    print("Aborting order deletion")
                    return
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
                oistr = self.input("Order number to modify")
                if not oistr:
                    print("Aborting order modification")
                    return
                oid = int(oistr)
                order = self.orders.get_order(oid)
            except:
                print(f"Please enter a valid order number from above")
        
        do_series = False
        if order.series:
            resp = self.input("Modify entire series or just this order?",
                    ["series","order"])
            if not resp:
                print("Aborting order modification")
                return
            do_series = resp == 's'

        if do_series:
            options = "[times/areas]"
        else:
            options = "[date/times/areas]"

        #get the value to modify here
        mtype = self.input("Modify what?",options)
        if not mtype:
            print("Aborting order modification")
            return
        elif mtype == 'a':
            #modify copy then see if it works with order list 
            val = copy.deepcopy(order.areas)
            self.edit_areas(val)
            if len(val) == 0:
                print("No areas, aborting order modification")
                return

        elif mtype == 't':
            val = copy.deepcopy(order.times)
            self.edit_times(val)
            if len(val.time_ranges) == 0:
                print("No times, aborting order modification")
                return

        else:
            val = self.get_date()
            if not val:
                print("No date, aborting order modification")
                return

        if do_series:
            self.orders.modify_series(order.series, val)
        else:
            self.orders.modify_order(oid, val)
        return

