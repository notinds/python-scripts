import tkinter as tk
from tkinter import ttk, messagebox
from pint import UnitRegistry

# Initialize Pint
ureg = UnitRegistry()

# Get all unit categories from Pint
categories = {
    'Length': ['meter', 'kilometer', 'centimeter', 'millimeter', 'micrometer', 'nanometer', 'mile', 'yard', 'foot', 'inch', 'nautical_mile'],
    'Mass': ['kilogram', 'gram', 'milligram', 'microgram', 'ton', 'pound', 'ounce', 'stone'],
    'Time': ['second', 'millisecond', 'microsecond', 'nanosecond', 'minute', 'hour', 'day', 'week', 'month', 'year'],
    'Temperature': ['kelvin', 'celsius', 'fahrenheit', 'rankine'],
    'Volume': ['liter', 'milliliter', 'cubic_meter', 'cubic_centimeter', 'cubic_millimeter', 'gallon', 'quart', 'pint', 'cup', 'fluid_ounce', 'tablespoon', 'teaspoon'],
    'Area': ['square_meter', 'square_kilometer', 'square_centimeter', 'square_millimeter', 'hectare', 'acre', 'square_mile', 'square_yard', 'square_foot', 'square_inch'],
    'Speed': ['meter/second', 'kilometer/hour', 'mile/hour', 'knot', 'foot/second'],
    'Energy': ['joule', 'kilojoule', 'calorie', 'kilocalorie', 'watt_hour', 'kilowatt_hour', 'electron_volt', 'british_thermal_unit', 'us_therm', 'foot_pound'],
    'Pressure': ['pascal', 'kilopascal', 'bar', 'psi', 'atmosphere', 'torr', 'mmHg'],
    'Power': ['watt', 'kilowatt', 'megawatt', 'gigawatt', 'horsepower'],
    'Data': ['bit', 'kilobit', 'megabit', 'gigabit', 'terabit', 'byte', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte'],
    'Frequency': ['hertz', 'kilohertz', 'megahertz', 'gigahertz'],
    'Fuel Economy': ['kilometer/liter', 'liter/100_kilometer', 'mile/gallon'],
    'Digital Storage': ['byte', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte'],
}

# Flatten all units for 'All' option
def get_all_units():
    all_units = set()
    for units in categories.values():
        all_units.update(units)
    return sorted(all_units)

class UnitConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('THE unit converter (not actually)')
        self.root.geometry('500x350')
        self.root.configure(bg='#23272f')
        self.root.resizable(False, False)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', background='#23272f', foreground='#f8f8f2', font=('Segoe UI', 12))
        self.style.configure('TButton', font=('Segoe UI', 12), padding=6)
        self.style.configure('TCombobox', font=('Segoe UI', 12))
        self.style.configure('TEntry', font=('Segoe UI', 12))

        # Category
        ttk.Label(root, text='Category:').place(x=40, y=30)
        self.category_var = tk.StringVar(value='Length')
        self.category_cb = ttk.Combobox(root, textvariable=self.category_var, values=['All'] + list(categories.keys()), state='readonly', width=18)
        self.category_cb.place(x=160, y=30)
        self.category_cb.bind('<<ComboboxSelected>>', self.update_units)

        # From Unit
        ttk.Label(root, text='From:').place(x=40, y=80)
        self.from_unit_var = tk.StringVar()
        self.from_unit_cb = ttk.Combobox(root, textvariable=self.from_unit_var, width=18, state='readonly')
        self.from_unit_cb.place(x=160, y=80)

        # To Unit
        ttk.Label(root, text='To:').place(x=40, y=130)
        self.to_unit_var = tk.StringVar()
        self.to_unit_cb = ttk.Combobox(root, textvariable=self.to_unit_var, width=18, state='readonly')
        self.to_unit_cb.place(x=160, y=130)

        # Value Entry
        ttk.Label(root, text='Value:').place(x=40, y=180)
        self.value_var = tk.StringVar()
        self.value_entry = ttk.Entry(root, textvariable=self.value_var, width=20)
        self.value_entry.place(x=160, y=180)

        # Convert Button
        self.convert_btn = ttk.Button(root, text='Convert', command=self.convert)
        self.convert_btn.place(x=200, y=230)

        # Result
        self.result_label = ttk.Label(root, text='', font=('Segoe UI', 14, 'bold'), background='#23272f', foreground='#50fa7b')
        self.result_label.place(x=40, y=280)

        self.update_units()

    def update_units(self, event=None):
        cat = self.category_var.get()
        if cat == 'All':
            units = get_all_units()
        else:
            units = categories[cat]
        self.from_unit_cb['values'] = units
        self.to_unit_cb['values'] = units
        if units:
            self.from_unit_var.set(units[0])
            self.to_unit_var.set(units[1] if len(units) > 1 else units[0])

    def convert(self):
        value = self.value_var.get()
        from_unit = self.from_unit_var.get()
        to_unit = self.to_unit_var.get()
        try:
            val = float(value)
            q = val * ureg(from_unit)
            result = q.to(to_unit)
            self.result_label.config(text=f'{result.magnitude:.6g} {result.units}')
        except Exception as e:
            messagebox.showerror('Conversion Error', f'Could not convert: {e}')
            self.result_label.config(text='')

if __name__ == '__main__':
    root = tk.Tk()
    app = UnitConverterGUI(root)
    root.mainloop()

