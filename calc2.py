#!/usr/bin/python3
import tkinter as tk

class Calculator():
    BUTTONS = {
        0: '%', 1: '/', 2: '*', 3: '-',
        4: '7', 5: '8', 6: '9', 7: '+',
        8: '4', 9: '5', 10: '6', 11: 'C',
        12: '1', 13: '2', 14: '3', 15: '=',
        16: '0', 18: '.'
        }

    total = 0.0
    first_num = '0'
    operation = '='

    OPERATIONS = {
        '%': lambda x, y: float(x) * (float(y)/100),
        '/': lambda x, y: float(x) / float(y),
        '*': lambda x, y: float(x) * float(y),
        '-': lambda x, y: float(x) - float(y),
        '+': lambda x, y: float(x) + float(y)
    }


    def __init__(self, master):
        self.master = master
        master.title('Calc V2!')
        master.minsize(width=180, height=250)
        master.maxsize(width=260, height=380)

        self.label_greet_text = tk.StringVar()
        self.label_greet_text.set('My Calculator V2')
        self.label_greet = tk.Label(master, textvariable=self.label_greet_text, font=('Arial', 17))
        self.label_greet.pack(fill=tk.Y, expand=True)

        self.frame_calc = tk.Frame(master, borderwidth=2, relief=tk.SUNKEN)
        self.frame_calc.pack(fill=tk.BOTH, expand=True)
        
        self.label_total_text = tk.IntVar()
        self.label_total_text.set(0.00)
        self.label_total = tk.Label(self.frame_calc,
                                    font=18,
                                    borderwidth=2,
                                    relief=tk.RAISED,
                                    pady=15,
                                    padx=5,
                                    anchor='e',
                                    textvariable=self.label_total_text)
        self.label_total.grid(row=0, column=0, columnspan=4, sticky=tk.W + tk.N + tk.E + tk.S)

        for row in range(5):
            self.frame_calc.columnconfigure(row , weight=1)
            self.frame_calc.rowconfigure(row, weight=1)
            for col in range(4):
                if row*4+col == 17 or row*4+col == 19:       #Отсутствующие кнопки 17 и 19
                    continue
                if row*4+col == 15 or row*4+col == 16:       #Растянуть кнопки 15 и 16
                    grid_row_span = grid_col_span = 2
                else:
                    grid_row_span = grid_col_span = 1
                self.create_button(self.BUTTONS[row*4+col],
                                   row+3, col,
                                   grid_col_span, grid_row_span)
        
                
    def create_button(self, value, grid_row, grid_column, grid_col_span, grid_row_span):
        self.btn = tk.Button(self.frame_calc,
                             text=value,
                             command=lambda: self.make_operation(value))
        self.btn.grid(row=grid_row,
                      column=grid_column,
                      columnspan=grid_col_span,
                      rowspan=grid_row_span,
                      sticky=tk.W + tk.N + tk.E + tk.S,
                      padx=3, pady=3)
        
    def make_operation(self, symbol):
        if symbol.isnumeric() or symbol == '.':
            if self.total != 0.0 and self.operation == '=':    # Если после нажатия '=' следущий символ - число
                self.total = 0.0                               # обнулить сумму
            self.update_num(symbol)
        elif symbol in ('+', '-', '*', '/', '%'):
            if self.total != 0.0 and self.first_num != '0':    # Производим вычисление по нажатию операторов
                self.make_total()                              # как при нажатии '='
            elif self.total == 0.0:
                self.total = float(self.first_num)             # Меняем местами сумму и вводимое число, если
                self.first_num = '0'                           # сумма была 0. Чтобы избежать нулевых результатов
            self.operation = symbol
        elif symbol == '=':
            self.make_total()
        elif symbol == 'C':
            self.make_clear()
            
    def make_clear(self):
        self.first_num = '0'
        self.operation = '='
        self.total = 0.0
        self.label_total_text.set(self.total)

    def make_total(self):
        try:
            self.total = self.OPERATIONS[self.operation](self.total, self.first_num)
        except ZeroDivisionError:
            self.total = self.total
            
        self.label_total_text.set(round(float(self.total), 6))
        self.first_num = '0'
        self.operation = '='

    def update_num(self, num):
        if self.first_num == '0':
            self.first_num = num
            if self.first_num == '.':
                self.first_num = '0.'
        else:
            if num == '.' and '.' in self.first_num:    # В числе может быть только одна десятичная точка
                self.first_num += ''
            else:
                self.first_num += num
        self.label_total_text.set(round(float(self.first_num), 6))
        
root = tk.Tk()
mycalc = Calculator(root)
root.mainloop()
