import random
import os


letters = [' ', 'A', 'Ą', 'B', 'C', 'Ć', 'D', 'E', 'Ę', 'F', 'G', 'H', 
            'I', 'J', 'K', 'L', 'Ł', 'M', 'N', 'O', 'Ó', 'P', 
            'R', 'S', 'Ś', 'T', 'U', 'W', 'Y', 'Z', 'Ź', 'Ż']

letters_count = {
    ' ': 2,
    'A': 9,
    'Ą': 1,
    'B': 2,
    'C': 3,
    'Ć': 1,
    'D': 3,
    'E': 7,
    'Ę': 1,
    'F': 1,
    'G': 2,
    'H': 2,
    'I': 8,
    'J': 2,
    'K': 3,
    'L': 3,
    'Ł': 2,
    'M': 3,
    'N': 5,
    'O': 6,
    'Ó': 1,
    'P': 3,
    'R': 4,
    'S': 4,
    'Ś': 1,
    'T': 3,
    'U': 2,
    'W': 4,
    'Y': 4,
    'Z': 5,
    'Ź': 1,
    'Ż': 1
}

def get_n_letters(n, bag):
  if len(bag) >= n:
    print('spoko, daje tyle ile chcesz')
    letters = bag[-n:]
    del bag[-n:]
    return letters
  else:
    print('masz tu jakies ściepy')
    letters = bag.copy()
    del bag[0:]
    return letters

def init_bag():
    # letters_bag = []
    # for letter, n in letters_count.items():
    #     letters_bag += [letter] * n
    # random.shuffle(letters_bag)
    # return letters_bag
    return [' '] * 5 + ['A'] * 5


words_database = {}

def insert(word):
    letters = word[:2]
    if letters in words_database.keys():
        words_database[letters].append(word)
    else:
        words_database[letters] = [word]

def exists(word):
    return word in words_database.get(word[:2], [])

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'words_database.txt')

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        insert(line.rstrip())

print('database loaded')
print(exists('siema'))

# counting points and words

tripleWords = [[0,0], [0,7], [0,14], [7,0], [7,14], [14,0], [14,7], [14,14]]
doubleWords = [[7,7], [1,1], [2,2], [3,3], [4,4], [10,10], [11,11], [12,12], [13,13], [1,13], [2,12], [3,11], [4,10], [13,1], [12,2], [11,3], [10,4]]
tripleLetters = [[1,5], [1,9], [5,1], [5,5], [5,9], [5,13], [9,1], [9,5], [9,9], [9,13], [13,5], [13,9]]
doubleLetters = [[0,3], [0,11], [2,6], [2,8], [3,0], [3,7], [3,14], [6,2], [6,6], [6,8], [6,12], [7,3], [7,11], [8,2], [8,6], [8,8], [8, 12], [11, 0], [11, 7], [11, 14], [12, 6], [12, 8], [14, 3], [14, 11]]
lettersPoints = {
    'A': 1, 'Ą': 5,'B': 3, 'C': 2, 'Ć': 6, 'D': 2, 'E': 1, 'Ę': 5, 'F': 5,'G': 3,'H': 3, 'I': 1, 'J': 3, 'K': 2, 'L': 2, 'Ł': 3, 'M': 2, 'N': 1, 'Ń': 7, 'O': 1, 'Ó': 5,
 'P': 2, 'R': 1, 'S': 1, 'Ś': 5, 'T': 2, 'U': 3, 'W': 1, 'Y': 2, 'Z': 1, 'Ź': 9, 'Ż': 5, ' ': 0}

# slowo1 = [{'letter': 'Ć', 'x': 3, 'y': 5},{'letter': 'U', 'x': 5, 'y': 5},{'letter': 'Z', 'x': 6, 'y': 5},{'letter': 'O', 'x': 7, 'y': 5},{'letter': 'N', 'x': 8, 'y': 5}]
class para:
    def __init__(self, y, x):
        self.y = y
        self.x = x

f = para(4,5)
l = para(8,5)

# print(lettersPoints.get('Ą'))
# print(slowo[0].get('letter'))
# tom_index = next((index for (index, d) in enumerate(slowo) if d['y'] == 5), None)
# print(slowo[tom_index].get('letter'))
# print(lettersPoints.get(slowo[tom_index].get('letter')))

def find_every_word_horizontally_and_vertically_and_calculate_points_for_every_founded_word_then_sum_it_all_for_pawel(Grid, word):
    def find_idx(y_or_x, value):
        i = next((index for (index, d) in enumerate(word) if d[y_or_x] == value), None)
        return i



    def scan_word(y, x, axis): # axis = "horizontal"/"vertical" - horizontal to poziomo po angielsku yd
        firstY = y
        firstX = x
        lastY = y
        lastX = x
        if axis == "horizontal":
            while Grid[firstY][firstX-1] != '' or find_idx("x", firstX-1) != None:
                firstX = firstX-1
            while Grid[lastY][lastX+1] != '' or find_idx("x", lastX+1) != None:
                lastX = lastX+1

        elif axis == "vertical":
            while Grid[firstY-1][firstX] != '' or find_idx("y", firstY-1) != None:
                firstY = firstY-1 #dajemx to do funkcji count
            while Grid[lastY+1][lastX] != '' or find_idx("y", lastY+1) != None:
                lastY = lastY+1 #dajemx to do funkcji count
        return firstY, firstX, lastY, lastX

    def count(firstLetter, lastLetter):
        points = 0
        multiplier = 1
        w=''
        if firstLetter.y == lastLetter.y:
            # poziom
            i = firstLetter.y
            for j in range (firstLetter.x,lastLetter.x+1):
                if Grid[i][j] != '':
                    # print(Grid[i][j])

                    letterPts = lettersPoints.get(Grid[i][j], 0)
                    if Grid[i][j][0] == 'b':
                        w += Grid[i][j][1]
                    else:
                        w += Grid[i][j]
                else:
                    x = next((index for (index, d) in enumerate(word) if d['x'] == j and d['y'] == i), None)
                    letterPts = lettersPoints.get(word[x].get('letter'), 0)

                    letter = word[x]['letter']
                    if letter[0] == 'b':
                        w += letter[1]
                    else:
                        w += letter

                    if [i,j] in tripleLetters:
                        letterPts = letterPts *3
                    elif [i,j] in doubleLetters:
                        letterPts = letterPts *2 
                    if [i,j] in tripleWords:
                        multiplier = multiplier * 3
                    elif [i,j] in doubleWords:
                        multiplier = multiplier * 2  
                points += letterPts 
        else:
            #pion E4 hehe
            j = firstLetter.x
            for i in range (firstLetter.y,lastLetter.y+1):
                if Grid[i][j] != '':
                    letterPts = lettersPoints.get(Grid[i][j], 0)
                    
                    if Grid[i][j][0] == 'b':
                        w += Grid[i][j][1]
                    else:
                        w += Grid[i][j]
                else:
                    y = next((index for (index, d) in enumerate(word) if d['y'] == i and d['x'] == j), None)
                    letterPts = lettersPoints.get(word[y].get('letter'), 0)
                    
                    letter = word[y]['letter']
                    if letter[0] == 'b':
                        w += letter[1]
                    else:
                        w += letter

                    if [i,j] in tripleLetters:
                        letterPts = letterPts *3
                    elif [i,j] in doubleLetters:
                        letterPts = letterPts *2
                    if [i,j] in tripleWords:
                        multiplier = multiplier * 3
                    elif [i,j] in doubleWords:
                        multiplier = multiplier * 2 
                points += letterPts  
        points = points * multiplier
        return points, w.lower()
    sum_of_points = 0
    list_of_words = []

    if len(word) == 1:
        f.y,f.x,l.y,l.x = scan_word(word[0].get('y'),word[0].get('x'),'horizontal')
        if f.x !=l.x:       
            p,s = count(f,l)
            sum_of_points += p
            list_of_words.append(s)
        f.y,f.x,l.y,l.x = scan_word(word[0].get('y'),word[0].get('x'),'vertical')
        if f.y !=l.y:
            p,s = count(f,l)
            sum_of_points += p
            list_of_words.append(s)
        print('suma punktów dla pojedynczej dołożonej litery:',sum_of_points)
    else:
        if word[0].get('y') == word[1].get('y'): #slowo w poziomie -- info dla Krzyśka bo mu się mylą wymiary xD
            f.y,f.x,l.y,l.x = scan_word(word[0].get('y'),word[0].get('x'),'horizontal')
            p,s = count(f,l)
            sum_of_points += p
            list_of_words.append(s)
            for i in word:
                f.y,f.x,l.y,l.x = scan_word(i.get('y'),i.get('x'),'vertical')
                if f.y !=l.y:
                    p,s = count(f,l)
                    sum_of_points += p
                    list_of_words.append(s)
            print('suma punktów dla słowa w poziomie:',sum_of_points)
        else:
            f.y,f.x,l.y,l.x = scan_word(word[0].get('y'),word[0].get('x'),'vertical')
            p,s = count(f,l)
            sum_of_points += p
            list_of_words.append(s)
            for i in word:
                f.y,f.x,l.y,l.x = scan_word(i.get('y'),i.get('x'),'horizontal')
                if f.x !=l.x:
                    p,s = count(f,l)
                    sum_of_points += p
                    list_of_words.append(s)
            print('suma punktów dla słowa w pionie:',sum_of_points)
    print(list_of_words)
    return sum_of_points, list_of_words
    
#s = find_every_word_horizontally_and_vertically_and_calculate_points_for_every_founded_word_then_sum_it_all_for_pawel(Grid1,slowo1)   
#asd = count(f,l)
#print(asd)