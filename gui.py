import random
import sqlite3
import tkinter
from datetime import datetime
from tkinter import simpledialog, messagebox

selected_item_index = None
temperature = 22
staff = 0

def update_labels(temp_label, staff_label):
    global temperature
    temperature = random.randrange(20, 24)
    temp_label.config(text=f"Temperatura: {temperature}\N{DEGREE SIGN}C")

    global staff
    rand = random.randrange(0, 4)
    if rand == 0: staff += 1
    elif rand == 1 and staff != 0: staff -= 1
    staff_label.config(text=f"Liczba pracowników: {staff}")

    window.after(1000, update_labels, temp_label, staff_label)

def on_select(event):
    global selected_item_index
    widget = event.widget
    current_selection = widget.curselection()

    if current_selection:
        current_index = current_selection[0]
        if selected_item_index == current_index:
            widget.selection_clear(current_index)
            selected_item_index = None
        else:
            selected_item_index = current_index
    else:
        widget.selection_clear(0, tkinter.END)
        selected_item_index = None

    delete_button["state"] = "normal" if selected_item_index is not None else "disabled"

def add_item():
    global window
    item_name = simpledialog.askstring("Dodaj przedmiot", "Podaj nazwę przedmiotu:")
    if item_name:
        item_temp_min = simpledialog.askfloat("Dodaj przedmiot", "Podaj temperaturę minimalną:")
        if item_temp_min:
            item_temp_max = simpledialog.askfloat("Dodaj przedmiot", "Podaj temperaturę maksymalną:")
            if item_temp_max:
                connection = sqlite3.connect("items.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO items (name, temp_min, temp_max) VALUES (?, ?, ?)",
                               (item_name, item_temp_min, item_temp_max))
                connection.commit()
                connection.close()

                # Odśwież listę po dodaniu nowego przedmiotu
                display_items_list(listbox)

def delete_selected_item():
    global selected_item_index
    if selected_item_index is not None:
        selected_item = listbox.get(selected_item_index)
        obj_id = selected_item.split(':')[0]
        confirmed = messagebox.askyesno("Potwierdź", "Czy na pewno chcesz usunąć zaznaczony przedmiot?")
        if confirmed:
            connection = sqlite3.connect("items.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM items WHERE id=?", (obj_id,))
            connection.commit()
            connection.close()

            # Zresetuj zaznaczenie po usunięciu
            selected_item_index = None

            # Odśwież listę po usunięciu przedmiotu
            display_items_list(listbox)

def display_items_list(listbox):

    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    connection.close()

    listbox.delete(0, tkinter.END)  # Wyczyść aktualne elementy w liście

    for i, item in enumerate(items):
        temp_min, temp_max = item[2], item[3]
        formatted_item = f"{item[0]}: {item[1]} \t {temp_min} - {temp_max} \N{DEGREE SIGN}C"

        # Sprawdź, czy przedmiot mieści się w przedziale aktualnej temperatury
        if temp_min <= temperature <= temp_max:
            listbox.insert(tkinter.END, formatted_item)
        else:
            # Jeżeli przedmiot nie mieści się w przedziale, koloruj na czerwono
            listbox.insert(tkinter.END, formatted_item)
            listbox.itemconfig(tkinter.END, {'fg': 'red'})

        # Jeżeli to jest zaznaczony element, ponownie zaznacz go po odświeżeniu listy
        if selected_item_index is not None and selected_item_index == i:
            listbox.selection_set(i)

    window.after(1000, lambda: display_items_list(listbox))

def create_main_window():
    global window  # Aby można było korzystać ze zmiennej globalnej window
    window = tkinter.Tk()
    window.geometry("400x300")
    window.title("Laboratorium")
    temp_label = tkinter.Label(window, text="")
    staff_label = tkinter.Label(window, text="")

    global listbox
    listbox = tkinter.Listbox(window, activestyle='none', bg='lightblue')
    listbox.pack(expand=True, fill="both")

    add_button = tkinter.Button(window, text="Dodaj", command=add_item)
    add_button.pack(side="bottom")

    global delete_button
    delete_button = tkinter.Button(window, text="Usuń", command=delete_selected_item, state="disabled")
    delete_button.pack(side="bottom")

    temp_label.pack()
    staff_label.pack()

    update_labels(temp_label, staff_label)  # Rozpocznij aktualizację godziny
    display_items_list(listbox)  # Wyświetl listę przedmiotów

    listbox.bind('<<ListboxSelect>>', on_select)

    window.mainloop()


if __name__ == "__main__":
    create_main_window()
