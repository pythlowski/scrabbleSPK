import random


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
    letters_bag = []
    for letter, n in letters_count.items():
        letters_bag += [letter] * n
    random.shuffle(letters_bag)
    return letters_bag

tripleWords = [[0,0], [0,7], [0,14], [7,0], [7,14], [14,0], [14,7], [14,14]]
doubleWords = [[7,7], [1,1], [2,2], [3,3], [4,4], [10,10], [11,11], [12,12], [13,13], [1,13], [2,12], [3,11], [4,10], [13,1], [12,2], [11,3], [10,4]]
tripleLetters = [[1,5], [1,9], [5,1], [5,5], [5,9], [5,13], [9,1], [9,5], [9,9], [9,13], [13,5], [13,9]]
doubleLetters = [[0,3], [0,11], [2,6], [2,8], [3,0], [3,7], [3,14], [6,2], [6,6], [6,8], [6,12], [7,3], [7,11], [8,2], [8,6], [8,8], [8, 12], [11, 0], [11, 7], [11, 14], [12, 6], [12, 8], [14, 3], [14, 11]]
lettersPoints = {
    'A': 1, 'Ą': 5,'B': 3, 'C': 2, 'Ć': 6, 'D': 2, 'E': 1, 'Ę': 5, 'F': 5,'G': 3,'H': 3, 'I': 1, 'J': 3, 'K': 2, 'L': 2, 'Ł': 3, 'M': 2, 'N': 1, 'Ń': 7, 'O': 1, 'Ó': 5,
 'P': 2, 'R': 1, 'S': 1, 'Ś': 5, 'T': 2, 'U': 3, 'W': 1, 'Y': 2, 'Z': 1, 'Ź': 9, 'Ż': 5, ' ': 0}

# slowo1 = [{'letter': 'Ć', 'x': 3, 'y': 5},{'letter': 'U', 'x': 5, 'y': 5},{'letter': 'Z', 'x': 6, 'y': 5},{'letter': 'O', 'x': 7, 'y': 5},{'letter': 'N', 'x': 8, 'y': 5}]
class para:
    def __init__(self, x, y):
        self.x = x
        self.y = y

f = para(4,5)
l = para(8,5)

    
def find_every_word_horizontally_and_vertically_and_calculate_points_for_every_founded_word_then_sum_it_all_for_pawel(Grid, word):
    def find_idx(x_or_y, value):
        i = next((index for (index, d) in enumerate(word) if d[x_or_y] == value), None)
        return i



    def scan_word(x, y, axis): # axis = "horizontal"/"vertical" - horizontal to poziomo po angielsku xd
        firstX = x
        firstY = y
        lastX = x
        lastY = y
        if axis == "horizontal":
            while Grid[firstX][firstY-1] != '' or find_idx("y", firstY-1) != None:
                firstY = firstY-1
            while Grid[lastX][lastY+1] != '' or find_idx("y", lastY+1) != None:
                lastY = lastY+1

        elif axis == "vertical":
            while Grid[firstX-1][firstY] != '' or find_idx("x", firstX-1) != None:
                firstX = firstX-1 #dajemy to do funkcji count
            while Grid[lastX+1][lastY] != '' or find_idx("x", lastX+1) != None:
                lastX = lastX+1 #dajemy to do funkcji count
        return firstX, firstY, lastX, lastY

    def count(firstLetter, lastLetter):
        points = 0
        multiplier = 1
        w=''
        if firstLetter.x == lastLetter.x:
            # poziom
            i = firstLetter.x
            for j in range (firstLetter.y,lastLetter.y+1):
                if Grid[i][j] != '':
                    letter = lettersPoints.get(Grid[i][j])
                    w = w + Grid[i][j]
                else:
                    y = next((index for (index, d) in enumerate(word) if d['y'] == j and d['x'] == i), None)
                    letter = lettersPoints.get(word[y].get('letter'))
                    w = w + word[y].get('letter')
                    
                if [i,j] in tripleLetters:
                    letter = letter *3
                elif [i,j] in doubleLetters:
                    letter = letter *2
                points += letter  
                if [i,j] in tripleWords:
                    multiplier = multiplier * 3
                elif [i,j] in doubleWords:
                    multiplier = multiplier * 2  
        else:
            #pion E4 hehe
            j = firstLetter.y
            for i in range (firstLetter.x,lastLetter.x+1):
                if Grid[i][j] != '':
                    letter = lettersPoints.get(Grid[i][j])
                    w = w + Grid[i][j]
                else:
                    x = next((index for (index, d) in enumerate(word) if d['x'] == i and d['y'] == j), None)
                    letter = lettersPoints.get(word[x].get('letter'))
                    w = w + word[x].get('letter')
                if [i,j] in tripleLetters:
                    letter = letter *3
                elif [i,j] in doubleLetters:
                    letter = letter *2
                points += letter  
                if [i,j] in tripleWords:
                    multiplier = multiplier * 3
                elif [i,j] in doubleWords:
                    multiplier = multiplier * 2 
        points = points * multiplier
        return points, w
    sum_of_points = 0
    list_of_words = []
    # for i in word:
    #     tmp = i.get('x')
    #     i['x'] = i.get('y')
    #     i['y'] = tmp
    if len(word) == 1:
        f.x,f.y,l.x,l.y = scan_word(word[0].get('x'),word[0].get('y'),'horizontal')
        if f.y !=l.y:       
            p,s = count(f,l)
            sum_of_points += p
            list_of_words.append(s)
        f.x,f.y,l.x,l.y = scan_word(word[0].get('x'),word[0].get('y'),'vertical')
        if f.x !=l.x:
            p,s = count(f,l)
            sum_of_points += p
            list_of_words.append(s)
        print('suma punktów dla pojedynczej dołożonej litery:',sum_of_points)
    else:
        if word[0].get('x') == word[1].get('x'): #slowo w poziomie -- info dla Krzyśka bo mu się mylą wymiary xD
            f.x,f.y,l.x,l.y = scan_word(word[0].get('x'),word[0].get('y'),'horizontal')
            p,s = count(f,l)
            sum_of_points += p
            list_of_words.append(s)
            for i in word:
                f.x,f.y,l.x,l.y = scan_word(i.get('x'),i.get('y'),'vertical')
                if f.x !=l.x:
                    p,s = count(f,l)
                    sum_of_points += p
                    list_of_words.append(s)
            print('suma punktów dla słowa w poziomie:',sum_of_points)
        else:
            f.x,f.y,l.x,l.y = scan_word(word[0].get('x'),word[0].get('y'),'vertical')
            p,s = count(f,l)
            sum_of_points += p
            list_of_words.append(s)
            for i in word:
                f.x,f.y,l.x,l.y = scan_word(i.get('x'),i.get('y'),'horizontal')
                if f.y !=l.y:
                    p,s = count(f,l)
                    sum_of_points += p
                    list_of_words.append(s)
            print('suma punktów dla słowa w pionie:',sum_of_points)
    print(list_of_words)
    return sum_of_points
    
# find_every_word_horizontally_and_vertically_and_calculate_points_for_every_founded_word_then_sum_it_all_for_pawel(Grid1,slowo1)   
#asd = count(f,l)
#print(asd)