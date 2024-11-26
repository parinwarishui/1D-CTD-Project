from tkinter import *  # Imports all classes/functions from tkinter
from tkinter import ttk  # Imports themed widgets from tkinter

class FeetToMeters:  # Defines main application class
    def __init__(self, root):  # Constructor that takes root window as parameter
        root.title("Feet to Meters")  # Sets window title
        
        # Creates main frame with padding (left top right bottom)
        mainframe = ttk.Frame(root, padding="3 3 12 12")  
        
        # Places frame in window at column 0, row 0 and makes it stick to all sides
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))  
        
        # Makes column 0 and row 0 expand to fill extra space
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Creates StringVar to store feet input value
        self.feet = StringVar()
        
        # Creates entry widget for feet input, width 7 characters
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))
        
        # Creates StringVar to store converted meters value
        self.meters = StringVar()
        
        # Creates label to display meters result
        ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        
        # Creates Calculate button that calls calculate() when clicked
        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)
        
        # Creates static labels for the interface
        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
        
        # Adds padding to all widgets in mainframe
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
        # Sets initial focus to feet entry widget
        feet_entry.focus()
        
        # Binds Return key to calculate function
        root.bind("<Return>", self.calculate)
    
    def calculate(self, *args):  # Calculate method that converts feet to meters
        try:
            value = float(self.feet.get())  # Gets feet value and converts to float
            # Converts to meters with 4 decimal precision and updates meters StringVar
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:  # Handles invalid input by doing nothing
            pass

# Creates root window
root = Tk()

# Creates instance of FeetToMeters class
FeetToMeters(root)

# Starts the Tkinter event loop
root.mainloop()