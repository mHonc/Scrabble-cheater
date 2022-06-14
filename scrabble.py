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
          ["|", " ", " ", " ", " ", " ", " ", " ", " ", "C", " ", " ", " ", " ", " ", " ", " ", " ", "|"],
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
    stillOK = True

    while pos1 < len(s1) and stillOK:
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
            stillOK = False

        pos1 = pos1 + 1

    return stillOK

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
    finalRight = False
    finalDown = False
    position_in_word = 0
    tempRack = RACK
    highScore = 0
    score = 0
    findedWord = ""

    rows = 19
    cols = 19
    for i in range(0, rows):  # rzedy
        for j in range(0, cols):  # kolumny
            if (board[i][j] != " " and board[i][j] != "|" and board[i][j] != "-"):  # jesli wykryjemy litere
                localRack = RACK + board[i][j]  # dodajemy ja do liter gracza
                for word in words:  # szukamy najlepiej punktowanego slowa, ktore mozemy wstawic na plansze
                    score = 0
                    if is_subset(word, localRack):  # sprawdzamy, czy kombinacja znajduje sie w slowniku
                        for letter in list(word):
                            score = score + scores[letter.lower()]  # wyliczamy wynik kombinacji
                        letterPosition = word.find(board[i][j])  # lokacja litery w slowie
                        if (
                                score > highScore and letterPosition != -1):  # jesli wynik jest lepszy od najlepszego dochczasowego, sprawdzamy, czy mozna go wstawic na plansze
                            right = True
                            down = True
                            for localColumn in range(j - letterPosition - 1, j + len(
                                    word) - letterPosition + 1):  # sprawdzamy, czy wyraz mozna wpasowac poziomo
                                if (localColumn == j):
                                    continue
                                if (board[i][localColumn] != " "):
                                    right = False
                                    break
                            if (right == True):  # jesli tak, aktualizujemy najlepsze znalezione slowo
                                row = i
                                column = j
                                highScore = score
                                findedWord = word
                                finalRight = True
                                position_in_word = letterPosition

                            else:
                                for localRow in range(i - letterPosition - 1, i + len(
                                        word) - letterPosition + 1):  # sprawdzamy, czy wyraz mozna wpasowac pionowo
                                    if (localRow == i):
                                        continue
                                    if (board[localRow][j] != " "):
                                        down = False
                                        break
                                if (down == True):
                                    row = i
                                    column = j
                                    highScore = score
                                    findedWord = word
                                    finalDown = True
                                    position_in_word = letterPosition

    # dodajemy w poziomie
    if (finalRight):
        i = 0
        for iteration in range(0, len(findedWord)):
            board[row][column - position_in_word + iteration] = findedWord[i]
            i += 1

    # dodajemy w pionie
    if (finalDown):
        i = 0
        for iteration in range(0, len(findedWord)):
            board[row - position_in_word + iteration][column] = findedWord[i]
            i += 1


print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                 for row in board]))

#FindCheatedWords()
add_cheated_word_on_map()


print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                 for row in board]))
