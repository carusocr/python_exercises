"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

codeskulptor.set_timeout(60)

WORDFILE = "assets_scrabble_words3.txt"
#"http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    newlist = []
    for item in list1:
        if item not in newlist:
            newlist.append(item)
    return newlist

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    newlist = []
    for item in list1:
        if item in list2:
            newlist.append(item)
    return newlist

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    1. Avoid mutation by making copies of lists.
    2. While loop comparing min of lists.
    3. add smaller item and remove from list copy
    4. add any remaining items to new list
    """
    newlist = []
    # MAKE COPIES OF LISTS
    new1 = list(list1)
    new2 = list(list2)
    while min(new1,new2):
        if new1[0] >= new2[0]:
            newlist.append(new2.pop(0))
        else:
            newlist.append(new1.pop(0))
    if new1:
        newlist += new1
    else:
        newlist += new2
    return newlist
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    newlist = list(list1)
    new1 = newlist[0:len(newlist)/2]
    new2 = newlist[len(newlist)/2:]
    # base case is 0/1 list that needs no sorting
    if len(newlist) <= 1:
        return newlist
    else:
        return merge(merge_sort(new1),merge_sort(new2))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    1. Split input word into first character and rest of word.
    2. Generate all strings out of rest.
    3. Add all strings that include first at any position in the strings.
    """
    wordlist = []
    # base case is empty word
    if word == "":
        return [""] #chokes on non-list return, duh
    first_char = word[0]
    # generate all strings out of rest
    for rest_strings in gen_all_strings(word[1:]):
        for index in range(len(rest_strings)+1): 
            #insert first char into each position of rest
            new_word = rest_strings[:index] + first_char + rest_strings[index:]
            wordlist.append(new_word)
    return gen_all_strings(word[1:]) + wordlist

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    words = []
    for word in netfile.readlines():
        words.append(word.rstrip())
    return words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    print len(words)
    print words[200]
    print len(words[200])
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
#testlist = [1,1,2,3,4,5,5]
#list1 = [1,2,3,4,5]
#list2 = [3,4,5,6,7]
#print remove_duplicates(testlist)
#print intersect(list1, list2)
#print merge(list1,list2)
#print merge_sort(testlist)
#print gen_all_strings("zorg")
#words = load_words(WORDFILE)
