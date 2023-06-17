import tkinter as tk
import requests
import sqlite3
from datetime import datetime
from tkinter import ttk

root = tk.Tk()
root.title("Запрос вывода API ")

tree = tk.ttk.Treeview(root, columns=('IP адрес', 'Дата запроса'), show='headings')
tree.heading('#1', text='IP адрес')
tree.heading('#2', text='Дата запроса')
tree.column('#1', width=200)
tree.column('#2', width=200)
tree.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

def get_and_insert_data():
    response = requests.get('http://51.250.95.237:5000/logs')
    data = response.json()
    db = sqlite3.connect('requests.db')
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS requests (ip_address TEXT, request_time TEXT)')
    for item in data:
        ip_address = item.get('ip_address', '')
        request_time = item.get('request_time', '')
        request_time = datetime.strptime(request_time, '%d/%b/%Y:%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO requests VALUES (?, ?)', (ip_address, request_time))
    db.commit()
    db.close()
    populate_table()

def sort_by_time():
    db = sqlite3.connect('requests.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM requests ORDER BY request_time DESC')
    rows = cursor.fetchall()
    db.close()

    for record in tree.get_children():
        tree.delete(record)

    for row in rows:
        tree.insert('', tk.END, values=row)

def populate_table(reverse=False):
    db = sqlite3.connect('requests.db')
    cursor = db.cursor()
    if reverse:
        cursor.execute('SELECT * FROM requests ORDER BY request_time DESC')
    else:
        cursor.execute('SELECT * FROM requests')
    rows = cursor.fetchall()
    db.close()

    for record in tree.get_children():
        tree.delete(record)

    for row in rows:
        tree.insert('', tk.END, values=row)

sort_by_time_button = tk.Button(root, text="Сортировать по времени", command=sort_by_time)
sort_by_time_button.grid(row=1, column=2, padx=5, pady=5)

get_and_insert_button = tk.Button(root, text="Получить и внести данные", command=get_and_insert_data)
get_and_insert_button.grid(row=1, column=0, padx=5, pady=5)

update_table_button = tk.Button(root, text="Обновить таблицу", command=populate_table)
update_table_button.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()