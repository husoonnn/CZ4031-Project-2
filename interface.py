# The file interface.py contains the code for the GUI.

import json
import tkinter as tk
from tkinter import font, ttk
import preprocessing
import sqlparse
import json
import psycopg2

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = preprocessing.config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


conn = psycopg2.connect(
    host="localhost",
    database="TPC-H",
    user="postgres",
    password="password")

cur = conn.cursor()

def get_json():
    """ query parts from the parts table """
    conn = None
    try:
        params = preprocessing.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(retrieveInput())
        rows = cur.fetchall()
        print(json.dumps(rows))
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    

def retrieveInput():
    inputValue=query_text.get('1.0', 'end-1c')
    return inputValue

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Query Visualizer')
    button_font = font.Font(family='Google Sans Display', size=12, weight='bold')
    text_font = font.Font(family='Fira Code Retina', size=12)
    label_font = font.Font(family='Google Sans Display', size=12)
    query_label = tk.Label(root, text='Enter your SQL query here', font=label_font)
    query_text = tk.Text(root, font=text_font, height=20)
    query_scrollbar = tk.Scrollbar(root, orient='vertical', command=query_text.yview)
    
    visualize_button = tk.Button(root, text='EXECUTE', padx=12, bg='#1FBFE0', fg='white', font=button_font,
                                 anchor='center', command=lambda: get_json())
    # visualize_button.bind('<Button-1>', lambda event: visualize_query(root, query_text.get('1.0', 'end-1c'),
    #                                                                   plan_text.get('1.0', 'end-1c')))

    query_label.grid(row=0, sticky='w', padx=12, pady=(12, 0))
    query_text.grid(row=1, padx=(12, 0))
    query_scrollbar.grid(row=1, column=1, sticky='ns', padx=(0, 12))
    visualize_button.grid(row=2, sticky='e', padx=0, pady=12)

    root.mainloop()

