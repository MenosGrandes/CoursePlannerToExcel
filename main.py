import customtkinter
import datetime
import re
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
def select_all(widget):
    # select text
    widget.select_range(0, 'end')
    # move cursor to the end
    widget.icursor('end')

class HourValidator:
    def __init__(self, widget) -> None:
        self.vcmd = (widget.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.widget = widget
        self.regex = re.compile(r'/^([01][0-9]|2[0-3]):([0-5][0-9])$/')


    def validate(self, action, index, value_if_allowed,
                   prior_value, text, validation_type, trigger_type, widget_name):
        print(f"validate {text} | {value_if_allowed}");
        '''
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                print(f"INVALID {self.widget}")
                return False
        else:
            print(f"INVALID {self.widget}")
            return False
        '''
        # '/^([01][0-9]|2[0-3]):([0-5][0-9])$/'
        r = self.regex.search(value_if_allowed)
        print(r)
        if r is None:
            return False
        return True

class LabelAndEntry(customtkinter.CTkFrame):
    def __init__(self, master, labelName, textBoxWidth=400, textBoxHeight=60):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text=labelName)
        self.label.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w")

        self.textBox = customtkinter.CTkEntry(self,width=textBoxWidth, height=textBoxHeight);
        self.textBox.grid(row=0, column=1,padx=10, pady=(10,10), sticky="e")


        self.textBox.bind('<Control-KeyRelease-a>', self.callback)

    def get(self):
        return self.textBox.get("0.0","end")

    def callback(self,event):
        print(f"CALLBACK {event}");
        app.after(50,select_all,event.widget)

class LabelAndEntryHourValidator(LabelAndEntry):
    def __init__(self, master, labelName, textBoxWidth=400, textBoxHeight=60):
        super().__init__(master, labelName, textBoxWidth, textBoxHeight)
        self.validator = HourValidator(self)
        #self.textBox.configure(validate='key',validatecommand=self.validator.vcmd) MG maybe someday

    
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

class App(customtkinter.CTk):
    def validate(self):

        print(f"timeOfStart = {self.timeOfStart.get()}");
        timeOfStart =self.timeOfStart.get();
        output = datetime.datetime.strptime(timeOfStart, "%-H:%-M")
        print(output)

        print(f"timeOfEnd = {self.timeOfEnd.get()}");
        print(f"nazwaGrupy= {self.studentGroup.get()}");
        print(f"nazwaPrzedmiotu= {self.nameOfClass.get()}");
        return True
    def do(self):
        print("ZACZYNAM");


    def __init__(self):
        super().__init__()


        row=0
        column = 0
        self.title("my app")
        self.geometry("600x500")
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.classDates = LabelAndEntry(self, "Daty")
        self.classDates.grid(row=row, column=column, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)
        row+=1;

        self.nameOfClass= LabelAndEntry(self, "NazwaPrzedmiotu")
        self.nameOfClass.grid(row=row, column=column, padx=(10,10), pady=(10, 10), sticky="nsew",  columnspan=2)
        row+=1;

        self.timeOfStart= LabelAndEntryHourValidator(self, "godzina rozpoczecia", textBoxWidth=100)
        self.timeOfStart.grid(row=row, column=column, padx=(10,10), pady=(10, 10), sticky="n")
        column+=1;
        self.timeOfEnd= LabelAndEntryHourValidator(self, "godzina zakonczenia", textBoxWidth=100)
        self.timeOfEnd.grid(row=row, column=column, padx=(10,10), pady=(10, 10), sticky="n")
        column-=1;
        row+=1;

        self.studentGroup= LabelAndEntry(self, "Nazwa grupy")
        self.studentGroup.grid(row=row, column=column, padx=(10,10), pady=(10, 10), sticky="n", columnspan=2)
        row+=1;

        self.generateButton = customtkinter.CTkButton(self, text="Create", command=self.do)
        self.generateButton.grid(row=row, column=column, padx=10, pady=10, sticky="ew", columnspan=2)
app = App();

app.mainloop()
