import os
import pickle

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
        while imp.lower() != 'q' and imp.lower() != "quit":
            inp = input("Type a command [add/delete/modify/quit]: ")
            if inp.lower() == 'a' or imp.lower() == 'add':
                #DEFINE A CLASS FUNCTION FOR THIS
        return
    def get_data(self):
        data = {"name" : self.name,
                "netid": self.netid,
                "password": self.password,
                "orders": self.orders,
                "settings": self.settings}
        return data



            
            
