from tkinter import *

search_frame_visible = False
ITEMS_PER_PAGE = 8
current_page = 1

#------------------------------------------------------------------------------
#открывание и закрывание холодильника
def change_image():
  global current_image, search_frame_visible
  if current_image == image1:
    label.config(image=image2)
    current_image = image2
    btn1.config(text="Закрыть")
    toggle_search_frame(True)
  else:
    label.config(image=image1)
    current_image = image1
    btn1.config(text="Открыть")
    toggle_search_frame(False)

#------------------------------------------------------------------------------
#появление и исчезновение списка
def toggle_search_frame(visible):
  search_frame_visible = visible
  if visible:
    search_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=15)
  else:
    search_frame.grid_forget()

#------------------------------------------------------------------------------
def search_listbox(event=None):
  search_term = search_entry.get().lower()
  update_listbox(search_term)

#------------------------------------------------------------------------------
#удаление продуктов из списка
def update_quantity(item, amount):
  item_quantities[item] += amount
  if item_quantities[item] <= 0:
    del item_quantities[item]
  update_listbox()

#------------------------------------------------------------------------------
#добавление продуктов
def add_item():
  new_item = new_item_entry.get()
  if new_item:
    if new_item in item_quantities:
      messagebox.showwarning("Ошибка", "Этот продукт уже существует!")
    else:
      item_quantities[new_item] = 0
      update_listbox()
      new_item_entry.delete(0,END)
  else:
    messagebox.showwarning("Ошибка","Введите название продукта")

#--------------------------------------------------------------------------------------------------------------
def update_listbox(search_term=""):
  global current_page
  start_index = (current_page - 1) * ITEMS_PER_PAGE
  end_index = start_index + ITEMS_PER_PAGE

  for widget in listbox.winfo_children():
    widget.destroy()

  filtered_items = [item for item, quantity in item_quantities.items() if search_term.lower() in item.lower()]
  displayed_items = filtered_items[start_index:end_index]

  for item in displayed_items:
    quantity = item_quantities[item]
    item_frame = Frame(listbox)
    item_frame.pack(fill=X)

    item_label = Label(item_frame, text=f"{item} ({quantity})",bg="white",width=37)
    item_label.pack(side=LEFT)

    add_button = Button(item_frame, text="+", command=lambda item=item: update_quantity(item, 1), width=2)
    add_button.pack(side=RIGHT)
    sub_button = Button(item_frame, text="-", command=lambda item=item: update_quantity(item, -1), width=2)
    sub_button.pack(side=RIGHT)

  update_page_buttons()

#------------------------------------------------------------------------------
def update_page_buttons():
  total_pages = (len(item_quantities) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
  prev_button.config(state=("disabled" if current_page == 1 else "normal"))
  next_button.config(state=("disabled" if current_page == total_pages else "normal"))

#------------------------------------------------------------------------------
def prev_page():
    global current_page
    current_page -= 1
    update_listbox()

#------------------------------------------------------------------------------
def next_page():
    global current_page
    current_page += 1
    update_listbox()

#------------------------------------------------------------------------------
root = Tk()
root.title("Холодильник")
root.resizable(False, False)

item_quantities = {
    "Яблоко": 5,
    "Банан": 3,
    "Апельсин": 2,
    "Груша": 1,
    "Киви": 2,
    "Манго": 7,
    "Ананас": 4,
    "Виноград": 9,
    "Арбуз": 1,
    "Дыня": 2,
    "Персик": 3,
    "Нектарин": 5
}

image1 = PhotoImage(file="holodos_1.png")
image2 = PhotoImage(file="holodos_2.png")

btn1 = Button(root, text="Открыть", command=change_image, bg="white")
btn1.grid(row=0, column=0, sticky="nw", padx=90)

search_frame = Frame(root)
toggle_search_frame(False)
#---------------------------------------------------------------------------------------
#строка поиска
search_label = Label(search_frame, text="Поиск:")
search_entry = Entry(search_frame)

search_label.grid(row=0, column=0, sticky="w", padx=5)
search_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
search_entry.bind("<KeyRelease>", search_listbox)
#---------------------------------------------------------------------------------------
current_image = image1
label = Label(root, image=image1)
label.grid(row=1, column=0, sticky="nsew")

listbox = Frame(search_frame)
listbox.grid(row=1, column=0, columnspan=2, pady=5, sticky="nsew")
#----------------------------------------------------------------------------------------
#навигация
page_controls = Frame(search_frame)
page_controls.grid(row=2, column=0, columnspan=2, pady=5)

prev_button = Button(page_controls, text="Назад", command=prev_page, state="disabled")
prev_button.pack(side=LEFT)
next_button = Button(page_controls, text="Вперед", command=next_page)
next_button.pack(side=RIGHT)

add_item_frame = Frame(search_frame)
add_item_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

#----------------------------------------------------------------------------------------
#добавление продуктов
new_item_label = Label(add_item_frame, text="Добавить продукт:")
new_item_label.grid(row=0, column=0, sticky="w")
new_item_entry = Entry(add_item_frame)
new_item_entry.grid(row=0, column=1, sticky="ew", padx=5)
add_item_button = Button(add_item_frame, text="Добавить", command=add_item)
add_item_button.grid(row=0, column=2, padx=5)
#-----------------------------------------------------------------------------------------

search_frame.grid(row=1, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

update_listbox()  

root.mainloop()