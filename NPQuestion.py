import nltk
import string
import random
import time
from Tkinter import *

def to_String(tokens):
    return "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()

def find_NPs(tagged_sentence):
    NP = 'NP: {<JJ.*>*<NN.*>*<POS>?<CC>?<NN.*>}' #This rule says that an NP chunk should be formed whenever
    cp = nltk.RegexpParser(NP)
    sentence = cp.parse(tagged_sentence)
    #sentence.draw()
    return sentence

def get_NP(sentence):
    return [line for line in [str(sentence[i]) for i in range(len(sentence))] if line[1:3] == 'NP']

def get_Words(NP):
    if NP[1:3] != 'NP':
        raise Exception('Not an NP')
    space_idx = [pos + 1 for pos, char in enumerate(NP) if char == ' ']
    slash_idx = [pos for pos, char in enumerate(NP) if char == '/']
    return [NP[space_idx[i]:slash_idx[i]] for i in range(len(space_idx))]

file = open('fungi_notes.txt')
raw_text = file.readlines()
text = [line for line in raw_text if len(line) > 1 and '-----' not in line]
line_idx = [i for i in range(len(raw_text)) if len(raw_text[i]) <= 1]
note_idx = [i for i in range(len(raw_text)) if len(raw_text[i]) > 1 and '-----' in raw_text[i]]

def NP_question(num):
    tokens = nltk.word_tokenize(text[num])
    tagged_sentence = nltk.pos_tag(tokens)
    #print(tagged_sentence)

    sentence = find_NPs(tagged_sentence)
    raw_NPs = get_NP(sentence)
    NPs = [get_Words(raw_NP) for raw_NP in raw_NPs]
    #print NPs

    #ugly, ugly
    raw_questions = []
    banned_words = ['most', 'and', "'s"]

    for NP in NPs:
        #if "'s" in NP:
        #    idx = NP.index("'s")
        #    NP[idx - 1] += NP[idx]
        #    NP[idx] = ''
        temp = tokens[:]
        first = True
        for word in tokens:
            for NP_word in NP:
                if NP_word in temp and NP_word not in banned_words:
                    idx = temp.index(NP_word)
                    if first == True or prev_idx + 1 == idx or prev_idx + 2 == idx:
                        num_spaces = len(temp[idx])
                        temp[idx] = '_'*num_spaces
                        first = False
                    prev_idx = idx
        raw_questions.append(temp)
    #for q in raw_questions:
    #    print to_String(q)
    randoQ = random.randrange(len(raw_questions))
    return to_String(raw_questions[randoQ])

def NP_text():
    counter = 0
    T.delete(1.0, END)
    for i in range(len(text)):
        counter = counter + 1
        line = NP_question(i)
        T.insert(END, line + '\n')
        if counter in line_idx:
            #T.insert(END, '\n')
            counter = counter + 1
        elif counter in note_idx:
            T.insert(END, '----------------------------\n')
            counter = counter + 1

def full_text():
    T.delete(1.0, END)
    [T.insert(END, line) for line in raw_text if len(line) > 1]

top = Tk()

def key(event):
    print event.char
    if event.char is 'f': full_text()
    if event.char is 'n': NP_text()

def callback(event):
    bop.focus_set()

bop = Frame(top, width=100, height = 100)
Button(bop, text='Exit', command=top.destroy).pack() #Adding a button means set_focus in while loop
bop.focus_set()
bop.bind("<Key>", key)
bop.bind("<Button-1>", callback)
bop.pack(side=RIGHT)

T = Text()
T.pack(side=LEFT)

def troll():
    T.delete(1.0, END)
    T.insert(END, 'asdasdas')

#NP_text()
while True:
    bop.focus_set()
    top.update_idletasks()
    top.update()