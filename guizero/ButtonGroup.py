from tkinter import Frame, StringVar

from . import utilities as utils
from .Box import Box
from .RadioButton import RadioButton


class ButtonGroup:

    def __init__(self, master, options, selected, horizontal=False, command=None, grid=None, align=None):

        self.selected = StringVar()

        # Set (using StringVar set() method) the selected option **number**
        self.selected.set(selected)
        self.description = "[ButtonGroup] object with selected option \"" + self.selected.get() + "\""
        self.options = []   # List of RadioButton objects
        self.layout_manager = "grid"
        self.horizontal = horizontal

        # Create a Tk frame object to contain the RadioButton objects
        try:
            self.tk = Frame(master)
        except AttributeError:
            utils.error_format( self.description + "\n" +
            "Could not create [ButtonGroup] object")

        # Position the radio buttons in the Frame
        gridx = 0
        gridy = 0

        # Loop through the list given, creating a RadioButton object from each
        # Defaults to setting the hidden value to the same as the text

        for button in options:
            # If only a 1D list was provided, auto number the items FROM 1
            if not isinstance(button, list):
                button = [button, options.index(button)+1]

            # Create a radio button object
            rbutton = RadioButton(self.tk, text=str(button[0]), value=str(button[1]), variable=self.selected)

            # Add a command if there was one
            if command is not None:
                rbutton.tk.config(command=command)

            # Add this radio button to the internal list
            self.options.append(rbutton)

            # Place on grid
            utils.auto_pack(rbutton, self, [gridx, gridy], "left")

            # Which way the buttons go
            if horizontal:
                gridy += 1
            else:
                gridx += 1

        # Pack the whole button group
        utils.auto_pack(self, master, grid, align)


    # PROPERTIES
    # -----------------------------------

    # Gets the selected value (1, 2, 3 etc.)
    @property
    def value(self):
        return (self.selected.get())

    # Sets which option is selected (if it doesn't exist, nothing is selected)
    @value.setter
    def value(self, value):
        self.selected.set(str(value))

    # Gets the text of the currently selected option
    @property
    def value_text(self):
        search = self.selected.get() # a string containing the selected option
        # This is a bit nasty - suggestions welcome
        for item in self.options:
            if item.value == search:
                return item.text
        return ""

    # Wondering if this is really confusing. value_text is the text associated with the selected
    # option. You can change it because it's useful to be able to *get* it, but maybe this is weird.
    @value_text.setter
    def value_text(self, value):
        search = self.selected.get()    # Currently selected number
        for item in self.options:
            if item.value == search:
                item.text = str(value)
                print( item.text )
                return 0
        utils.error_format("Could not set value text - no matching option")

    # METHODS
    # -----------------------------------

    # To help with debugging - return list of text/value pairs
    def get_group_as_list(self):
        list_of_options = []
        for option in self.options:
            list_of_options.append([option.text, option.value])
        return list_of_options

    # DEPRECATED METHODS
    # -----------------------------------
    # Get selected value (e.g. 1, 2, 3)
    def get(self):
        return self.selected.get()
        utils.deprecated("get() is deprecated. Please use the value property instead.")

    # Set which option is selected
    def set(self, value):
        self.selected.set(str(value))
        utils.deprecated("set() is deprecated. Please use the value property instead.")
