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

    action = 's'
    while action[0].lower() != 'q':
        action = input("Select an option [start/edit/view/quit]: ")
        if action[0].lower() == 's':
            session.start()
        elif action[0].lower() == 'e':
            session.edit()
        elif action[0].lower() == 'v':
            session.view()
        
    print("Saving data and exiting")
    session.save()

    return

if __name__ == "__main__":
    main()
