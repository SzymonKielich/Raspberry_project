# This is a sample Python script.
import sqlite3
from time import sleep

from LaboratoryApp import LaboratoryApp


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Aaaaa")
    gui = LaboratoryApp()
    gui.temperature = 30

    print(gui.temperature)
    gui.staff.append("kaczor")
    sleep(5)
    gui.temperature = 40
    gui.staff.append("kaczorek")
    gui.staff.remove("kaczor")
    sleep(5)
    gui.temperature = 21
    gui.staff.remove("kaczorek")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
