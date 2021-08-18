"""
Main entry point for program event loop
"""

from book_workout import book_workout
from datetime import date, time

def main():
    rtypes = ['Squat Racks', 'Free Weights']
    excl = ["Women's Fitness Zone"]
    day = date(2021,8,8)
    tm = [(time(17,0),time(22,0))]

    book_workout(rtypes, excl, day, tm)

    return

if __name__ == "__main__":
    main()
