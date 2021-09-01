import os
import sys
import pickle
from user import User
import book_workout
from datetime import date, time, datetime, timedelta
import time as tm

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
            print("Add some orders to get started!")
            self.SeshUser.edit_orders()
        else:
            with open(self.user_data_file,'rb') as f:
                user = pickle.load(f)
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
                pushed_range = next_order.times.push_range(0)
                if pushed_range:
                    print("Pushing up order start time and retrying")
                    continue
                
                #pushing range failed, so delete it
                next_order.times.delete_range(0)
                #check if any ranges left
                if len(next_order.times.time_ranges) == 0:
                    #order can't be completed, so delete
                    print(f"Could not book order {next_order.id}, removing")
                    self.SeshUser.orders.remove_order(next_order.id)
                    #order removed so no sorting required
                else:
                    #range is gone, resort orders and try again
                    self.SeshUser.orders.sort_orders()

        return

    def edit(self):
        self.SeshUser.edit()
        self.save()
        return

    def view(self):
        self.SeshUser.orders.print_orders()
        return

    def save(self):
        with open(self.user_data_file, 'wb') as f:
            pickle.dump(self.SeshUser, f)
        return
