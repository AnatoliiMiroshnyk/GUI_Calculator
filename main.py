import tkinter as tk
from tkinter import messagebox as msgbx
import decimal

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.math_expr = tk.StringVar(value='')
        self.count_brakes = 0
        self.initUI()

    def initUI(self):
        self.master.geometry('400x400+500+250')
        self.master.title('Calculator')
        self.master.minsize(400,400)

        font_btn = ('Arial', 25)
        buttons_meanings = [['7','8','9','+','C'],
                            ['4','5','6','-','CE'],
                            ['1','2','3','*','**'],
                            ['()','0','.','/','='],]
        
        main_frame = tk.Frame(self.master, padx=0, pady=0)
        main_frame.pack(expand=True, fill='both', padx=0, pady=0)
        frames = [tk.Frame(main_frame, padx=0, pady=0) for i in range(5)]
        for frame in frames:
            frame.pack(expand=True, fill='both', padx=0, pady=0)

        screen = tk.Label(frames[0],
                       textvariable = self.math_expr,
                       font = ('Arial', 32),
                       height = 3,
                       border = 0,
                       padx = 0,
                       pady = 0,
                       anchor = 'se',
                       bg = '#595954',
                       fg = 'white',)
        screen.pack(expand=True, fill='both', padx=0, pady=0)

        buttons = [[tk.Button(frames[i], text=buttons_meanings[i-1][j], font=font_btn,
                              width=4, border=0, padx=0, pady=0, relief='groove',
                              bg='#2E2E2E', fg='white')
                    for j in range(len(buttons_meanings[i-1]))] for i in range(1, len(buttons_meanings)+1)]

        for i in buttons:
            for j in i:
                j.pack(expand=True, fill='both', side='left', padx=0, pady=0)
                if j['text'] not in ('=','C','CE','()'):
                    j.bind('<Button-1>', self.display)
                elif j['text'] == 'C':
                    j.bind('<Button-1>', lambda e: self.math_expr.set(value=''.join(list(self.math_expr.get())[:-1])))
                elif j['text'] == 'CE':
                    j.bind('<Button-1>', lambda e: self.math_expr.set(value=''))
                elif j['text'] == '()':
                    j.bind('<Button-1>', self.brakes)
                elif j['text'] == '=':
                    j.bind('<Button-1>', self.equal)
                        
        self.master.mainloop()

    def display(self, event=None, num=None):
        number = event.widget.cget('text') if not num and event else num
        me = self.math_expr.get()
        max_len = self.master.winfo_width() * 1.25 // 32
        if len(me) > max_len:
            msgbx.showinfo('Input limit',f'The length of the expression must not exceed {max_len}')
            return
        if number in ('+','*','/') and (not me or me[-1] in ('+','*','/','-','(','**')):
            msgbx.showwarning('Warning','Invalid input format')
        elif number in ('+','*','/','-','**','(',')','.') and me and me[-1] == '.':
            msgbx.showwarning('Warning','Invalid input format')
        elif number == '-' and (not me or me[-1] in ('+','*','/','-','**')):
            me += f'({number}'
            count_brakes += 1
        elif number.isdigit() and me == '0':
            me = f'{number}'
        elif number.isdigit() and me and me[-1] == '0' and me[-2] in ('+','*','/','-','(',')','**'):
            me = ''.join(list(me)[:-1]) + number
        elif number == '.' and (not me or me[-1] in ('+','*','/','-','(',')','**')):
            me += f'0{number}'
        elif number == '(' and me and me[-1].isdigit():
            me += f'*('
        else:
            me += number
        self.math_expr.set(value=me)

    def brakes(self, event):
        if self.count_brakes == 0 or self.math_expr.get()[-1] in ('+','*','/','-'):
            self.display(num='(')
            self.count_brakes += 1
        else:
            self.display(num=')')
            self.count_brakes -= 1

    def equal(self, event):
        try:
            res = eval(self.math_expr.get())
            if isinstance(res, float):
                context = decimal.Context(prec=5)
                res = context.create_decimal(res).normalize()
            self.math_expr.set(value=res)
            self.count_brakes = 0
        except:
            msgbx.showerror('Error','Invalid input format')
    
if __name__ == '__main__':
    app = App(tk.Tk())
    
