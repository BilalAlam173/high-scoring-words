import functools
from itertools import chain, permutations


class HighScoringWords:
    MAX_LEADERBOARD_LENGTH = 100  # the maximum number of items that can appear in the leaderboard
    MIN_WORD_LENGTH = 3  # words must be at least this many characters long
    letter_values = {}
    valid_words = []

    def __assignValuesToWord(self, x):
        charList = list(x)
        charListWithValues = map(lambda x:self.letter_values[x], charList)
        return functools.reduce(lambda a,b: a+b, charListWithValues)
    
    def __comparator(self, a, b):
        if a[1] < b[1]:
            return -1
        elif a[1] > b[1]:
            return 1
        else:
            return -1 if a[0] > b[0] else 1

    def __superset(self, iterable):
        s = list(iterable)
        return chain.from_iterable(permutations(s, r) for r in range(len(s)+1))

    def __init__(self, validwords='wordlist.txt', lettervalues='letterValues.txt'):
        """
        Initialise the class with complete set of valid words and letter values by parsing text files containing the data
        :param validwords: a text file containing the complete set of valid words, one word per line
        :param lettervalues: a text file containing the score for each letter in the format letter:score one per line
        :return:
        """
        with open(validwords) as f:
            word_list = f.read().splitlines()
            self.valid_words = list(filter(lambda x : len(x) >= self.MIN_WORD_LENGTH, word_list))

        with open(lettervalues) as f:
            for line in f:
                (key, val) = line.split(':')
                self.letter_values[str(key).strip().lower()] = int(val)
    
    def __sortWithValues(self, wordlist):
        wordsWithValues = list(map(lambda x: (x, self.__assignValuesToWord(x)), wordlist))
        return sorted(wordsWithValues, key=functools.cmp_to_key(self.__comparator), reverse=True)[:100]

    def build_leaderboard_for_word_list(self):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOAD_LENGTH words from the complete set of valid words.
        :return: The list of top words.
        """
        return self.__sortWithValues(self.valid_words); 

    def build_leaderboard_for_letters(self, starting_letters):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that can be built using only the letters contained in the starting_letters String.
        The number of occurrences of a letter in the startingLetters String IS significant. If the starting letters are bulx, the word "bull" is NOT valid.
        There is only one l in the starting string but bull contains two l characters.
        Words are ordered in the leaderboard by their score (with the highest score first) and then alphabetically for words which have the same score.
        :param starting_letters: a random string of letters from which to build words that are valid against the contents of the wordlist.txt file
        :return: The list of top buildable words.
        """
        possibleWordsList = list(filter(lambda x: len(x) >=self.MIN_WORD_LENGTH, map(''.join, self.__superset(starting_letters))))
        valid_words = list(filter(lambda x: len(x)<=len(starting_letters), self.valid_words))
        print(len(self.valid_words), len(valid_words))
        validPossibleWordsList = list(filter(lambda x: x in valid_words, possibleWordsList))
        return self.__sortWithValues(validPossibleWordsList);

def display(list):
    for i, item in enumerate(list):
        print("#{}   {} ({})".format(i+1, item[0],item[1]))
h = HighScoringWords()
print("\n** Words leaderboard with their values ** \n")
display(h.build_leaderboard_for_word_list())
print('\n ** Leaderboard with values of all possible words which can be made from the word "deora" ** \n')
display(h.build_leaderboard_for_letters('deora'))