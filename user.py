import os
import pickle
from order import RequestedOrder

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
            self.get_orders()
            print("Setup successful. Starting program")
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
                odate = date.fromisoformat(input("Enter the order date [YYYY-MM-DD]: "))
                if odate < date.today():
                    raise ValueError
            except:
                print("Please enter a valid future date")
        doneTimes = False
        otimes = TimeRangeList()
        while not doneTimes:
            try:
                trangestr = input("Time range [??:?? ?M - ??:?? ?M]:")
                t1, t2 = trangestr.split(' - ')
                trange = TimeRange(t1, t2)

                
                    for otrange in otimes:
                        if trange.conflicts_with(otrange):
        
                otimes.append((t1, t2))
                otimes.sort(lambda x: x[0])
                
                print("\nCurrent time ranges:")
                for ot1, ot2 in otimes:
                    t1str = ot1.strftime("%I:%M %p")
                    t2str = ot2.strftime("%I:%M %p")
                    print("\t{0} - {1}".format(t1str,t2str))

                cont = input("Add another time range [y/n]?: ")
                if cont[0].lower() != 'y':
                    doneTimes = False
                else:
                    doneTimes = True
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
        
        oidn = self.get_next_id()
        
        sconf = input("Create weekly series from order? [y/n]?: ")
        
        #add checking for conflicts with other orders
        if sconf[0].lower() == 'y':
            
            #Create a series of orders starting with this one here until a specified date
        else:
            newOrder = RequestedOrder(odate, otimes, oalist, oidn)
            self.orders.append(newOrder)
        print("Order successfully added!")
        return
        
    def delete_order(self):
        pass
    def modify_order(self):
        pass


    def get_data(self):
        return vars(self)



            
            
