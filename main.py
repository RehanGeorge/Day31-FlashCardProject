import random
import pandas
from tkinter import *

#Create the Dataframe of French and English words

try:
    french = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    french = pandas.read_csv("data/french_words.csv")
except pandas.errors.EmptyDataError:
    french = pandas.read_csv("data/french_words.csv")
finally:
    french_english_dictionary = french.to_dict(orient="records")
    random_word = {}

#Function to change text
def change_text():
    global random_word, flip_timer
    window.after_cancel(flip_timer)
    try:
        random_word = random.choice(french_english_dictionary)
    except IndexError:
        canvas.itemconfig(card_image, image=card_front_img)
        canvas.itemconfig(card_title, text="Congratulations!", fill="black")
        canvas.itemconfig(card_word, text="You got them all!", fill="black")
    else:
        canvas.itemconfig(card_image, image=card_front_img)
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_word, text=random_word["French"], fill="black")
        flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=random_word["English"], fill="white")

#Function for Button Yes
def button_yes():
    global random_word, flip_timer
    try:
        french_english_dictionary.remove(random_word)
    except ValueError:
        print("No remaining random words")
    change_text()

#Create a words to learn file
def exit_card():
    to_learn = french_english_dictionary
    to_learn_df = pandas.DataFrame.from_dict(to_learn)
    to_learn_df.to_csv("./data/words_to_learn.csv", index=False)
    window.destroy()

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

# window.minsize(width=1000, height=600)
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flash Card Project")

flip_timer = window.after(3000, func=flip_card)

#Create the Front Canvas
canvas = Canvas(width=800, height=526)
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
change_text()

#Create buttons
button_yes_image = PhotoImage(file="images/right.png")
button_yes = Button(image=button_yes_image, highlightthickness=0, command=button_yes)
button_yes.grid(column=1, row=1)

button_no_image = PhotoImage(file="images/wrong.png")
button_no = Button(image=button_no_image, highlightthickness=0, command=change_text)
button_no.grid(column=0, row=1)

button_exit = Button(text="Exit", highlightthickness=0, command=exit_card)
button_exit.config(padx=20, pady=20)
button_exit.grid(column=0,row=2, columnspan=2)

#Saves to file on pressing the 'x' button as well
window.protocol("WM_DELETE_WINDOW", exit_card)

window.mainloop()

