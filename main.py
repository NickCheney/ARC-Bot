"""
Main entry point for program event loop
"""
import sys
from book_workout import book_workout
from session import Session

def main():
    args = sys.argv[1:]
    if "-s" in args or "--s" in args:
        #start automatically
        sesh = Session(auto=True)
        if sesh.SeshUser:
            sesh.start()
        return
    sesh = Session()
    user = sesh.SeshUser
    opts = ["start","edit","view","quit"]
    action = True
    while action:
        action = user.input("Select an option",opts,True)
        if action == 's':
            sesh.start()
        elif action == 'e':
            sesh.edit()
        elif action == 'v':
            sesh.view()
        
    print("Saving and exiting")
    sesh.save()

    return

if __name__ == "__main__":
    main()
