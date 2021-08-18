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
            self.netid = input("Current NetID password: ")
            s_mode = None
            while s_mode != "default" and s_mode != "custom":
                s_mode = input('User settings (enter "default" or "custom"): ')
            self.settings = self.get_settings(s_mode)
            self.orders = self.get_orders()
            print("Setup successful. Starting program")
    def get_settings(self, mode):
        return {}
    def get_orders(self):
        return []
    def get_data(self):
        data = {"name" : self.name,
                "netid": self.netid,
                "password": self.password,
                "orders": self.orders,
                "settings": self.settings}
        return data



            
            
