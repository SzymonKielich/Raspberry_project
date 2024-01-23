import sqlite3
import tkinter
from datetime import datetime

def update_time_label(label):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label.config(text=current_time)
    window.after(1000, update_time_label, label)  # Wywołaj samą siebie co 1000 ms (1 sekunda)

def display_items_list(listbox):
    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name FROM items_log")
    items = cursor.fetchall()
    connection.close()

    listbox.delete(0, tkinter.END)  # Wyczyść aktualne elementy w liście

    for item in items:
        listbox.insert(tkinter.END, f"{item[0]}: {item[1]}")

    window.after(5000, lambda: display_items_list(listbox))  # Aktualizuj listę co 5000 ms (5 sekund)

def create_main_window():
    global window  # Aby można było korzystać ze zmiennej globalnej window
    window = tkinter.Tk()
    window.geometry("400x250")
    window.title("RECEIVER")
    label = tkinter.Label(window, text="")
    exit_button = tkinter.Button(window, text="Stop", command=window.quit)

    listbox = tkinter.Listbox(window)
    listbox.pack(expand=True, fill="both")

    label.pack()
    exit_button.pack(side="right")

    update_time_label(label)  # Rozpocznij aktualizację godziny
    display_items_list(listbox)  # Wyświetl listę przedmiotów

    window.mainloop()


if __name__ == "__main__":
    create_main_window()