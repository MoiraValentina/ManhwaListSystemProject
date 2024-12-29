import tkinter as tk

# Create the main application window
root = tk.Tk()
root.geometry("600x400")

# Load the background image
background_image = tk.PhotoImage(file="Python PROJECTS/MY SYSTEM/bg.png")

# Create a Canvas to display the background image
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack(fill="both", expand=True)

# Add the background image to the Canvas
canvas.create_image(0, 0, image=background_image, anchor="nw")

# Place widgets on top of the Canvas
label = tk.Label(root, text="Welcome to my App", font=("Arial", 24), bg="white")
button = tk.Button(root, text="Click Me", font=("Arial", 14))

# Use the Canvas to position the widgets
canvas.create_window(300, 50, window=label)
canvas.create_window(300, 150, window=button)

# Start the application loop
root.mainloop()
