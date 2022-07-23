from tkinter import *
from tkinter import messagebox
import json
from random import choice
from symbol import Symbol
from kanji import Kanji


# ---------------------------- IMPORT DATABASE (at startup) ------------------------------- #
symbols_list = []
total_num_symbols = 0
# Import hiragana
with open("hiragana.json", "r") as hiragana_file:
    hiragana_db = json.load(hiragana_file)  # Load JSON hiragana DB
    symbols_list.append([Symbol(hiragana, hiragana_db[hiragana]["romaji"]) for
                         hiragana in hiragana_db])  # Create symbol objects from DB
    total_num_symbols += len(hiragana_db)

# Import katakana
with open("katakana.json", "r") as katakana_file:
    katakana_db = json.load(katakana_file)  # Load JSON katakana DB
    symbols_list.append([Symbol(katakana, katakana_db[katakana]["romaji"]) for
                         katakana in katakana_db])  # Create symbol objects from DB
    total_num_symbols += len(katakana_db)

# Import kanji
with open("kanji.json", "r") as kanji_file:
    kanji_db = json.load(kanji_file)
    symbols_list.append([Kanji(kanji, kanji_db[kanji]["reading"], kanji_db[kanji]["meaning"]) for
                         kanji in kanji_db])
    total_num_symbols += len(kanji_db)


# ---------------------------- NEW SYMBOL METHOD ------------------------------- #
def get_random_symbol():
    symbol_choice = choice(symbols_list)  # Choose which alphabet to use
    symbol = choice(symbol_choice)  # Choose which character to use

    return symbol


# ---------------------------- CHECK ANSWER ------------------------------- #
def check_answer(event=None):
    global current_symbol

    # Get user answer
    answer = answer_entry.get().lower()

    # Get correct answer
    correct_answer = current_symbol.romaji

    if answer and answer in correct_answer:  # Used "in" to allow multiple readings
        messagebox.showinfo(title="Correct Answer!", message="Correct!")
        setup_new_card()
    else:
        messagebox.showerror(title="Wrong answer...", message=f"Wrong answer.\nCorrect answer: {correct_answer}")

    # Clear last answer from text box
    answer_entry.delete(0, END)
    answer_entry.focus_force()


correct_answers = []


def setup_new_card():
    global current_symbol

    correct_answers.append(current_symbol)

    # Check if all the cards were guessed correctly
    if len(correct_answers) == total_num_symbols:
        messagebox.showinfo(title="All done!", message="You completed all the cards!")
        window.quit()
    else:
        # Get new symbol (prevent it from being the same one again)
        previous_symbol = current_symbol
        while current_symbol == previous_symbol or current_symbol in correct_answers:
            current_symbol = get_random_symbol()

        if isinstance(current_symbol, Kanji):
            # Choose between symbol and meaning
            symbol_label.config(text=choice([current_symbol.symbol,
                                             choice(current_symbol.meaning)]))  # Allow different meanings
        else:
            symbol_label.config(text=current_symbol.symbol)

        # Update progress label
        progress_label.config(text=f"{len(correct_answers)}/{total_num_symbols}")


# ---------------------------- UI SETUP ------------------------------- #

# Window setup
window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=30)
window.bind('<Return>', check_answer)

# Symbol setup
current_symbol = get_random_symbol()
symbol_label = Label(text=current_symbol.symbol, font=("Arial", 30, "bold"))
symbol_label.config(pady=40)
symbol_label.grid(row=1, column=1)

# Answer setup
answer_entry = Entry(width=20)
answer_entry.focus()
answer_entry.grid(row=2, column=1)

submit_answer_button = Button(text="Submit Answer", width=10, command=check_answer)
submit_answer_button.grid(row=3, column=1)

# Progress tracker
progress_label = Label(text=f"{len(correct_answers)}/{total_num_symbols}", font=("Arial", 20, "bold"))
progress_label.grid(row=0, column=1)

window.mainloop()
