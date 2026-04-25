"""Implementation of a deck of cards for object-oriented design.

This module provides classes to represent a standard 52-card deck,
including suits, card ranks, individual cards, and a deck with
shuffle and deal functionality.
"""

import random
from enum import Enum


class Suit(Enum):
    """Represents the four suits in a standard deck."""
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3


class Card:
    """Represents a single playing card with a suit and value."""

    FACE_CARDS = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}

    def __init__(self, value: int, suit: Suit):
        """Initialize a card with a value (1-13) and suit.

        Args:
            value: Integer from 1 (Ace) to 13 (King).
            suit: A Suit enum value.
        """
        if not 1 <= value <= 13:
            raise ValueError(f"Card value must be between 1 and 13, got {value}")
        self.value = value
        self.suit = suit

    def is_face_card(self) -> bool:
        """Return True if the card is a face card (Ace, Jack, Queen, King)."""
        return self.value in self.FACE_CARDS

    def __repr__(self) -> str:
        name = self.FACE_CARDS.get(self.value, str(self.value))
        return f"{name} of {self.suit.name.capitalize()}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value and self.suit == other.suit


class Deck:
    """Represents a standard 52-card deck.

    Supports shuffling, dealing single cards, and dealing hands.
    """

    def __init__(self):
        """Initialize a full, ordered 52-card deck."""
        self.cards = [
            Card(value, suit)
            for suit in Suit
            for value in range(1, 14)
        ]
        self.dealt_index = 0  # Tracks the next card to be dealt

    def shuffle(self) -> None:
        """Shuffle the remaining undealt cards in the deck."""
        undealt = self.cards[self.dealt_index:]
        random.shuffle(undealt)
        self.cards[self.dealt_index:] = undealt

    def deal_one(self) -> Card:
        """Deal a single card from the top of the deck.

        Returns:
            The next available Card.

        Raises:
            ValueError: If there are no remaining cards.
        """
        if not self.remaining_cards():
            raise ValueError("No cards remaining in the deck.")
        card = self.cards[self.dealt_index]
        self.dealt_index += 1
        return card

    def deal_hand(self, number: int) -> list:
        """Deal a hand of the specified number of cards.

        Args:
            number: The number of cards to deal.

        Returns:
            A list of Card objects.

        Raises:
            ValueError: If there are not enough cards remaining.
        """
        if self.remaining_cards() < number:
            raise ValueError(
                f"Not enough cards: requested {number}, "
                f"but only {self.remaining_cards()} remaining."
            )
        hand = self.cards[self.dealt_index: self.dealt_index + number]
        self.dealt_index += number
        return hand

    def remaining_cards(self) -> int:
        """Return the number of undealt cards remaining."""
        return len(self.cards) - self.dealt_index

    def reset(self) -> None:
        """Reset the deck so all cards are available again."""
        self.dealt_index = 0

    def __len__(self) -> int:
        return self.remaining_cards()

    def __repr__(self) -> str:
        return f"Deck({self.remaining_cards()} cards remaining)"


if __name__ == '__main__':
    deck = Deck()
    print(f"Created: {deck}")

    deck.shuffle()
    print("Deck shuffled.")

    hand = deck.deal_hand(5)
    print(f"Dealt hand: {hand}")
    print(f"Remaining: {deck}")

    card = deck.deal_one()
    print(f"Dealt one card: {card}")
    print(f"Remaining: {deck}")
