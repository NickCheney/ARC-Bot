import os
import pickle
from orders import RequestedOrder, TimeRange, TimeRangeList
from datetime import date, time, datetime

class Session:
    def __init__(self):
        self.data_folder = "./data/"
        self.user_data_file = self.data_folder + "udata.pickle"

        if not os.path.isfile(self.user_data_file):
            if not os.path.exists(self.data_folder):
                os.mkdir(self.data_folder)
            self.SeshUser = User()
        else:
            with open(self.user_data_file,'rb') as f:
                udata = pickle.load(f)
            self.SeshUser = User(udata)
    
    def start(self):
        if len(self.SeshUser.orders) == 0:
            print("You don't have any orders! Create some to get started")
            self.SeshUser.get_orders()
            self.save()
        
        print("Starting program, type CTRL-Z to exit...")
        #start program here
    def edit(self):
        pass
    def save(self):
        with open(self.user_data_file, 'wb') as f:
            pickle.dump(self.SeshUser.get_data(), f)


class User:
    def __init__(self, data = None):
        if data:
            self.netid = data['netid']
            self.password = data['password']
            self.orders = data['orders']
            self.name = data['name']
            self.settings = data['settings']
            self.next_order_id = 0
            print("Welcome, {}. Starting program".format(self.name))
        else:
            print("Local user data not found, please provide the following (data will only be stored locally):")
            self.name = input("Name: ")
            self.netid = input("Queen's NetID: ")
            self.password = input("Current NetID password: ")
            s_mode = "N"
            while s_mode[0].lower() != "d" and s_mode[0].lower() != "c":
                s_mode = input('User settings [default/custom]: ')
            self.settings = self.get_settings(s_mode)
            self.orders = []
            get_ord = input("Add orders [y/n]?: ")
            if get_ord[0].lower() == 'y':
                self.get_orders()
            print("Setup successful!")
    def get_settings(self, mode):
        descriptions = {
                "Booking frequency:" : {
                    "minimal" : "waits until 1 minute before the next requested order to browse the site",
                    "periodic" : "attempts to fulfil any eligible requested orders every 5 minutes"
                    },
                "Area search type:" : {
                    "string" : "searches for workout areas containing a user provided string",
                    "specified" : "user specifies the exact name(s) of the desired workout areas"
                    }
                }

        settings = {}
        if mode[0].lower() == "d":
            for setting in descriptions.keys():
                settings[setting] = list(descriptions[setting].keys())[0]
            return settings

        print("\nSETTINGS\n")
        for setting in descriptions.keys():
            print(setting)
            for val in descriptions[setting].keys():
                print('\t',val,'-',descriptions[setting][val])
            print()
        
        for setting in descriptions.keys():
            options = descriptions[setting].keys()
            choice = None
            while choice not in options:
                choice = input("{0} [{1}]: ".format(setting, "/".join(options)))
            settings[setting] = choice
        return settings


    def get_orders(self):
        print("\nORDER INITIALIZATION\n")
        inp = "none"
        while inp.lower() != 'q' and inp.lower() != "quit":
            inp = input("Choose an order option [add/delete/modify/quit]: ")
            if inp.lower()[0] == 'a':
                self.add_order()
            elif inp.lower()[0] == 'd':
                self.delete_order()
            elif inp.lower()[0] == 'm':
                self.modify_order()

        return

    def add_order(self):
        print("\nAdding a new order")
        
        odate = False
        while not odate:
            try:
                datestr = input("Enter the order date [YYYY-MM-DD]: ")
                odate = date.fromisoformat(datestr)
                if odate < date.today():
                    raise ValueError
            except:
                print("Please enter a valid future date")
        doneTimes = False
        otimes = TimeRangeList()
        cont = 'y'
        while cont[0].lower() == 'y':
            try:
                trangestr = input("Time range [??:?? ?M - ??:?? ?M]:")
                t1, t2 = trangestr.split(' - ')
                trange = TimeRange(t1, t2)

                otimes.add_range(trange)
                
                print("\nCurrent time ranges:")
                otimes.print_ranges(prefix = "\t")

                cont = input("Add another time range [y/n]?: ")

            except:
                print("Please enter a valid time range without conflicts")

        atype = self.settings["Area search type:"]
        oalist = []
        
        if atype == "specified":
            prompt = 'Name of preferred workout area '
            +'(e.g. "L2 Cardio Zone 1 - Treadmills")'
        else:
            prompt = 'Preferred workout area query (e.g. "Squat Rack"): '
        
        cont = 'y'
        while cont[0].lower() == 'y':
            a1 = input(prompt)
            oalist.append(a1)
            cont = input("Add another area [y/n]?: ")
        
        oidn = self.next_order_id
        
        sconf = input("Create weekly series from order? [y/n]?: ")
        
        #add checking for conflicts with other orders
        if sconf[0].lower() == 'y':
            print("Series not supported yet")            
            #Create a series of orders starting with this one here until a specified date
        else:
            newOrder = RequestedOrder(odate, otimes, oalist, oidn)
            self.orders.append(newOrder)
        print("Order successfully added!")
        self.next_order_id += 1
        return
        
    def delete_order(self):
        pass
    def modify_order(self):
        pass


    def get_data(self):
        return vars(self)



            
            
