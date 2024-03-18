import customtkinter as ctk
import flashcards

def refresh_overall_stats():
    l_unseen_cards.configure(text=deck.get_no_unseen())
    l_learn_cards.configure(text=len(deck.box1))
    l_learned_cards.configure(text=len(deck.box2))
    l_master_cards.configure(text=len(deck.box3))
    print(deck.active_card.active_score)

def refresh_word_stats():
    return

def b_answer_show(relx=0.5, rely=0.6):
    b_answer.place(relx=relx, rely=rely, anchor=ctk.CENTER)
    
def b_right_show(relx=0.3, rely=0.6):
    b_right.place(relx=relx, rely=rely, anchor=ctk.CENTER)

def b_wrong_show(relx=0.7, rely=0.6):
    b_wrong.place(relx=relx, rely=rely, anchor=ctk.CENTER)
    
def b_back_show(relx=0.1, rely=0.1):
    b_back.place(relx=relx, rely=rely, anchor=ctk.CENTER)
    
def b_draw_cards_show():
    b_draw_cards.place(relx=0.85, rely=0.1, anchor=ctk.CENTER)
    
def build_word_page():
    b_right.place_forget()
    b_wrong.place_forget()
    b_back.place_forget()
    b_answer_show()
    b_draw_cards_show()

def build_answer_page():
    b_answer.place_forget()
    b_draw_cards.place_forget()
    b_right_show()
    b_wrong_show()
    b_back_show()


# Function to be called when the button is clicked
def b_answer_click():
    l_main_word.configure(text=deck.get_english())
    l_second_word.configure(text="")
    l_main_word.configure(font=("Arial", 50))
    build_answer_page()
    
def b_right_click():
    deck.increase_score()
    deck.draw_next_card()
    l_main_word.configure(text=deck.get_chinese())
    l_second_word.configure(text=deck.get_pinyin())
    refresh_overall_stats()
    build_word_page()
    
def b_wrong_click():
    deck.decrease_score()
    deck.draw_next_card()
    l_main_word.configure(text=deck.get_chinese())
    l_second_word.configure(text=deck.get_pinyin())
    refresh_overall_stats()
    build_word_page()
    
    
def b_back_click():
    l_main_word.configure(text=deck.get_chinese())
    l_second_word.configure(text=deck.get_pinyin())
    build_word_page()
    
def b_draw_cards_click():
    deck.get_card_set_box1()
    deck.draw_next_card()
    l_main_word.configure(text=deck.get_chinese())
    l_second_word.configure(text=deck.get_pinyin())
    refresh_overall_stats()

deck = flashcards.create_deck_from_json()

# Set the theme and color scheme
ctk.set_appearance_mode("light")  # "light" or "dark"
ctk.set_default_color_theme("blue")  # Other themes available

# Create the main window
main_window = ctk.CTk()
main_window.title("HSK1 Flashcards")
main_window.geometry("400x400")

# Create a label with large text in the middle of the window
l_main_word = ctk.CTkLabel(main_window, text=deck.get_chinese(), font=("Arial", 72))
l_main_word.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

l_second_word = ctk.CTkLabel(main_window, text=deck.get_pinyin(), font=("Arial", 18))
l_second_word.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

# Create a button at the center bottom of the window
b_answer = ctk.CTkButton(main_window, text="Answer", command=b_answer_click)
b_answer_show()

b_right = ctk.CTkButton(main_window, text="Right", command=b_right_click, fg_color="#32CD32")
b_wrong = ctk.CTkButton(main_window, text="Wrong", command=b_wrong_click, fg_color="#FF6347")

b_back = ctk.CTkButton(main_window, text="<", command=b_back_click, fg_color="lightgrey", width=30, height=30)
b_draw_cards = ctk.CTkButton(main_window, text="Draw Cards", command=b_draw_cards_click, fg_color="lightgrey", width=50)
b_draw_cards_show()

# Overall Stats Label
l_title_unseen_cards = ctk.CTkLabel(main_window, text='Unseen Cards', font=("Arial", 12))
l_title_unseen_cards.place(relx=0.15, rely=0.75, anchor=ctk.CENTER)
l_unseen_cards = ctk.CTkLabel(main_window, text=deck.get_no_unseen(), font=("Arial", 12))
l_unseen_cards.place(relx=0.15, rely=0.8, anchor=ctk.CENTER)

l_title_learn_cards = ctk.CTkLabel(main_window, text='Learning Now', font=("Arial", 12))
l_title_learn_cards.place(relx=0.3766, rely=0.75, anchor=ctk.CENTER)
l_learn_cards = ctk.CTkLabel(main_window, text=len(deck.box1), font=("Arial", 12))
l_learn_cards.place(relx=0.3766, rely=0.8, anchor=ctk.CENTER)

l_title_learned_cards = ctk.CTkLabel(main_window, text='Learned Cards', font=("Arial", 12))
l_title_learned_cards.place(relx=0.6233, rely=0.75, anchor=ctk.CENTER)
l_learned_cards = ctk.CTkLabel(main_window, text=len(deck.box2), font=("Arial", 12))
l_learned_cards.place(relx=0.6233, rely=0.8, anchor=ctk.CENTER)

l_title_master_cards = ctk.CTkLabel(main_window, text='Mastered Cards', font=("Arial", 12))
l_title_master_cards.place(relx=0.85, rely=0.75, anchor=ctk.CENTER)
l_master_cards = ctk.CTkLabel(main_window, text=len(deck.box3), font=("Arial", 12))
l_master_cards.place(relx=0.85, rely=0.8, anchor=ctk.CENTER)

deck.get_card_set_box1()
deck.draw_next_card()
refresh_overall_stats()

# Start the GUI event loop
main_window.mainloop()