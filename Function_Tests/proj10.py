import cards  # required !!!

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def init_game():
    stock = cards.Deck()
    stock.shuffle()
    foudation = list()
    tableu = list()
    for i in range (4) :
        tableu.append([stock.deal()])
    return stock, tableu, foudation

def deal_to_tableau( tableau, stock):
    for i in range(4) :
        tableau[i].append(stock.deal())

def validate_move_to_foundation( tableau, from_col ):
    if len(tableau[from_col]) > 0 :
        move_card = tableau[from_col][-1]
        if move_card.rank() == 1 :
            print("\nError, cannot move {}.".format(move_card))
            return False
    else :
        print("\nError, empty column:" , from_col + 1)
        return False
    for i in range(4) :
        try:
            if (move_card.rank() < tableau[i][-1].rank() or tableau[i][-1].\
            rank() == 1) and move_card.suit() == tableau[i][-1].suit() :
                return True
        except :
            continue
    print("\nError, cannot move {}.".format(move_card))
    return False

def move_to_foundation( tableau, foundation, from_col ):
    if validate_move_to_foundation(tableau,from_col) == True :
        foundation.append(tableau[from_col].pop(-1))

def validate_move_within_tableau( tableau, from_col, to_col ):
    if len(tableau[to_col]) > 0 :
        print("\nError, target column is not empty:", to_col + 1)
    elif len(tableau[from_col]) > 0:
        return True
    else :
        print("\nError, no card in column:", from_col + 1)
    return False

def move_within_tableau( tableau, from_col, to_col ):
    if validate_move_within_tableau(tableau,from_col,to_col) == True :
        tableau[to_col].append(tableau[from_col].pop(-1))

def check_for_win( tableau, stock ):
    if len(stock) == 0 :
        for i in range (4) :
            for item in tableau[i] :
                if item.rank() != 1 :
                    return False
    else :
        return False
    return True

def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)

    assert maxm > 0   # maxm == 0 should not happen in this game?

    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')

        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')

        print()


def get_option():
    choice = input("\nInput an option (DFTRHQ): ")
    if choice.lower().strip() in ['d','r','h','q']:
        return [choice.upper()]
    elif 'f' in choice.lower() :
        a_list = choice.split()
        if len(a_list) == 2 and a_list[1] in ['1','2','3','4']:
            return ['F', int(a_list[1])-1]
        else :
            print("\nError in option:" , choice)
            return []
    elif 't' in choice.lower():
        a_list = choice.split()
        if len(a_list) == 3 and a_list[1] in ['1','2','3','4'] \
        and a_list[2] in ['1','2','3','4'] :
            return ['T', int(a_list[1])-1, int(a_list[2])-1]
        else:
            print("\nError in option:", choice)
            return []
    else :
        print("\nError in option:", choice)
        return []
def main():
    print(RULES)
    print(MENU)
    stock , tableau , foundation = init_game()
    display(stock,tableau,foundation)
    while 1 :
        option = get_option()
        if 'D' in option :
            deal_to_tableau(tableau , stock)

        elif 'F' in option :
            move_to_foundation(tableau,foundation,option[1])
            if check_for_win(tableau, stock) == True:
                print("\nYou won!")
                break

        elif 'T' in option :
            move_within_tableau(tableau,option[1],option[2])
            if check_for_win(tableau, stock) == True:
                print("\nYou won!")
                break

        elif 'R' in option:
            print("\n=========== Restarting: new game ============")
            print(RULES)
            print(MENU)
            stock, tableau, foundation = init_game()

        elif 'H' in option :
            print(MENU)

        elif 'Q' in option :
            print("\nYou have chosen to quit.")
            break
        if option != [] :
            display(stock, tableau, foundation)

if __name__ == '__main__':
     main()
