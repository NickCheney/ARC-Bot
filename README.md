# ARC-Bot
Automated Gym Session Booking for Queen's University Athletics and Recreation Centre (ARC). Uses Selenium to interact with the reservation website https://getactive.gogaelsgo.com/ and schedule the user's requested gym sessions when available. 

All reservations are currently categorized by the gym area name and equipment available, together know as the category (e.g. *"LL1 Lifting Zone - Squat Racks"*, *"L2 Cardio Zone 1 - Treadmills"*). Gym sessions are currently 1 hour in length and can be booked starting exactly 3 days prior.

## Installation
### Prerequisites
You must have the chromedriver executable installed and on `$PATH` in order for the program to run. Find the correct version for your Chrome here: https://chromedriver.chromium.org/downloads

To verify, type `chromedriver` and you should see something like the following:
```
Starting ChromeDriver 92.0.4515.107 (87a818b10553a07434ea9e2b6dccf3cbe7895134-refs/branch-heads/4515@{#1634}) on port 9515
Only local connections are allowed.
Please see https://chromedriver.chromium.org/security-considerations for suggestions on keeping ChromeDriver safe.
ChromeDriver was started successfully.
```
### **Linux**
First, ensure X virtual frame buffer is installed with:
```
sudo apt-get install xvfb
```
Then find the latest version under releases and download. Currently the only architecture supported is x86_64 but arm executables will be available soon. Run `./arcbot` from the installation directory or add to `$PATH` for easy access. Alternatively, you can fork and clone the repo to run the program in your own python environment. To ensure you have all the requirements
### **Windows**
Coming soon...
## Usage
The program is currently implemented as a text-based terminal tool, with the potential for a GUI based application in the future. Prompt options are given in brackets and can be selected with the full option name or the first character:
```
select option [first/second]: f
first option selected!
```
### Standard
Start the program with: `./arcbot` from the installation directory or `arcbot` if it is in `$PATH`
You will be prompted to enter user information:
```
$./arcbot
Local user data not found, please provide the following (data will only be stored locally):
Name: Nick
Gender (for Women's Fitness Zone exclusion) [male/female]: m
Queen's NetID: 12ABC3
Current NetID password: 123password
Setup successful!
```
You will then be prompted to edit your orders. You must have at least one to start the program. You can later remove or modify existing orders:
```
Add some orders to get started!

STARTING ORDER EDITOR

Choose an order option [add/delete/modify/quit]: 
```
After qutting the order editor you will see the main menu from where you can start the program, edit your orders again, view your orders or quit. This will be the default entry point after your first usage without automatic start set. Once you have added at least one order, the program can be started:
```
Select an option [start/edit/view/quit]: s
Starting program, type CTRL-Z to exit...
```
### Automatic
After inital user setup, the program can be automatically started without need for user interaction using the `-s` or `--start` arguments and will run until no orders remain:
```
$./arcbot -s
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
To start the program automatically on boot up, add the path to `arcbot` to your `$PATH` variable and edit `~/.bashrc` to include `arcbot -s > acbot-log.txt`. Check program output anytime with `cat ~/arcbot-log.txt`
