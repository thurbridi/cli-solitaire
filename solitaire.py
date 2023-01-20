import random
import os
import re
import time

# Cards console display
def card_number2value(n):
    if n == 1:
        return "A"
    elif n == 11:
        return "J"
    elif n == 12:
        return "Q"
    elif n == 13:
        return "K"
    else:
        return n


def card_content_string(value, suit_key):
    if value == "UNKNOWN" and suit_key == "UNKNOWN":
        return f"   ?"

    if value == "UNKNOWN":
        return f"   {suit_symbols[suit_key]}"

    color = suit_colors[suit_key] if suit_colors[suit_key] == "RED" else "WHITE"
    return f"{color_ansi_codes[color]}{card_values[value]:{2}} {suit_symbols[suit_key]:{1}}\033[39;49m"


def card_top_string(width=4):
    return f"╭{'─'*width}╮"


def card_bottom_string(width=4):
    return f"│{' '*4}│\n╰{'─'*width}╯"


def card_covered_string(value, suit_key):
    return f"{card_top_string()}\n│{card_content_string(value, suit_key)}│"


def card_whole_string(value, suit_key):
    return f"{card_top_string()}\n│{card_content_string(value, suit_key)}│\n{card_bottom_string()}"


def padding_string(lines, width=6):
    padding = ""
    for _ in range(lines):
        padding += " " * width + "\n"
    return padding


def stock_string(stock):
    if stock:
        return card_whole_string(*UNKNOWN_CARD)
    else:
        return padding_string(lines=4, width=6)


def pile_string(pile):
    if pile:
        return card_whole_string(*top_card(pile))
    else:
        return padding_string(lines=4, width=6)


def foundation_string(foundation, suit):
    if foundation:
        return card_whole_string(*top_card(foundation))
    else:
        colored_card = []
        for line in card_whole_string("UNKNOWN", suit).split("\n"):
            colored_card.append(
                "".join([color_ansi_codes["BLACK"], line, "\033[39;49m"])
            )
        return "\n".join(colored_card)


def stack_string(stack):
    lines = 0
    string = ""
    if stack:
        for card in stack[:-1]:
            string += card_covered_string(*card)
            string += "\n"
            lines += 2

        string += card_whole_string(*stack[-1])
        string += "\n"
        lines += 4

    string += padding_string(lines=28 - lines)

    return string


def print_example_stack():
    print(
        f"{card_covered_string(11, 'SPADES')}\n{card_covered_string(10, 'HEARTS')}\n{card_whole_string(9, 'CLUBS')}"
    )


def clear_lines(n=1):
    LINE_UP = "\033[1A"
    LINE_CLEAR = "\x1b[2K"
    for _ in range(n):
        print(LINE_UP, end=LINE_CLEAR)


UNKNOWN_CARD = ("UNKNOWN", "UNKNOWN")

suit_symbols = {
    "HEARTS": "\u2665",
    "DIAMONDS": "\u2666",
    "CLUBS": "\u2663",
    "SPADES": "\u2660",
}

suit_colors = {
    "HEARTS": "RED",
    "DIAMONDS": "RED",
    "CLUBS": "BLACK",
    "SPADES": "BLACK",
}

color_ansi_codes = {
    "RED": "\033[31m",
    "BLACK": "\033[30m",
    "WHITE": "\033[37m",
}

card_numbers = range(1, 14)

suits = ["CLUBS", "HEARTS", "SPADES", "DIAMONDS"]


card_values = {number: card_number2value(number) for number in card_numbers}


def print_stack(stack):
    print(stack_string(stack))


def print_game(tableau, stock, waste, foundations):
    header_string = ""
    for line in zip(
        stock_string(stock).split("\n"),
        *(pile_string(pile).split("\n") for pile in [waste, []]),
        *(
            foundation_string(foundation, suit).split("\n")
            for suit, foundation in foundations.items()
        ),
    ):
        header_string += "".join(line)
        header_string += "\n"

    tableau_string = ""
    for line in zip(
        *(stack_string(tableau[column]).split("\n") for column in range(7))
    ):
        tableau_string += "".join(line)
        tableau_string += "\n"

    print("".join([header_string, tableau_string]))


# Solitaire rules
def top_card(stack):
    if len(stack) > 0:
        return stack[-1]
    return None


def card_value(card):
    if card:
        return card[0]


def card_suit(card):
    if card:
        return card[1]


def can_move_stack(n, stack_a, stack_b):
    if not stack_a or n > len(stack_a):
        return False

    value_a, suit_a = stack_a[-n]

    if not stack_b:
        if value_a == 13:
            return True

    else:
        value_b, suit_b = stack_b[-1]
        if value_a == value_b - 1 and suit_colors[suit_a] != suit_colors[suit_b]:
            return True


def can_move_to_foundation(card, foundations):
    if not card:
        return

    value, suit = card

    foundation = foundations[suit]
    if len(foundation) == 0 and value == 1:
        return True
    if len(foundation) > 0:
        return card_value(top_card(foundation)) == value - 1


def move_stack(n, stack_a, stack_b, deck):
    aux = []
    for _ in range(n):
        aux.append(stack_a.pop())

    while aux:
        stack_b.append(aux.pop())

    if stack_a:
        if top_card(stack_a) == UNKNOWN_CARD:
            stack_a.pop()
            stack_a.append(deck.pop())


def init_tableau(deck):
    tableau = []
    for column_number in range(7):
        unknowns = column_number
        column = []

        for _ in range(unknowns):
            column.append(UNKNOWN_CARD)
        column.append(top_card(deck))
        deck.pop()

        tableau.append(column)

    return tableau


def take_from_stock(stock, waste, n=1):
    if stock:
        for _ in range(min(n, len(stock))):
            waste.append(stock.pop())
    elif waste:
        # Stock is empty but there are cards in the waste, turn waste into stock
        while waste:
            stock.append(waste.pop())
        take_from_stock(stock, waste, n)
    else:
        return


def parse_move(deck, tableau, stock, waste, foundations, move):
    # TODO: Move from foundation to tableau
    move = move.lower()
    if move == "exit":
        quit(0)

    if move == "reset":
        deck, tableau, stock, waste, foundations = reset_game()
        return deck, tableau, stock, waste, foundations

    if move == "win":
        if len(deck) == 0 and len(stock) == 0 and len(waste) == 0:
            tableau, stock, waste, foundations = win_animation(
                deck, tableau, stock, waste, foundations
            )
            return deck, tableau, stock, waste, foundations

    if move == "s":
        take_from_stock(stock, waste, n=1)
        return deck, tableau, stock, waste, foundations

    match = re.match(r"^(\d+) from (\d) to (\d)", move)
    if match:
        n = int(match.group(1))
        from_ = int(match.group(2)) - 1
        to = int(match.group(3)) - 1
        if can_move_stack(n, tableau[from_], tableau[to]):
            move_stack(n, tableau[from_], tableau[to], deck)
        return deck, tableau, stock, waste, foundations

    match = re.match(r"^from (\d|w) to (\d|f)", move)
    if match:
        from_ = match.group(1)
        to = match.group(2)

        # waste to foundation
        if from_ == "w" and to == "f":
            if waste:
                if can_move_to_foundation(top_card(waste), foundations):
                    move_stack(1, waste, foundations[card_suit(top_card(waste))], deck)
            return deck, tableau, stock, waste, foundations

        # waste to tableau
        if from_ == "w":
            to = int(to) - 1
            if can_move_stack(1, waste, tableau[to]):
                move_stack(1, waste, tableau[to], deck)
            return deck, tableau, stock, waste, foundations

        # tableau to foundation
        if to == "f":
            from_ = int(from_) - 1
            if can_move_to_foundation(top_card(tableau[from_]), foundations):
                move_stack(
                    1,
                    tableau[from_],
                    foundations[card_suit(top_card(tableau[from_]))],
                    deck,
                )
            return deck, tableau, stock, waste, foundations

        # tableau to tableau
        from_ = int(from_) - 1
        to = int(to) - 1
        if can_move_stack(1, tableau[from_], tableau[to]):
            move_stack(1, tableau[from_], tableau[to], deck)
        return deck, tableau, stock, waste, foundations
    return deck, tableau, stock, waste, foundations


def win_animation(deck, tableau, stock, waste, foundations):
    while sum((len(foundation) for foundation in foundations.values())) < 52:
        card = None
        for suit, foundation in foundations.items():
            if len(foundation) == 0:
                card = (0, suit)
                break

            topmost_card = top_card(foundation) or (1, suit)
            if card is None or card_value(card) > card_value(topmost_card):
                card = topmost_card

        for column in tableau:
            if len(column) == 0:
                continue

            if (
                card_suit(top_card(column)) == card_suit(card)
                and card_value(top_card(column)) == card_value(card) + 1
            ):
                move_stack(1, column, foundations[card_suit(card)], deck)

        os.system("clear")
        print_game(tableau, stock, waste, foundations)
        time.sleep(0.2)

    return tableau, stock, waste, foundations


def reset_game():
    deck = [(value, suit) for suit in suits for value in card_numbers]
    random.shuffle(deck)

    tableau = init_tableau(deck)
    stock = deck[:24]
    deck = deck[24:]

    waste = []
    foundations = {suit: [] for suit in suits}

    return deck, tableau, stock, waste, foundations


def game_loop(deck, tableau, stock, waste, foundations):
    while True:
        os.system("clear")
        print_game(tableau, stock, waste, foundations)
        move = input("move ")
        deck, tableau, stock, waste, foundations = parse_move(
            deck, tableau, stock, waste, foundations, move
        )


if __name__ == "__main__":
    deck, tableau, stock, waste, foundations = reset_game()
    game_loop(deck, tableau, stock, waste, foundations)
