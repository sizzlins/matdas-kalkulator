import tkinter as tk
from tkinter import messagebox
import sympy as sp

class MatdasKalkulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Matdas Kalkulator")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        # Layar Kalkulator
        self.display_var = tk.StringVar()
        self.display = tk.Entry(root, textvariable=self.display_var, font=('Arial', 24), bd=10, insertwidth=4, width=14, borderwidth=4, justify='right')
        self.display.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="we")

        # Mendefinisikan tombol-tombol
        self.create_buttons()

        # Bind tombol Enter di keyboard agar langsung menghitung
        self.root.bind('<Return>', lambda event: self.button_equal())

    def create_buttons(self):
        # Tombol Standar
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('x', 4, 2), ('+', 4, 3)
        ]

        for (text, row, col) in buttons:
            btn = tk.Button(self.root, text=text, font=('Arial', 16, 'bold'), command=lambda t=text: self.button_click(t))
            btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

        # Tombol Spesial (Matdas)
        btn_parenthesis_open = tk.Button(self.root, text='(', font=('Arial', 16, 'bold'), command=lambda: self.button_click('('))
        btn_parenthesis_open.grid(row=5, column=0, sticky="nsew", padx=3, pady=3)
        
        btn_parenthesis_close = tk.Button(self.root, text=')', font=('Arial', 16, 'bold'), command=lambda: self.button_click(')'))
        btn_parenthesis_close.grid(row=5, column=1, sticky="nsew", padx=3, pady=3)

        btn_power = tk.Button(self.root, text='^', font=('Arial', 16, 'bold'), command=lambda: self.button_click('**'))
        btn_power.grid(row=5, column=2, sticky="nsew", padx=3, pady=3)

        btn_clear = tk.Button(self.root, text='Hapus', font=('Arial', 14, 'bold'), bg='#ff9999', command=self.button_clear)
        btn_clear.grid(row=5, column=3, sticky="nsew", padx=3, pady=3)

        btn_integral = tk.Button(self.root, text='Integral (∫)', font=('Arial', 16, 'bold'), bg='#99ccff', command=self.button_integral)
        btn_integral.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

        btn_derivative = tk.Button(self.root, text='Turunan (dx)', font=('Arial', 16, 'bold'), bg='#ffcc99', command=self.button_derivative)
        btn_derivative.grid(row=6, column=2, columnspan=2, sticky="nsew", padx=3, pady=3)

        btn_equal = tk.Button(self.root, text='Hitung (=)', font=('Arial', 16, 'bold'), bg='#99ff99', command=self.button_equal)
        btn_equal.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

        btn_solve = tk.Button(self.root, text='Cari x (=0)', font=('Arial', 16, 'bold'), bg='#cc99ff', command=self.button_solve)
        btn_solve.grid(row=7, column=2, columnspan=2, sticky="nsew", padx=3, pady=3)

        # Konfigurasi grid agar rapi
        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def button_click(self, char):
        current = self.display_var.get()
        self.display_var.set(current + str(char))

    def button_clear(self):
        self.display_var.set("")

    def get_parsed_expr(self, expr_str):
        # Gunakan sympy parser agar mendukung implicit multiplication (seperti 2x -> 2*x)
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        transformations = (standard_transformations + (implicit_multiplication_application,))
        # Ubah ^ menjadi ** untuk amannya
        expr_str = expr_str.replace('^', '**')
        return parse_expr(expr_str, transformations=transformations)

    def format_result(self, result):
        if result in [sp.zoo, sp.oo, -sp.oo, sp.nan]:
            return "Tak Terdefinisi"
        return str(result)

    def button_equal(self):
        expr_str = self.display_var.get()
        if not expr_str:
            return
        try:
            result = self.get_parsed_expr(expr_str)
            self.display_var.set(self.format_result(result))
        except Exception as e:
            messagebox.showerror("Error", "Ekspresi tidak valid!")

    def button_integral(self):
        expr_str = self.display_var.get()
        if not expr_str:
            return
        try:
            x = sp.Symbol('x')
            expr = self.get_parsed_expr(expr_str)
            
            if any(sym != x for sym in expr.free_symbols):
                messagebox.showerror("Error", "Hanya variabel 'x' yang diizinkan untuk dikalkulasi!")
                return
                
            # Menghitung Integral terhadap x
            result = sp.integrate(expr, x)
            self.display_var.set(self.format_result(result))
        except Exception as e:
            messagebox.showerror("Error", "Gagal menghitung Integral! Pastikan ekspresi valid.")

    def button_derivative(self):
        expr_str = self.display_var.get()
        if not expr_str:
            return
        try:
            x = sp.Symbol('x')
            expr = self.get_parsed_expr(expr_str)
            
            if any(sym != x for sym in expr.free_symbols):
                messagebox.showerror("Error", "Hanya variabel 'x' yang diizinkan untuk dikalkulasi!")
                return
                
            # Menghitung Turunan terhadap x
            result = sp.diff(expr, x)
            self.display_var.set(self.format_result(result))
        except Exception as e:
            messagebox.showerror("Error", "Gagal menghitung Turunan! Pastikan ekspresi valid.")

    def button_solve(self):
        expr_str = self.display_var.get()
        if not expr_str:
            return
        try:
            x = sp.Symbol('x')
            expr = self.get_parsed_expr(expr_str)
            
            if any(sym != x for sym in expr.free_symbols):
                messagebox.showerror("Error", "Hanya variabel 'x' yang diizinkan untuk dikalkulasi!")
                return
                
            # Mencari nilai x saat expr = 0
            roots = sp.solve(expr, x)
            if not roots:
                self.display_var.set("Tidak ada solusi real")
            else:
                # Format hasil agar rapi jika ada beberapa akar
                res_str = ", ".join(self.format_result(r) for r in roots)
                self.display_var.set(f"x = {res_str}")
        except Exception as e:
            messagebox.showerror("Error", "Gagal mencari nilai x! Pastikan ekspresi valid.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MatdasKalkulator(root)
    root.mainloop()
