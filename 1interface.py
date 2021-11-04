# The file interface.py contains the code for the GUI.

import json
import tkinter as tk
from tkinter import font, ttk

import sqlparse

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
                                 anchor='center', command=lambda: retrieveInput())
    # visualize_button.bind('<Button-1>', lambda event: visualize_query(root, query_text.get('1.0', 'end-1c'),
    #                                                                   plan_text.get('1.0', 'end-1c')))

    query_label.grid(row=0, sticky='w', padx=12, pady=(12, 0))
    query_text.grid(row=1, padx=(12, 0))
    query_scrollbar.grid(row=1, column=1, sticky='ns', padx=(0, 12))
    visualize_button.grid(row=2, sticky='e', padx=0, pady=12)

    root.mainloop()

