from tkinter import *
from PIL import ImageTk
import PIL.Image
from tkinter import filedialog


root = Tk()
root.title("File explorer")
root.geometry("500x500")
root.config(background="white")


def open():
    global my_image
    filename = filedialog.askopenfilename(initialdir="", title="Select file", filetypes=(
        ("Png files", "*.png"), ("All files", "*.*")))

    intro_label.configure(text="File opend: " + filename)

    my_image = ImageTk.PhotoImage(PIL.Image.open(filename))
    my_image_label = Label(image=my_image)
    my_image_label.grid(row=3, column=1)


intro_label = Label(
    root, text="File exporer using python", font=("Arial", 15, ""), width=50, height=4, fg="blue")
intro_label.grid(row=0, column=1)

open_browser = Button(root, text="Browser", command=open)
open_browser.grid(row=1, column=1)

exit_button = Button(root, text="Excit", command=root.destroy)
exit_button.grid(row=2, column=1)

mainloop()
