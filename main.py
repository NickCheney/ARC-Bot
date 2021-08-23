"""
Main entry point for program event loop
"""
from book_workout import book_workout
#from datetime import date, time
from user import Session
def main():

    #rtypes = ['Squat Racks', 'Free Weights']
    #excl = ["Women's Fitness Zone"]
    #day = date(2021,8,8)
    #tm = [(time(17,0),time(22,0))]

    #book_workout(rtypes, excl, day, tm)
    session = Session()

    action = 's'
    while action[0].lower() != 'q':
        action = input("Select an option [start/edit/quit]: ")
        if action[0].lower() == 's':
            session.start()
        elif action[0].lower() == 'e':
            session.edit()
        
    print("Saving data and exiting")
    session.save()

    return

if __name__ == "__main__":
    main()
