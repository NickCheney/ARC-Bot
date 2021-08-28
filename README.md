# ARC-Bot
Automated Gym Session Booking for Queen's University Athletics and Recreation Centre (ARC). Uses Selenium to interact with the reservation website https://getactive.gogaelsgo.com/ and schedule the user's requested gym sessions when available. 

All reservations are currently categorized by the gym area name and equipment available, together know as the category (e.g. *"LL1 Lifting Zone - Squat Racks"*, *"L2 Cardio Zone 1 - Treadmills"*). Gym sessions are currently 1 hour in length and can be booked starting exactly 3 days prior.

## Installation
### **Linux**
### **Windows**
## Usage
The program is currently implemented as a text-based terminal tool, with the potential for a GUI based application in the future. Prompt options are given in brackets and can be selected with the full option name or the first character:
```
select option [first/second]: f
first option selected!
```
### Standard
Start the program with: `python main.py`
You will be prompted to enter user information and can choose to add inital orders or not:
```
Local user data not found, please provide the following (data will only be stored locally):
Name: Nick
Gender (for Women's Fitness Zone exclusion) [male/female]: m
Queen's NetID: 12ABC3
Current NetID password: 123password
Add orders [y/n]?: n
Setup successful!
```
You will then reach the main menu from where you can start the program, edit (add/remove/modify) your orders, view your orders or quit. This will be the default entry point after your first usage. Once you have added at least one order, the program can be started:
```
Select an option [start/edit/view/quit]: s
Starting program, type CTRL-Z to exit...
```
### Automatic
After inital user setup, the program can be automatically started without need for user interaction using the `-s` or `--start` arguments and will run until no orders remain:
```
$python main.py -s
Welcome, Nick

Starting program, type CTRL-Z to exit...
Removing expired orders:
None found
Hibernating for 17:46:46 until next booking can be made
```
The following line can be used to run the program in the background in linux without terminal output (add `nohup` if accessing remotely):
```
$python main.py -s > log.txt &
$
```
