import random
import sqlite3
import threading
import tkinter
from tkinter import simpledialog, messagebox
import names


class LaboratoryApp:
    def __init__(self):
        self.selected_item_index = None
        self.temperature = 22.1
        self.staff = []
        self.create_main_window()


    def update_labels(self, temp_label, staff_label):
        temp_label.config(text=f"Temperatura: {self.temperature}\N{DEGREE SIGN}C")

        staff_label.config(text=f"Liczba pracowników: {len(self.staff)}")

        self.window.after(1000, lambda: self.update_labels(temp_label, staff_label))



    def on_select(self, event):
        widget = event.widget
        current_selection = widget.curselection()

        if current_selection:
            current_index = current_selection[0]
            if self.selected_item_index == current_index:
                widget.selection_clear(current_index)
                self.selected_item_index = None
            else:
                self.selected_item_index = current_index
        else:
            widget.selection_clear(0, tkinter.END)
            self.selected_item_index = None

        self.delete_button["state"] = "normal" if self.selected_item_index is not None else "disabled"

    def add_item(self):
        item_name = simpledialog.askstring("Dodaj przedmiot", "Podaj nazwę przedmiotu:")

        while item_name:
            item_temp_min = simpledialog.askfloat("Dodaj przedmiot", "Podaj temperaturę minimalną:")

            while item_temp_min is not None:
                item_temp_max = simpledialog.askfloat("Dodaj przedmiot", "Podaj temperaturę maksymalną:")

                while item_temp_max is not None:
                    if item_temp_max >= item_temp_min:
                        connection = sqlite3.connect("items.db")
                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO items (name, temp_min, temp_max) VALUES (?, ?, ?)",
                                       (item_name, item_temp_min, item_temp_max))
                        connection.commit()
                        connection.close()

                        self.display_items_list()
                        return
                    else:
                        messagebox.showwarning("Błąd", "Temperatura maksymalna nie może być mniejsza niż minimalna.")
                        item_temp_max = simpledialog.askfloat("Dodaj przedmiot", "Podaj temperaturę maksymalną:")

                item_temp_min = simpledialog.askfloat("Dodaj przedmiot", "Podaj temperaturę minimalną:")

            item_name = simpledialog.askstring("Dodaj przedmiot", "Podaj nazwę przedmiotu:")

    def delete_selected_item(self):
        if self.selected_item_index is not None:
            selected_item = self.listbox.get(self.selected_item_index)
            obj_id = selected_item.split(':')[0]
            confirmed = messagebox.askyesno("Potwierdź", "Czy na pewno chcesz usunąć zaznaczony przedmiot?")
            if confirmed:
                connection = sqlite3.connect("items.db")
                cursor = connection.cursor()
                cursor.execute("DELETE FROM items WHERE id=?", (obj_id,))
                connection.commit()
                connection.close()

                self.selected_item_index = None
                self.display_items_list()

    def display_items_list(self):
        connection = sqlite3.connect("items.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        connection.close()

        self.listbox.delete(0, tkinter.END)

        for i, item in enumerate(items):
            temp_min, temp_max = item[2], item[3]
            formatted_item = f"{item[0]}: {item[1]} \t {temp_min} - {temp_max} \N{DEGREE SIGN}C"
            if temp_min <= self.temperature <= temp_max:
                self.listbox.insert(tkinter.END, formatted_item)
            else:
                self.listbox.insert(tkinter.END, formatted_item)
                self.listbox.itemconfig(tkinter.END, {'fg': 'red'})
            if self.selected_item_index is not None and self.selected_item_index == i:
                self.listbox.selection_set(i)

        self.window.after(1000, self.display_items_list)

    def display_staff_list(self):
        staff_list = "\n".join(self.staff)
        staff_dialog = tkinter.Toplevel(self.window)
        staff_dialog.title("Lista Pracowników")

        staff_label = tkinter.Label(staff_dialog, text=staff_list)
        staff_label.pack()

    def create_main_window(self):
        self.window = tkinter.Tk()
        self.window.geometry("400x300")
        self.window.title("Laboratorium")
        temp_label = tkinter.Label(self.window, text="")
        staff_label = tkinter.Label(self.window, text="")
        staff_button = tkinter.Button(self.window, text="Pracownicy", command=self.display_staff_list)

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

        self.listbox = tkinter.Listbox(self.window, activestyle='none', bg='lightblue')
        self.listbox.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.add_button = tkinter.Button(self.window, text="Dodaj przedmiot", command=self.add_item)
        self.add_button.grid(row=2, column=0, columnspan=2)

        self.delete_button = tkinter.Button(self.window, text="Usuń przedmiot", command=self.delete_selected_item,
                                            state="disabled")
        self.delete_button.grid(row=3, column=0, columnspan=2)

        temp_label.grid(row=1, column=0, columnspan=2)

        staff_label.grid(row=4, column=0, sticky="e")
        staff_button.grid(row=4, column=1, sticky="w")


        self.update_labels(temp_label, staff_label)
        self.display_items_list()

        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.window.mainloop()

if __name__ == "__main__":
    app = LaboratoryApp()
    # gui_thread = threading.Thread(target=app.window.mainloop)
    # gui_thread.start()