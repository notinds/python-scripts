import tkinter as tk
from tkinter import messagebox

# Conversion functions
def hex_to_dec(hex_str):
    try:
        return str(int(hex_str, 16))
    except ValueError:
        return ''

def hex_to_bin(hex_str):
    try:
        return bin(int(hex_str, 16))[2:]
    except ValueError:
        return ''

def dec_to_hex(dec_str):
    try:
        return hex(int(dec_str))[2:].upper()
    except ValueError:
        return ''

def dec_to_bin(dec_str):
    try:
        return bin(int(dec_str))[2:]
    except ValueError:
        return ''

def bin_to_dec(bin_str):
    try:
        return str(int(bin_str, 2))
    except ValueError:
        return ''

def bin_to_hex(bin_str):
    try:
        return hex(int(bin_str, 2))[2:].upper()
    except ValueError:
        return ''

# GUI setup
root = tk.Tk()
root.title('what even is a hexadecimal')
root.geometry('350x200')

# StringVars for entry fields
hex_var = tk.StringVar()
dec_var = tk.StringVar()
bin_var = tk.StringVar()

# Update functions
def on_hex_change(*args):
    hex_val = hex_var.get().strip()
    if hex_val == '':
        dec_var.set('')
        bin_var.set('')
        return
    dec = hex_to_dec(hex_val)
    bin_ = hex_to_bin(hex_val)
    if dec == '' or bin_ == '':
        messagebox.showerror('Invalid Input', 'Invalid hexadecimal input!')
        return
    dec_var.set(dec)
    bin_var.set(bin_)

def on_dec_change(*args):
    dec_val = dec_var.get().strip()
    if dec_val == '':
        hex_var.set('')
        bin_var.set('')
        return
    hex_ = dec_to_hex(dec_val)
    bin_ = dec_to_bin(dec_val)
    if hex_ == '' or bin_ == '':
        messagebox.showerror('Invalid Input', 'Invalid decimal input!')
        return
    hex_var.set(hex_)
    bin_var.set(bin_)

def on_bin_change(*args):
    bin_val = bin_var.get().strip()
    if bin_val == '':
        hex_var.set('')
        dec_var.set('')
        return
    dec = bin_to_dec(bin_val)
    hex_ = bin_to_hex(bin_val)
    if dec == '' or hex_ == '':
        messagebox.showerror('Invalid Input', 'Invalid binary input!')
        return
    dec_var.set(dec)
    hex_var.set(hex_)

# Entry fields and labels
label_hex = tk.Label(root, text='Hexadecimal:')
label_hex.grid(row=0, column=0, padx=10, pady=10, sticky='e')
entry_hex = tk.Entry(root, textvariable=hex_var)
entry_hex.grid(row=0, column=1, padx=10, pady=10)

label_dec = tk.Label(root, text='Decimal:')
label_dec.grid(row=1, column=0, padx=10, pady=10, sticky='e')
entry_dec = tk.Entry(root, textvariable=dec_var)
entry_dec.grid(row=1, column=1, padx=10, pady=10)

label_bin = tk.Label(root, text='Binary:')
label_bin.grid(row=2, column=0, padx=10, pady=10, sticky='e')
entry_bin = tk.Entry(root, textvariable=bin_var)
entry_bin.grid(row=2, column=1, padx=10, pady=10)

# Tracing changes
hex_var.trace_add('write', lambda *args: on_hex_change() if entry_hex.focus_get() == entry_hex else None)
dec_var.trace_add('write', lambda *args: on_dec_change() if entry_dec.focus_get() == entry_dec else None)
bin_var.trace_add('write', lambda *args: on_bin_change() if entry_bin.focus_get() == entry_bin else None)

# Run the GUI
root.mainloop()

