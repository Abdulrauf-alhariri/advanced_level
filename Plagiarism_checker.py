from textblob import TextBlob, blob
from tkinter import *
from apiclient.discovery import build
from bs4 import BeautifulSoup
import requests


# Here we are creating a resouce object so we can use it to send a request
resource = build("customsearch", "v1", developerKey=api_key).cse()


# print(pages_des)


root = Tk()
root.title("Plagiarism checker")
root.geometry("500x600")


show = StringVar()


def clear():
    my_text.delete(1.0, END)


def check():
    global results

    text = my_text.get(1.0, END)

    # Here I'm creating a blob object
    blob = TextBlob(text)
    text_list = []

    for item in blob.sentences:
        text_list.append(str(item.replace(".", "")))

    # Here we are checking the plagiarism
    illegal = []
    for sentence in text_list:
        pages = []
        pages_des = []
        for i in range(1, 20, 10):
            try:
                results = resource.list(q=sentence,
                                        cx="ea525f8631b79cc8c", start=i).execute()
                pages.append(results["items"])
            except:
                pass

        for page in pages:
            for item in page:
                try:
                    title = item["pagemap"]
                    des = item["pagemap"]["metatags"][0]["og:description"]
                    länk = item["pagemap"]["metatags"][0]["og:url"]
                    pages_des.append(des)
                except:
                    pass

        for des in pages_des:
            if sentence in des:
                illegal.append(sentence)

    result = len(illegal) / len(text_list)
    show.set(f"{result} %")


if __name__ == "__main__":

    # Here we are creating the textfield to get the text that we want to check
    my_text = Text(root, width=50, height=30, font=("Helvetica", 10))
    my_text.pack(pady=20, padx=20)

    # Creating a frame for the buttons
    btn_frame = Frame(root)
    btn_frame.pack()

    # A button to clear the textfield
    btn_clear = Button(btn_frame, text="Clear text", command=clear)
    btn_clear.grid(row=0, column=0)

    # A button to check the text
    btn_check = Button(btn_frame, text="Check text", command=check)
    btn_check.grid(row=0, column=1, padx=20)

    # An entry and a label to show the result
    result_label = Label(btn_frame, text="Plagiarism: ")
    result_label.grid(row=1, column=0, pady=10)

    result_entry = Entry(btn_frame, textvariable=show)
    result_entry.grid(row=1, column=1)


root.mainloop()
