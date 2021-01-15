from tkinter import *
import random
from timeit import default_timer as timer


intro_window = Tk()
intro_window.geometry("400x200")
x = 0

speed = IntVar()


def typing_app():
    global x
    global speed

    if x == 0:
        intro_window.destroy()
        x += 1

    words = ["Home", "Sensitive", " school", "Space"]

    word = random.choice(words)

    def check_speed():
        # Here we are checking if the word that was writtin is right or not
        # and if it is so we are taking the time from the start minus the time now
        if entry.get() == word:

            end = timer()

            speed.set(end - start)
            print(end - start)

        else:
            speed.set("Worng spiling")
            print("Wrong spiling")

    start = timer()

    # Here we are creating and designing the main window where we're going to type
    app_window = Tk()
    app_window.geometry("450x200")

    entry = Entry(app_window, textvariable=speed, width=25)
    entry.place(x=280, y=55)

    type_word = Label(app_window, text=word, font="times 20")
    type_word.place(x=150, y=10)

    start_label = Label(app_window, text="Start typing", font="times 20")
    start_label.place(x=10, y=50)

    done_button = Button(app_window, text="Done",
                         command=check_speed, width=12, bg="grey")
    done_button.place(x=245, y=85)

    re_start = Button(app_window, text="restart", width=12, command=typing_app)
    re_start.place(x=330, y=85)

    app_window.mainloop()


intro_label = Label(
    intro_window, text="Lets start typing ...", font="times 20")
intro_label.place(x=20, y=10)

go_button = Button(intro_window, text="Go",
                   command=typing_app, width=20, bg="grey")
go_button.place(x=150, y=80)
intro_window.mainloop()
