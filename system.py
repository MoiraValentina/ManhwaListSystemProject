import tkinter as tk
from tkinter import messagebox, ttk
import database
from pathlib import Path
from PIL import Image, ImageTk

bg_color = '#06061f'
highlight_color = '#c1a0d3'
count = 0

# ------- FUNCTIONS -------
def logout():
    root.destroy()
    import login

def show_data():
    info = database.fetch()
    table.delete(*table.get_children())
    for i in info:
        table.insert('', "end", values=i)

def clear():
    idE.delete(0, "end")
    titleE.delete(0, "end")
    authorE.delete(0, "end")
    chaptersE.delete(0, "end")
    lastreadE.delete(0, "end")
    statusB.set('Ongoing')

def selected(event):
    selected_i = table.selection()
    if selected_i:
        row = table.item(selected_i)['values']
        clear()
        idE.insert(0, row[0])
        titleE.insert(0, row[1])
        authorE.insert(0, row[2])
        chaptersE.insert(0, row[3])
        lastreadE.insert(0, row[4])
        statusB.set(row[5])

def add():
    if idE.get() == '' or titleE.get() == '' or authorE.get() == '' or chaptersE.get() == '' or lastreadE.get() == '':
        messagebox.showerror('↻ Try again ↻', 'All details are required.')
    elif database.id_exists(idE.get()):
        messagebox.showerror('↻ Try again ↻', 'Manhwa already listed.')
    else:
        if lastreadE.get().isdigit() and chaptersE.get().isdigit():
            if int(lastreadE.get()) > int(chaptersE.get()):
                messagebox.showerror('↻ Try again ↻', 'Last read must be less than the total chapters')
                return
                
            database.insert(idE.get(), titleE.get(),authorE.get(), chaptersE.get(), lastreadE.get(), statusB.get())
            show_data()
            clear()
            
        else:
            messagebox.showerror('↻ Try again ↻', 'Total Chapters and Last Read must be a number.')
        
        

def remove():
    selected_i = table.selection()
    if not selected_i:
        messagebox.showerror('↻ Try again ↻', 'Select Manhwa to delete')
    else:
        database.delete(idE.get())
        show_data()
        clear()

def edit(event):
    selected_i = table.selection()
    if not selected_i:
        add()
    else:
        if lastreadE.get().isdigit() and chaptersE.get().isdigit():
            if int(lastreadE.get()) > int(chaptersE.get()):
                messagebox.showerror('↻ Try again ↻', 'Last read must be less than the total chapters')
                return
                
            database.update(idE.get(), titleE.get(), authorE.get(), chaptersE.get(), lastreadE.get(), statusB.get())
            show_data()
            clear()
            
        else:
            messagebox.showerror('↻ Try again ↻', 'Total Chapters and Last Read must be a number.')

def clear_all():
    table.selection_remove(table.focus())
    clear()

def search_manhwa():
    query = searchE.get().lower()
    if query:
        results = []
        for row in database.fetch():
            if any(query in str(value).lower() for value in row):
                results.append(row)
        table.delete(*table.get_children())
        for item in results:
            table.insert('', "end", values=item)
    else:
        show_data()

def search2(event):
    search_manhwa()


def showalldata():
    show_data()

def format():
    result = messagebox.askyesno('Confirm', 'Do you really want to delete everything?')
    if result:
        database.deleteall()
        show_data()
        clear()


def showdetails():
    detailW = tk.Toplevel()
    detailW.title('My Manhwa Information')
    detailW.geometry('700x350+380+320')
    detailW.configure(bg='#121212')
    
    manhwaInfo = tk.Frame(detailW, bg='#121212')
    manhwaInfo.pack(pady=30)

    def on_hover_totalM(event):
        totalM.config(fg='#00d8d6')
    
    def on_leave_totalM(event):
        totalM.config(fg='#0d7377')
    
    totalM = tk.Label(manhwaInfo, text=f'Total Manhwas: {database.countR()}', bg='#121212', fg='#0d7377', font=('Helvetica', 18, 'bold'))
    totalM.pack(pady=(10, 5))
    totalM.bind("<Enter>", on_hover_totalM)
    totalM.bind("<Leave>", on_leave_totalM)

    
    def on_hover_totalRead(event):
        totalRead.config(fg='#0d7377')
    
    def on_leave_totalRead(event):
        totalRead.config(fg='#00d8d6')
    
    readT = database.getRead()
    totalRead = tk.Label(manhwaInfo, text=f'Total Chapters Read: {readT}',
                         bg='#121212', fg='#00d8d6', font=('Helvetica', 18, 'bold'))
    totalRead.pack(pady=(5, 5))
    totalRead.bind("<Enter>", on_hover_totalRead)
    totalRead.bind("<Leave>", on_leave_totalRead)
    
    instructionsF = tk.Frame(detailW, bg='#1f1f1f', highlightbackground='#0d7377', highlightthickness=2)
    instructionsF.pack(pady=(20, 10), padx=20, fill='x')
    
    insT = tk.Label(instructionsF, text='Information', bg='#1f1f1f', fg='#ffffff',
                    font=('Helvetica', 14, 'bold'))
    insT.pack(pady=10)
    
    instructions = [
        'To ADD: Input details in the entry fields and press Enter or click the Add button.',
        'To UPDATE: Select an entry from the list, edit the details, and press Enter.',
        'To DELETE: Select an entry from the list and click the Delete button.'
    ]
    
    for ins in instructions:
        tk.Label(instructionsF, text=ins, bg='#1f1f1f', fg='#cccccc',
                 font=('Helvetica', 12), wraplength=650, justify='left').pack(pady=5)



def changeTheme(choice):
    global bg_color, highlight_color, bg_pic, bg_image


    if choice == 'red':
        bg_color = '#101010'
        highlight_color = '#ff3c3c'
        bg_pic = 'red_bg.png'
    elif choice == 'green':
        bg_color = '#032c28'
        highlight_color = '#0bca82'
        bg_pic = 'green_bg.png'
    elif choice == 'blue':
        bg_color = '#001e54'
        highlight_color = '#30cef0'
        bg_pic = 'blue_bg.png'
    elif choice == 'purple':
        bg_color = '#06061f'
        highlight_color = '#c1a0d3'
        bg_pic = 'purple_bg.png'        
    

    logoutbtn.config(bg=highlight_color)
    theme.config(bg=highlight_color)
    manhwaList.config(bg=bg_color)
    bottom.config(background=bg_color)
    formF.config(bg=bg_color)

    titleF.config(highlightbackground=highlight_color, bg=bg_color)
    titleL.config(bg=bg_color)
    authorF.config(highlightbackground=highlight_color, bg=bg_color)
    authorL.config(bg=bg_color)
    chaptersF.config(highlightbackground=highlight_color, bg=bg_color)
    chaptersL.config(bg=bg_color)
    lastreadF.config(highlightbackground=highlight_color, bg=bg_color)
    lastreadL.config(bg=bg_color)
    idF.config(highlightbackground=highlight_color, bg=bg_color)
    idL.config(bg=bg_color)
    statusF.config(highlightbackground=highlight_color, bg=bg_color)
    statusL.config(bg=bg_color)
    buttonsF.config(bg=bg_color)
    
    addbtn.config(bg=highlight_color)
    clearbtn.config(bg=highlight_color)
    deletebuttons.config(bg=highlight_color)
    
    detailsbtn.config(bg=bg_color)
        
    searchFrame.config(bg=bg_color)
    showallbtn.config(bg=bg_color)
    searchb.config(bg=bg_color)
    
    
    style.configure('Treeview', background=bg_color)


    try:
        bg_image_path = relative_to_assets(bg_pic)
        new_bg_image = ImageTk.PhotoImage(Image.open(bg_image_path))
        bg_image = new_bg_image
        canvas.itemconfig(bg_image_id, image=bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load background image: {e}")





root = tk.Tk()
root.title('Manhwa Compilation System')
root.geometry('1100x700+210+50')
root.resizable(0, 0)
root.grid_columnconfigure(0, weight=1)





# ------- GUI -------




OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\miniconda3\envs\myproject\MY SYSTEM\assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


bg_image = None
bg_pic = 'purple_bg.png'
def load_images():
    global bg_image
    try:
        bg_image_path = relative_to_assets(bg_pic)
        bg_image = ImageTk.PhotoImage(Image.open(bg_image_path))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load background image: {e}")

load_images()

canvas = tk.Canvas(root, width=1100, height=700)
canvas.pack(fill='both', expand=True)


if bg_image:
    bg_image_id = canvas.create_image(0, 0, image=bg_image, anchor='nw')
else:
    messagebox.showerror("Error", "Background image not loaded!")


top_buttons = tk.Frame(root)
top_buttons.place(x=70, y=30)

logoutbtn = tk.Button(top_buttons, text='Logout', padx=10, bg=highlight_color, fg='#fff', font=('Helvetica', 13, 'bold'), width=10, relief=tk.RIDGE, bd=3, command=logout)
logoutbtn.pack(side=tk.LEFT)

theme = tk.Menubutton(top_buttons, text='Theme', padx=10, bg=highlight_color, fg='#fff', font=('Helvetica', 13, 'bold'), width=10, relief=tk.RAISED, bd=3)
theme.pack(side=tk.RIGHT)
menuTheme = tk.Menu(theme, tearoff=0)
theme.config(menu=menuTheme)
menuTheme.add_command(label='Red', command= lambda: changeTheme('red'))
menuTheme.add_command(label='Green', command= lambda: changeTheme('green'))
menuTheme.add_command(label='Blue', command= lambda: changeTheme('blue'))
menuTheme.add_command(label='Purple', command= lambda: changeTheme('purple'))




# ------- LIST -------

manhwaList = tk.Frame(root, bg=bg_color, padx=10)
manhwaList.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

table = ttk.Treeview(manhwaList, height=10)
table.grid(row=0, column=0)

table['column'] = ('Id', 'Title', 'Author', 'Chapters', 'Read', 'Status')

table.heading('Id', text='Code')
table.heading('Title', text='Title')
table.heading('Author', text='Author & Artist')
table.heading('Chapters', text='Total Chapters')
table.heading('Read', text='Last Read')
table.heading('Status', text='Status')

table.config(show='headings')

table.column('Id', width=100)
table.column('Title', width=250)
table.column('Author', width=300)
table.column('Chapters', width=100)
table.column('Read', width=100)
table.column('Status', width=100)

style = ttk.Style()

style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
style.configure('Treeview', font=('Helvetica', 12), background=bg_color, foreground='white', rowheight=30 )

style.map('Treeview', padding=[('selected', 4), ('!selected', 2)])



# ------- FORM -------

bottom = tk.Frame(root, background=bg_color, relief=tk.GROOVE, bd=5)
bottom.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

formF = tk.Frame(bottom, relief=tk.FLAT, bd=5, bg=bg_color)
formF.pack(side=tk.LEFT)


#Title
titleF = tk.Frame(formF, highlightbackground = highlight_color, highlightthickness=2, bg=bg_color)
titleF.grid(row=0, column=0, pady=12, padx=15)
titleL = tk.Label(titleF, text='Title', font=('arial', 10, 'bold'), bg=bg_color, fg='white')
titleL.pack(side=tk.LEFT, padx=(7, 24))
titleE = tk.Entry(titleF, font=('arial', 13), width=25, bd=5, relief=tk.SUNKEN)
titleE.pack(side=tk.RIGHT)


#Author
authorF = tk.Frame(formF, highlightbackground = highlight_color, highlightthickness=2, bg=bg_color)
authorF.grid(row=1, column=0, pady=12, padx=15)
authorL = tk.Label(authorF, text='Creator', font=('arial', 10, 'bold'), bg=bg_color, fg='white')
authorL.pack(side=tk.LEFT, padx=5)
authorE = tk.Entry(authorF, font=('arial', 13), width=25, bd=5, relief=tk.SUNKEN)
authorE.pack(side=tk.RIGHT)


#Total Chapters
chaptersF = tk.Frame(formF, highlightbackground = highlight_color, highlightthickness=2, bg=bg_color)
chaptersF.grid(row=0, column=2, pady=12, padx=15)
chaptersL = tk.Label(chaptersF, text='Total Chp.', font=('arial', 10, 'bold'), bg=bg_color, fg='white')
chaptersL.pack(side=tk.LEFT, padx=8)
chaptersE = tk.Entry(chaptersF, font=('arial', 13), width=8, bd=5, relief=tk.SUNKEN)
chaptersE.pack(side=tk.RIGHT)


#Last read
lastreadF = tk.Frame(formF, highlightbackground = highlight_color, highlightthickness=2, bg=bg_color)
lastreadF.grid(row=1, column=2, pady=12, padx=15)
lastreadL = tk.Label(lastreadF, text='Last Read', font=('arial', 10, 'bold'), bg=bg_color, fg='white')
lastreadL.pack(side=tk.LEFT, padx=8)
lastreadE = tk.Entry(lastreadF, font=('arial', 13), width=8, bd=5, relief=tk.SUNKEN)
lastreadE.pack(side=tk.RIGHT)


#Id
idF = tk.Frame(formF, highlightbackground = highlight_color, highlightthickness=2, bg=bg_color)
idF.grid(row=0, column=4, pady=12, padx=15)
idL = tk.Label(idF, text='ID (permanent)', font=('arial', 10, 'bold'), bg=bg_color, fg='white')
idL.pack(side=tk.LEFT, padx=2)
idE = tk.Entry(idF, font=('arial', 13), width=8, bd=5, relief=tk.SUNKEN)
idE.pack(side=tk.RIGHT)


#Status
statusF = tk.Frame(formF, highlightbackground = highlight_color, highlightthickness=2, relief=tk.FLAT, bd=5, bg=bg_color)
statusF.grid(row=1, column=4, pady=12, padx=15)
status_options = ['Ongoing', 'Completed']
statusL = tk.Label(statusF, text='Status', font=('arial', 10, 'bold'), bg=bg_color, fg='white')
statusL.pack(side=tk.LEFT, padx=(5, 15))
statusB = ttk.Combobox(statusF, values=status_options, state='readonly', font=('arial', 10), width=13)
statusB.pack(side=tk.RIGHT)
statusB.set("Ongoing")


# ------- BUTTONS -------

buttonsF = tk.Frame(bottom, width=10, bg=bg_color, relief=tk.RAISED)
buttonsF.pack(side=tk.RIGHT)

clearbtn = tk.Button(buttonsF, text='Clear Input', padx=10, bg=highlight_color, fg='#000', font=('Helvetica', 10, 'bold'), width=10, relief=tk.RAISED, command=clear_all)
clearbtn.pack(side=tk.TOP, pady=5, padx=20)

addbtn = tk.Button(buttonsF, text='Add Manhwa', padx=10, bg=highlight_color, fg='#000', font=('Helvetica', 10, 'bold'), width=10, relief=tk.RAISED, command=add)
addbtn.pack(side=tk.TOP, pady=5, padx=20)

deletebuttons = tk.Menubutton(buttonsF, text='Delete', padx=10, bg=highlight_color, fg='#000', font=('Helvetica', 10, 'bold'), width=12, relief=tk.RAISED)
deletebuttons.pack(side=tk.TOP, pady=5, padx=20)
menu = tk.Menu(deletebuttons, tearoff=0)
deletebuttons.config(menu=menu)
menu.add_command(label='Delete', command=remove)
menu.add_command(label='Delete All', command=format)



searchFrame = tk.Frame(root, bg=bg_color, highlightbackground = '#fff', highlightthickness=2)
searchFrame.place(x=360, y=635)

showallbtn = tk.Button(searchFrame, text='Show all', bg=bg_color, fg='#fff', font=('Helvetica', 9), command=showalldata)
showallbtn.pack(side=tk.RIGHT, padx=5, pady=5)

searchE = tk.Entry(searchFrame, font=('Helvetica', 12))
searchE.pack(side=tk.RIGHT)

searchb = tk.Button(searchFrame, text='Search Manhwa', bg=bg_color, fg='#fff', font=('Helvetica', 9), command=search_manhwa)
searchb.pack(side=tk.RIGHT, padx=5, pady=5)



detailsbtn = tk.Button(root, text='See Information', padx=10, bg=bg_color, fg='#fff', font=('Helvetica', 12), width=14, relief=tk.RIDGE, bd=3, command=showdetails)
detailsbtn.place(x=860, y=628)


show_data()

root.bind('<ButtonRelease>', selected)
titleE.bind("<Return>", edit)
authorE.bind("<Return>", edit)
chaptersE.bind("<Return>", edit)
lastreadE.bind("<Return>", edit)
idE.bind("<Return>", edit)
searchE.bind("<Return>", search2)
statusB.bind("<<ComboboxSelected>>", edit)

root.mainloop()