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
        random.shuffle(not_box1)
        self.box1 = self.box1 + sorted(not_box1, key=lambda flash_card: flash_card.box)[:no_cards]
        for card in self.box1:
            card.box = 1
    
        
    def draw_next_card(self):
        
        def weighted_random_choice(lst):
            if len(lst) <= 1:
                return lst[0]
            weights = range(len(lst)-1, -1, -1)
            chosen = random.choices(lst, weights=weights, k=1)[0]
            lst.remove(chosen)
            lst.append(chosen)
            return chosen
        
        r = random.random()
        if len(self.box3) > 0 and r < 0.08: #random chance to draw mastered card
            self.active_card = weighted_random_choice(self.box3)
        elif len(self.box2) > 0 and r < 0.15: #random chance to draw learned card
            self.active_card = weighted_random_choice(self.box2)
        elif len(self.box1) > 3:
            self.active_card = weighted_random_choice(self.box1)
        elif 0 < len(self.box1) <= 3 and len(self.box2) > 0:
            if r < 0.8:
                self.active_card = weighted_random_choice(self.box2)
            else:
                self.active_card = weighted_random_choice(self.box1)
        elif 0 < len(self.box1) <= 3 and len(self.box3) > 0:
            if r < 0.8:
                self.active_card = weighted_random_choice(self.box3)
            else:
                self.active_card = weighted_random_choice(self.box1)
        elif len(self.box1) == 0 and len(self.box2) > 3:
            self.active_card = weighted_random_choice(self.box2)
        elif len(self.box1) == 0 and  0 < len(self.box2) <= 3:
            if r < 0.8:
                self.active_card = weighted_random_choice(self.box3)
            else:
                self.active_card = weighted_random_choice(self.box2)
        elif len(self.box2) == 0 and len(self.box3) > 0:
            self.active_card = weighted_random_choice(self.box3)
        else:
            self.active_card = FlashCard("-1", "No Cards", "No Cards", "")
        
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
            
    def save_progress(self):
        vocab_data = {}
        file_path = "./saves/" + self.name + "_save.json"
        for flash_card in self.flash_cards:
            vocab_data[flash_card.id] = {
                "chinese":              flash_card.chinese,
                "pinyin":               flash_card.pinyin,
                "english":              flash_card.english,
                "box" :                 flash_card.box,
                "active_score" :        flash_card.active_score,
                "correct_guesses" :     flash_card.correct_guesses,
                "total_guesses" :       flash_card.total_guesses
            }
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(vocab_data, file, ensure_ascii=False, indent=4)
                #print("Data saved successfully.")
        except Exception as e:
            print(f"Saving failed! Error: {e}")
    
def create_deck_from_json(path="hsk1_vocab.json", name='default', load_progress=False):
    with open(path, 'r', encoding='utf-8') as file:
        vocab_data = json.load(file)

    flash_card_deck = FlashCardDeck(name=name)
    
    if load_progress:
        for idx, data in vocab_data.items():
            flash_card = FlashCard(idx, data["chinese"], data["pinyin"], data["english"],
                                   box=int(data["box"]), active_score=int(data["active_score"]),
                                   correct_guesses=int(data["correct_guesses"]), total_guesses=int(data["total_guesses"]))
            flash_card_deck.add_flash_card(flash_card)
    else:
        for idx, data in vocab_data.items():
            flash_card = FlashCard(idx, data["chinese"], data["pinyin"], data["english"])
            flash_card_deck.add_flash_card(flash_card)
    
    return flash_card_deck
    
if __name__ == "__main__":
    flash_card_deck = create_deck_from_json()
    flash_card_deck.get_card_set_box1()
    flash_card_deck.draw_next_card()
    flash_card_deck.print_card()
    
    for i in [0,1,2]:
        flash_card_deck.increase_score()
    
    print(len(flash_card_deck.box1))
    print(flash_card_deck.box2[0])
    
    flash_card_deck.save_progress()
    
    flash_card_deck = create_deck_from_json(path="./saves/default_save.json", load_progress=True)
    print(len(flash_card_deck.box1))
    print(len(flash_card_deck.box2))
    flash_card_deck.get_card_set_box1()
    flash_card_deck.draw_next_card()
    flash_card_deck.print_card()
    
    for i in [0,1,2]:
        flash_card_deck.increase_score()
    
    print(len(flash_card_deck.box1))
    print(len(flash_card_deck.box2))
    print(flash_card_deck.box2[0])
    