import operator

# wczytanie slownika
with open('sowpods.txt', 'r') as f:
    sowpods = f.readlines()
words = [x.strip() for x in sowpods]

# tablcia punktow
scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
          "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
          "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
          "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
          "x": 8, "z": 10}

# plansza gry, ostatnie puste pola pozostaja wolne, dostepnych pol jest 15x15
board = ([["|", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "|"],
          ["|", "X", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "X", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", "A", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", "L", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", "I", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", "C", " ", " ", "X", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", "E", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
          ["|", "X", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "X", "|"],
          ["|", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "|"]])

# dostepne litery dla gracza
RACK = "LONE"

# tablica wyrazow dajacych sie zlozyc z liter gracza
valid_words = []


def is_subset(s1, s2):
    alist = list(s2)

    pos1 = 0
    still_ok = True

    while pos1 < len(s1) and still_ok:
        pos2 = 0
        found = False
        while pos2 < len(alist) and not found:
            if s1[pos1] == alist[pos2]:
                found = True
            else:
                pos2 = pos2 + 1

        if found:
            alist[pos2] = None
        else:
            still_ok = False

        pos1 = pos1 + 1

    return still_ok


# tablica wszystkich mozliwych kombinacji slow z dostepnych liter
def find_cheated_words():
    for word in words:
        if is_subset(word, RACK):
            valid_words.append(word)

    # posortowanie tablicy wyrazow wedlug punktow
    score = 0
    result = {}
    for word in valid_words:
        for letter in list(word):
            score = score + scores[letter.lower()]
        result[word] = score
        score = 0
    sorted_x = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    result = dict(sorted_x)
    for word in result.keys():
        print("{} {}".format(result[word], word))


def add_cheated_word_on_map():
    row = 0
    column = 0
    right = False
    down = False
    final_right = False
    final_down = False
    position_in_word = 0
    temp_rack = RACK
    high_score = 0
    score = 0
    finded_word = ""

    rows = 19
    cols = 19
    for i in range(0, rows):  # rzedy
        for j in range(0, cols):  # kolumny
            if (board[i][j] != " " and board[i][j] != "|" and board[i][j] != "-"):  # jesli wykryjemy litere
                local_rack = RACK + board[i][j]  # dodajemy ja do liter gracza
                for word in words:  # szukamy najlepiej punktowanego slowa, ktore mozemy wstawic na plansze
                    score = 0
                    if is_subset(word, local_rack):  # sprawdzamy, czy kombinacja znajduje sie w slowniku
                        for letter in list(word):
                            score = score + scores[letter.lower()]  # wyliczamy wynik kombinacji
                        letter_position = word.find(board[i][j])  # lokacja litery w slowie
                        if (
                                score > high_score and letter_position != -1):  # jesli wynik jest lepszy od najlepszego dochczasowego, sprawdzamy, czy mozna go wstawic na plansze
                            right = True
                            down = True
                            for local_column in range(j - letter_position - 1, j + len(
                                    word) - letter_position + 1):  # sprawdzamy, czy wyraz mozna wpasowac poziomo
                                if (local_column == j):
                                    continue
                                if (board[i][local_column] != " "):
                                    right = False
                                    break
                            if (right == True):  # jesli tak, aktualizujemy najlepsze znalezione slowo
                                row = i
                                column = j
                                high_score = score
                                finded_word = word
                                final_down = True
                                position_in_word = letter_position

                            else:
                                for local_row in range(i - letter_position - 1, i + len(
                                        word) - letter_position + 1):  # sprawdzamy, czy wyraz mozna wpasowac pionowo
                                    if (local_row == i):
                                        continue
                                    if (board[local_row][j] != " "):
                                        down = False
                                        break
                                if (down == True):
                                    row = i
                                    column = j
                                    high_score = score
                                    finded_word = word
                                    final_down = True
                                    position_in_word = letter_position

    # dodajemy w poziomie
    if final_right:
        i = 0
        for iteration in range(0, len(finded_word)):
            board[row][column - position_in_word + iteration] = finded_word[i]
            i += 1

    # dodajemy w pionie
    if final_down:
        i = 0
        for iteration in range(0, len(finded_word)):
            board[row - position_in_word + iteration][column] = finded_word[i]
            i += 1


print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                 for row in board]))

#find_cheated_words()
add_cheated_word_on_map()

print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                 for row in board]))
