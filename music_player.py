from tkinter import *
from pygame.locals import *
import pygame as pg
import os

root = Tk()
root.geometry("400x400")
pg.init()

# Creating the frame that we gonna need in this project
entry_frame = Frame(root)
buttons_frame = Frame(root)

var = StringVar()

# Creating a frame for the list box and creating a scroll bar for the list box
list_frame = Frame(root)
my_scrollbar = Scrollbar(list_frame, orient=VERTICAL)

# Creating a list box
my_listbox = Listbox(list_frame, width=50, yscrollcommand=my_scrollbar.set)

# Connecting the croll bar with the list box and putting the scroll bar on the right side of the frame
my_scrollbar.config(command=my_listbox.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_listbox.pack(pady=20)
list_frame.grid(row=0, column=0, padx=10)

# Creating the entry where we are going to displat the chosen song
my_entry = Entry(entry_frame, textvariable=var,  font=("default", 20))
my_entry.pack()
entry_frame.grid(row=1, column=0, pady=10, padx=10)


def add_songs(path):
    songs = []

    for root, dir, files in os.walk(path):
        for file in files:
            songs.append(os.path.join(root, file))

    for song in songs:
        my_listbox.insert(END, song)

    print(songs)


def play():
    pg.mixer.music.load(my_listbox.get(ANCHOR))
    pg.mixer.music.play()
    var.set(my_listbox.get(ANCHOR))


def stop():
    pg.mixer.music.stop()


def pause():
    pg.mixer.music.pause()


def unpause():
    pg.mixer.music.unpause()


if __name__ == "__main__":
    add_songs("C:\\songs")

    # Creating the buttons for the music player
    play_button = Button(buttons_frame, text="Play",
                         command=play, font=("default", 15))
    play_button.grid(row=0, column=0)

    pause_button = Button(buttons_frame, text="Pause",
                          command=pause, font=("default", 15))
    pause_button.grid(row=0, column=1, padx=2)

    unpause_button = Button(buttons_frame, text="Unpause",
                            command=unpause, font=("default", 15))
    unpause_button.grid(row=0, column=2, padx=2)

    stop_button = Button(buttons_frame, text="Stop",
                         command=stop, font=("default", 15))
    stop_button.grid(row=0, column=3, padx=2)

    buttons_frame.grid(row=2, column=0, pady=10)

root.mainloop()
