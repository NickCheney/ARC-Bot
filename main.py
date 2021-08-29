"""
Main entry point for program event loop
"""
import sys
from book_workout import book_workout
from user import Session
def main():
    args = sys.argv[1:]
    if "-s" in args or "--s" in args:
        #start automatically
        session = Session(auto=True)
        if session.SeshUser:
            session.start()
        return
    session = Session()
    user = session.SeshUser
    opts = ["start","edit","view","quit"]
    action = True
    while action:
        action = user.input("Select an option",opts,True)
        if action == 's':
            session.start()
        elif action == 'e':
            session.edit()
        elif action == 'v':
            session.view()
        
    print("Saving and exiting")
    session.save()

    return

if __name__ == "__main__":
    main()
