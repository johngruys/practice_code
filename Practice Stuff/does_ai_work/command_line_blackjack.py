import random

def create_deck():
    """Create a new shuffled deck of 52 cards."""
    deck = []
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def card_value(card):
    """Return the blackjack value for a card. Aces count as 11 initially."""
    rank, suit = card
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def hand_value(hand):
    """Calculate the total value of a hand, adjusting for Aces as needed."""
    total = 0
    aces = 0
    for card in hand:
        total += card_value(card)
        if card[0] == 'A':
            aces += 1
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def print_hand(name, hand, hide_first_card=False):
    """Utility function to display a hand of cards.
    
    If hide_first_card is True then the first card is hidden (used for the dealer).
    """
    if hide_first_card:
        # Hide the first card
        visible_cards = [f"{card[0]} of {card[1]}" for card in hand[1:]]
        print(f"{name}'s hand: [Hidden], " + ", ".join(visible_cards))
    else:
        cards_str = ", ".join([f"{card[0]} of {card[1]}" for card in hand])
        print(f"{name}'s hand: {cards_str} (Total: {hand_value(hand)})")

def player_turn(deck, player_hand):
    """Allow the player to hit or stand until they bust or choose to stop."""
    while True:
        current_value = hand_value(player_hand)
        if current_value >= 21:
            break
        move = input("Do you want to hit or stand? (h/s): ").lower().strip()
        if move == 'h':
            card = deck.pop()
            player_hand.append(card)
            print(f"You drew: {card[0]} of {card[1]}")
            print("Your hand:", ", ".join([f"{c[0]} of {c[1]}" for c in player_hand]),
                  f"(Total: {hand_value(player_hand)})")
        elif move == 's':
            break
        else:
            print("Invalid input. Please enter 'h' to hit or 's' to stand.")
    return player_hand

def dealer_turn(deck, dealer_hand):
    """Dealer reveals the hidden card and hits until reaching 17 or more."""
    while hand_value(dealer_hand) < 17:
        card = deck.pop()
        dealer_hand.append(card)
    return dealer_hand

def main():
    balance = 1000  # Starting balance for the player
    print("Welcome to Command Line Blackjack!")
    print("You start with a balance of", balance)

    while True:
        # Check if the player still has money to wager
        if balance <= 0:
            print("You're out of money! Game over.")
            break

        # Create a new deck for the round
        deck = create_deck()

        # Ask the player for a wager
        while True:
            try:
                wager = int(input(f"\nEnter your wager for this round (Available balance: {balance}): "))
                if wager <= 0:
                    print("Wager must be a positive integer.")
                elif wager > balance:
                    print("Wager cannot exceed your current balance.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid integer amount.")

        # Deal initial cards (2 for the player, 2 for the dealer)
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        print("\nDealing cards...")
        print_hand("Dealer", dealer_hand, hide_first_card=True)
        print_hand("Player", player_hand)

        # Player's turn
        player_turn(deck, player_hand)
        player_total = hand_value(player_hand)

        # Check if player busts
        if player_total > 21:
            print("You busted!")
            balance -= wager
        else:
            # Dealer's turn
            print("\nDealer reveals hidden card:")
            print_hand("Dealer", dealer_hand)
            dealer_turn(deck, dealer_hand)
            dealer_total = hand_value(dealer_hand)
            print("Dealer's final hand:", ", ".join([f"{card[0]} of {card[1]}" for card in dealer_hand]),
                  f"(Total: {dealer_total})")

            # Compare the totals to decide the outcome
            if dealer_total > 21:
                print("Dealer busted! You win!")
                winnings = wager * 2  # 2:1 odds payout
                balance += winnings
                print(f"You win {winnings}! Your new balance is {balance}.")
            elif dealer_total == player_total:
                print("Push. It's a tie! Your wager is returned.")
            elif player_total > dealer_total:
                print("You win!")
                winnings = wager * 2  # 2:1 odds payout
                balance += winnings
                print(f"You win {winnings}! Your new balance is {balance}.")
            else:
                print("Dealer wins.")
                balance -= wager

        print("Current balance:", balance)

        # Ask if the player wants to play another round
        play_again = input("\nPlay another round? (y/n): ").lower().strip()
        if play_again != 'y':
            print("Thanks for playing! Final balance:", balance)
            break

if __name__ == '__main__':
    main()
