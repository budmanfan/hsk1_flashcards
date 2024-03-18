import json
import random

class FlashCard:
    def __init__(self, id, chinese, pinyin, english, box=0, active_score=0, correct_guesses=0, total_guesses=0):
        self.id = id
        self.chinese = chinese
        self.pinyin = pinyin
        self.english = english
        self.box = box
        self.active_score = active_score
        self.correct_guesses = correct_guesses
        self.total_guesses = total_guesses
    
    def __str__(self):
        return f"ID: {self.id} \tCN: {self.chinese} \tPY: {self.pinyin} \tEN: {self.english}"


class FlashCardDeck:
    def __init__(self, name=None):
        self.name = name
        self.flash_cards = []
        self.active_card = FlashCard("-1", "", "", "")
        self.box1 = []
        self.box2 = []
        self.box3 = []
        
    def add_flash_card(self, flash_card):
        self.active_card = flash_card
        self.flash_cards.append(self.active_card)
        if flash_card.box == 1:
            self.box1.append(self.active_card)
        if flash_card.box == 2:
            self.box2.append(self.active_card)
        if flash_card.box == 3:
            self.box3.append(self.active_card)
        
    def print_card(self):
        print(self.active_card)
    
    def draw_random_card(self):
        self.active_card = random.choice(self.flash_cards)
    
    def get_chinese(self):
        return self.active_card.chinese
    
    def get_pinyin(self):
        return self.active_card.pinyin
    
    def get_english(self):
        return self.active_card.english
    
    def get_no_unseen(self):
        return sum(card.box == 0 for card in self.flash_cards)
    
    def get_card_set_box1(self, no_cards=10):
        not_box1 = [card for card in self.flash_cards if card not in self.box1]
        self.box1 = self.box1 + sorted(not_box1, key=lambda flash_card: flash_card.box)[:no_cards]
        for card in self.box1:
            card.box = 1
        
    def draw_next_card(self):
        r = random.random()
        if len(self.box1) == 0:
            self.active_card = FlashCard("-1", "No more cards", "No more cards", "")
        elif len(self.box3) > 0 and r < 0.05:
            self.active_card = random.choice(self.box3)
        elif len(self.box2) > 0 and r < 0.2:
            self.active_card = random.choice(self.box2)
        else:
            self.active_card = random.choice(self.box1)
        
    def increase_score(self):
        self.active_card.active_score += 1
        self.active_card.total_guesses += 1
        self.active_card.correct_guesses += 1
        if self.active_card.active_score >= 3:
            self.active_card.active_score = 0
            if self.active_card in self.box2:
                self.box2.remove(self.active_card)
                self.box3.append(self.active_card)
                self.active_card.box = 3
            if self.active_card in self.box1:
                self.box1.remove(self.active_card)
                self.box2.append(self.active_card)
                self.active_card.box = 2
    
    def decrease_score(self):
        self.active_card.active_score -= 1
        self.active_card.total_guesses += 1
        if self.active_card.active_score < 0:
            self.active_card.active_score = 0
        if self.active_card in self.box2:
            self.active_card.active_score = 0
            self.box2.remove(self.active_card)
            self.box1.append(self.active_card)
            self.active_card.box = 1
        if self.active_card in self.box3:
            self.active_card.active_score = 0
            self.box3.remove(self.active_card)
            self.box1.append(self.active_card)
            self.active_card.box = 1
            
    def save_words(self):
        return
    
    
with open("hsk1_vocab.json", 'r', encoding='utf-8') as file:
    vocab_data = json.load(file)

flash_card_deck = FlashCardDeck()

for idx, data in vocab_data.items():
    flash_card = FlashCard(idx, data["chinese"], data["pinyin"], data["english"])
    flash_card_deck.add_flash_card(flash_card)
    
if __name__ == "__main__":
    flash_card_deck.get_card_set_box1()
    flash_card_deck.draw_next_card()
    flash_card_deck.print_card()
    
    for i in [0,1,2]:
        flash_card_deck.increase_score()
    
    print(len(flash_card_deck.box1))
    print(flash_card_deck.box2[0])