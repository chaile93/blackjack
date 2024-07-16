import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Player:
    def __init__(self):
        self.hand = []

    def receive_card(self, card):
        self.hand.append(card)

    def calculate_hand_value(self):
        value = 0
        num_aces = 0
        for card in self.hand:
            if card.rank.isdigit():
                value += int(card.rank)
            elif card.rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.rank == 'Ace':
                num_aces += 1
                value += 11  # Aces initially count as 11
        # Adjust for Aces
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value

    def display_hand(self, show_all=False):
        if show_all:
            return ', '.join(str(card) for card in self.hand)
        else:
            return str(self.hand[0])  # Show only the first card

    def clear_hand(self):
        self.hand = []

class Dealer(Player):
    def __init__(self):
        super().__init__()

    def display_hand(self, show_all=False):
        if show_all:
            return super().display_hand(show_all=True)
        else:
            return "Hidden card, " + str(self.hand[1])

    def should_hit(self):
        return self.calculate_hand_value() < 17  # Dealer hits on 16 or less

def blackjack_game():
    deck = Deck()
    deck.shuffle()

    player = Player()
    dealer = Dealer()

    # Deal initial cards
    player.receive_card(deck.deal_card())
    dealer.receive_card(deck.deal_card())
    player.receive_card(deck.deal_card())
    dealer.receive_card(deck.deal_card())

    print("Welcome to Blackjack!")
    print(f"Player's hand: {player.display_hand()}")
    print(f"Dealer's hand: {dealer.display_hand()}")

    # Player's turn
    while player.calculate_hand_value() < 21:
        action = input("Do you want to hit or stand? (h/s): ").lower()
        if action == 'h':
            player.receive_card(deck.deal_card())
            print(f"Player's hand: {player.display_hand()}")
        elif action == 's':
            break

    player_value = player.calculate_hand_value()

    if player_value > 21:
        print("Bust! You lose.")
    else:
        # Dealer's turn
        while dealer.should_hit():
            dealer.receive_card(deck.deal_card())
        dealer_value = dealer.calculate_hand_value()

        print(f"Dealer's hand: {dealer.display_hand(show_all=True)}")

        if dealer_value > 21:
            print("Dealer busts! You win.")
        elif dealer_value == player_value:
            print("Game tied.")
        elif dealer_value > player_value:
            print("Dealer wins.")
        else:
            print("Player wins!")

    player.clear_hand()
    dealer.clear_hand()

# Run the game
if __name__ == "__main__":
    while True:
        blackjack_game()
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            break

    print("Thanks for playing Blackjack!")
