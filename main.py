from random import choices, shuffle
from os import system, name

SUITS = ("Coeur", "Carreau", "Trèfles", "Pic")
RANKS = (
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Valet",
    "Dame",
    "Roi",
    "As",
)
VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Valet": 10,
    "Dame": 10,
    "Roi": 10,
    "As": 11,
}
PLAYING = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    """ Création du jeu de cartes et distribution de deux cartes au joueur et au croupier """

    def __init__(self):
        self.deck = []
        self.joueur = []
        self.dealer = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append((suit, rank))

    def shuffle(self):
        """ Mélanger les cartes du deck """
        shuffle(self.deck)

    def deal_carte(self):
        """ Distribuer les cartes """
        self.joueur = choices(self.deck, k=2)
        self.suppCarte(self.joueur)
        self.dealer = choices(self.deck, k=2)
        self.suppCarte(self.dealer)  # Delete Drawn carte
        return self.joueur, self.dealer

    def suppCarte(self, total_drawn):
        """ Supprimer les cartes tirées du deck """
        try:
            for i in total_drawn:
                self.deck.remove(i)
        except ValueError:
            pass


class Hand:
    """ Ajouter les valeurs des cartes du joueur et du croupier et changer la valeur de l'AS en fonction de la situation """

    def __init__(self):
        self.carte = []
        self.value = 0
        self.aces = 0

    def add_carte(self, card):
        self.carte.extend(card)
        for count, ele in enumerate(card, 0):
            if ele[1] == "As":
                self.aces += 1
            self.value += VALUES[ele[1]]
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.aces > 0 and self.value > 21:
            self.value -= 10
            self.aces -= 1


class Jetons:
    """ Jetons des joueurs pour faire des paris et ajouter ou enlever le total du joueur """

    def __init__(self):
        self.total = 100
        self.bet = 0
        self.winnings = 0

    def win_bet(self):
        self.total += self.bet
        self.winnings += 1

    def loss_bet(self):
        self.total -= self.bet
        self.winnings += 1


def take_bet(bet_amount, joueur_money):
    try:
        while bet_amount > joueur_money or bet_amount <= 0:
            bet_amount = int(input(" Entrez votre montant à nouveau : "))
        return bet_amount

    except TypeError:
        return "Montant invalide"


def hits(obj_de):
    new_card = [obj_de.deal_carte()[0][0]]
    # obj_h.add_carte(new_card)
    return new_card


def blackj_options(p_chips, obj_de, obj_h, dealer_card):
    global PLAYING
    next_card = hits(obj_de)
    choice = str(input(f"[ Tirer | Rester | Abandonner | Doubler ] : ")).lower()
    print("\n")
    if choice == "tirer":
        # hits(obj_de, obj_h)
        obj_h.add_carte(next_card)
        show_some(obj_h.carte, dealer_card, obj_h)

    elif choice == "rester":
        PLAYING = False

    elif choice == "abandonner":
        p_chips.bet = p_chips.bet / 2
        PLAYING = False
        obj_h.value += 21

    elif choice == "doubler":
        if p_chips.bet * 2 <= p_chips.total:
            p_chips.bet *= 2
            next_d_card = hits(obj_de)
            obj_h.add_carte(next_d_card)
            PLAYING = False
        else:
            print(" --Tu ne peux pas doubler, tu n'as pas assez d'argent--")
    else:
        print(" --Choix Invalide--")


def show_some(joueur_carte, dealer_carte, obj_h):
    print(f" ----->\n Cartes du joueur [{obj_h.value}] : {joueur_carte}")
    print(
        f" Cartes du croupier [{VALUES[dealer_carte[1][1]]}] : {[dealer_carte[1]]} \n ----->\n"
    )


def show_all(joueur_carte, dealer_carte, obj_h, obj_d):
    print(f" ----->\n Cartes du joueur [{obj_h.value}] : {joueur_carte}")
    print(f" Cartes du croupier [{obj_d.value}] : {dealer_carte} \n ----->\n")


def joueur_bust(obj_h, obj_c):
    if obj_h.value > 21:
        obj_c.loss_bet()
        return True
    return False


def joueur_wins(obj_h, obj_d, obj_c):
    if any((obj_h.value == 21, obj_h.value > obj_d.value and obj_h.value < 21)):
        obj_c.win_bet()
        return True
    return False


def dealer_bust(obj_d, obj_h, obj_c):
    if obj_d.value > 21:
        if obj_h.value < 21:
            obj_c.win_bet()
        return True
    return False


def dealer_wins(obj_h, obj_d, obj_c):
    if any((obj_d.value == 21, obj_d.value > obj_h.value and obj_d.value < 21)):
        obj_c.loss_bet()
        return True
    return False


def push(obj_h, obj_d):
    if obj_h.value == obj_d.value:
        return True
    return False


def joueur_surrender(obj_c):
    obj_c.loss_bet()
    return True


def clear_screen():
    system("cls" if name == "nt" else "clear")


def greet():
    print(" " + "".center(40, "_"), "|" + "".center(40, " ") + "|", sep="\n")
    print(
        "|" + "BlackJack".center(40, " ") + "|",
        "|" + "".center(40, "_") + "|",
        sep="\n",
    )


def main():
    p_win, d_win, draw = 0, 0, 0
    greet()
    p_chips = Jetons()
    while True:
        carte_deck = Deck()
        carte_deck.shuffle()
        p_carte, d_carte = carte_deck.deal_carte()
        p_hand = Hand()
        p_hand.add_carte(p_carte)
        print("\n Argent total -> ", p_chips.total)
        bet_money = int(input(" Entrez votre mise svp : "))
        p_chips.bet = take_bet(bet_money, p_chips.total)
        print("\n")

        show_some(p_carte, d_carte, p_hand)
        global PLAYING
        while PLAYING:  # Recall var. from hit and stand function
            blackj_options(p_chips, carte_deck, p_hand, d_carte)
            if joueur_bust(p_hand, p_chips):
                d_win += 1
                print("\n -- Joueur --> Busted")
                break

        PLAYING = True

        if p_hand.value <= 21:
            d_hand = Hand()
            d_hand.add_carte(d_carte)
            while d_hand.value < 17:
                d_card = hits(carte_deck)
                d_hand.add_carte(d_card)
                if dealer_bust(d_hand, p_hand, p_chips):
                    p_win += 1
                    print("\n -- Croupier --> Busted\n")
                    break
            show_all(p_hand.carte, d_hand.carte, p_hand, d_hand)

            if push(p_hand, d_hand):
                draw += 1
                print("\n " + " PUSH ".center(12, "-"))
            elif joueur_wins(p_hand, d_hand, p_chips):
                p_win += 1
                print(" " + " Joueur gagne ".center(22, "-"))
            elif dealer_wins(p_hand, d_hand, p_chips):
                d_win += 1
                print(" " + " Croupier gagne ".center(22, "-"))

        else:
            print("\n " + " Croupier gagne ".center(22, "-"))

        print(f"\n Jetons Restant : {p_chips.total} \n")

        ans = str(input(" Rejouer(OUI/NON) : ")).lower()
        if ans != "oui" or p_chips.total < 1:
            if p_chips.total < 1:
                print(" Tu n'as plus d'argent ")
            break
        clear_screen()
        print("\n" + " ".ljust(30, "-"))


main()

