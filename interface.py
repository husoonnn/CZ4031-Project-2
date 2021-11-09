import json
import tkinter as tk
from tkinter import font, ttk, messagebox
from node_types import ATTRIBUTE
import sqlparse
import node_types
import psycopg2
import annotation


COLORS = [
    ('#f44336', 'black'),
    ('#e91e63', 'black'),
    ('#9c27b0', 'white'),
    ('#673ab7', 'white'),
    ('#3f51b5', 'white'),
    ('#2196f3', 'black'),
    ('#03a9f4', 'black'),
    ('#00bcd4', 'black'),
    ('#009688', 'black'),
    ('#4caf50', 'black'),
    ('#8bc34a', 'black'),
    ('#cddc39', 'black'),
    ('#ffeb3b', 'black'),
    ('#ffc107', 'black')
]

NODE_COLORS = {node_type: color
               for node_type, color in zip(node_types.NODE_TYPES, COLORS)}


conn = psycopg2.connect(
    host="localhost",
    database="TPC-H",
    user="postgres",
    password="password")

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = conn

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



cur = conn.cursor()

def get_json():
    """ query parts from the parts table """
    
    conn = None
    x = None 
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="TPC-H",
            user="postgres",
            password="password")
        
        cur = conn.cursor()
        cur.execute(retrieveInput())
        rows = cur.fetchall()
        x = json.dumps(rows)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        messagebox.showerror("Error",error)
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print("success")
    return x
    

def retrieveInput():
    inputValue=query_text.get('1.0', 'end-1c')
    return inputValue

class TreeFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.button_font = font.Font(family='Google Sans Display', size=12, weight='bold')
        self.canvas = tk.Canvas(self, background= '#c5ded2')
        self.canvas.grid(row=0, column=0)

        self._on_hover_listener = None
        self._on_click_listener = None
        self._on_hover_end_listener = None

    def draw_tree(self, root_node):
        bbox = self._draw_node(root_node, 12, 12)
        self.canvas.configure(width=bbox[2] - bbox[0] + 24, height=bbox[3] - bbox[1] + 24)

    def set_on_hover_listener(self, on_hover_listener):
        self._on_hover_listener = on_hover_listener

    def set_on_click_listener(self, on_click_listener):
        self._on_click_listener = on_click_listener

    def set_on_hover_end_listener(self, on_hover_end_listener):
        self._on_hover_end_listener = on_hover_end_listener

    def _on_click(self, node):
        if self._on_click_listener is not None:
            self._on_click_listener(node)

    def _on_hover(self, node):
        if self._on_hover_listener is not None:
            self._on_hover_listener(node)

    def _on_hover_end(self, node):
        if self._on_hover_end_listener is not None:
            self._on_hover_end_listener(node)

    def _draw_node(self, node, x1, y1):
        child_x = x1
        left = x1
        right = -1
        top = y1
        bottom = -1
        #1FBFE0
        button = tk.Button(self.canvas, text=node.node_type, padx=12,
                           bg='#7d8ed1', fg='white', font=self.button_font, anchor='center')
        button.bind('<Button-1>', lambda event: self._on_click(node))
        button.bind('<Enter>', lambda event: self._on_hover(node))
        button.bind('<Leave>', lambda event: self._on_hover_end(node))
        window = self.canvas.create_window((x1, y1), window=button, anchor='nw')
        bbox = self.canvas.bbox(window)
        child_bboxes = []
        if len(node.children) == 0:
            return bbox
        for child in node.children:
            child_bbox = self._draw_node(child, child_x, y1 + 60)  # (x1, y1, x2, y2)
            child_x = child_bbox[2] + 20
            right = max(right, child_bbox[2])
            bottom = max(bottom, child_bbox[3])
            child_bboxes.append(child_bbox)
        x_mid = (left + right) // 2
        bbox_mid_x = (bbox[0] + bbox[2]) // 2
        self.canvas.move(window, x_mid - bbox_mid_x, 0)
        for child_bbox in child_bboxes:
            child_mid_x = (child_bbox[0] + child_bbox[2]) // 2
            self.canvas.create_line(x_mid, bbox[3], child_mid_x, child_bbox[1], width=2, arrow=tk.FIRST)
        return left, top, right, bottom


class QueryFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.text_font = font.Font(family='Fira Code Retina', size=12)
        self.text = tk.Text(self, height=18, font=self.text_font)
        self.text.grid(row=0, column=0)
        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.text.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.text.configure(yscrollcommand=self.scrollbar.set)

        for node_type, color in NODE_COLORS.items():
            self.text.tag_configure(node_type, background=color[0], foreground=color[1])
        self.text.tag_configure('OTHER', background='#ff9800', foreground='black')

        self.index_map = {}
        self.query = None

    def set_query(self, query):
        self.query = query
        self.text.delete('1.0', 'end')
        self.text.insert('end', query)

        self.index_map = {}
        line = 1
        column = 0
        index = 0
        while index <= len(query):
            self.index_map[index] = f'{line}.{column}'
            if index < len(query) and query[index] == '\n':
                line += 1
                column = 0
            else:
                column += 1
            index += 1

    def highlight_text(self, start, end, node_type):
        if self.query is not None:
            print(f'query[{start}:{end}] = {self.query[start:end]}')
        if node_type in node_types.NODE_TYPES:
            self.text.tag_add(node_type, self.index_map[start], self.index_map[end])
        else:
            self.text.tag_add('OTHER', self.index_map[start], self.index_map[end])

    def clear_highlighting(self):
        for node_type in node_types.NODE_TYPES + ['OTHER']:
            self.text.tag_remove(node_type, '1.0', 'end')


class TableFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        table_view_style = ttk.Style()
        table_view_style.configure('Treeview', font=('Google Sans Display', 12))
        table_view_style.configure('Treeview.Heading', font=('Google Sans Display', 14, 'bold'))
        self.table_view = ttk.Treeview(self)
        self.table_view['columns'] = ['Value']
        self.table_view.column('#0', minwidth=0, width=700) #, stretch=tk.NO
        self.table_view.heading('#0', text='Analysis', anchor='w')
        self.table_view.grid(row=0, column=0, sticky='nswe')

        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.table_view.yview)
        self.table_view.configure(yscrollcommand=self.scrollbar.set)
        # self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        

    def show_node_info(self, node):
        raw_json = node.raw_json
        print("HIIII", raw_json)
        self.table_view.delete(*self.table_view.get_children())
        for index, (key, value) in enumerate(raw_json.items()):
            # self.table_view.insert('', index+1, text=key, values=[value])
            if key == "Node Type":
                for operations in ATTRIBUTE:
                    if operations == value.upper():
                        operation_type = ATTRIBUTE[operations]
            
            if key in operation_type:
                B = str(key) + ": " + str(value)
                self.table_view.insert('', index+1, text=B)



def execute_query(root_widget, query):
    plan = get_json()
    plan = plan[2:-2]
    
    plan = json.loads(plan)
    print(plan)
    
    top_level = tk.Toplevel(root_widget)
    
    top_level.title('Visualization')
    top_level.iconphoto(False, tk.PhotoImage(file='tree.png'))
    query = query.replace('\n', ' ')
    query = sqlparse.format(query, reindent=True, keyword_case='upper')

    query_frame = QueryFrame(top_level)
    query_frame.set_query(query)
    query_frame.grid(row=0, column=0, sticky='eswn')

    table_frame = TableFrame(top_level)
    table_frame.grid(row=1, column=0, sticky='eswn')

    tree_frame = TreeFrame(top_level)
    tree_frame.grid(row=0, column=1, rowspan=2)

    print(type(plan))
    root_node = annotation.build_tree([plan[0]['Plan']])[0]
    match_dict = annotation.build_invert_relation(query, root_node)

    def on_click_listener(node):
        table_frame.show_node_info(node)

    def on_hover_listener(node):
        if node in match_dict:
            for start, end in match_dict[node]:
                query_frame.highlight_text(start, end, node.node_type)

    def on_hover_end_listener(node):
        query_frame.clear_highlighting()

    tree_frame.set_on_click_listener(on_click_listener)
    tree_frame.set_on_hover_listener(on_hover_listener)
    tree_frame.set_on_hover_end_listener(on_hover_end_listener)

    tree_frame.draw_tree(root_node)
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Input Query')
    root.iconphoto(False, tk.PhotoImage(file='tree.png'))

    button_font = font.Font(family='Google Sans Display', size=12, weight='bold')
    text_font = font.Font(family='Fira Code Retina', size=12)
    label_font = font.Font(family='Google Sans Display', size=12)

    query_label = tk.Label(root, text='Enter your SQL query here', font=label_font)
    query_text = tk.Text(root, font=text_font, height=20)

    execute_button = tk.Button(root, text='EXECUTE', padx=12, bg='#1FBFE0', fg='white', font=button_font,
                                 anchor='center', command=lambda: get_json())

    execute_button.bind('<Button-1>', lambda event: execute_query(root, retrieveInput()))

    query_scrollbar = tk.Scrollbar(root, orient='vertical', command=query_text.yview)
 
    query_text.configure(yscrollcommand=query_scrollbar.set)
  
    query_label.grid(row=0, sticky='w', padx=12, pady=(12, 0))
    query_text.grid(row=1, padx=(12, 0))
    query_scrollbar.grid(row=1, column=1, sticky='ns', padx=(0, 12))

    execute_button.grid(row=4, sticky='e', padx=12, pady=12)

    root.mainloop()
