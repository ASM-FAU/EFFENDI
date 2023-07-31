import json
import re
import os
import sys
import pickle
import time
import datetime
from PyQt5 import QtWidgets
# import numpy as np


ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


class T8WordMatching:
    def __init__(self, language, dict_path, keyboard_layout):
        letter_layout = [3, 3, 3, 3, 3, 4, 3, 4]
        
        # Determine number of letters per key
        available_keys = keyboard_layout.count(True)
        # available_keys = 0
        # for i in range(len(keyboard_layout)):
        #     if keyboard_layout[i] is True:
        #         available_keys += 1
        if available_keys < 10:
            letters_per_key = int(26 / (available_keys - 2)) # subtract 2 for next and space button
            remaining_keys = 26 % (available_keys - 2)  # number of keys that contain more letters than general
            letter_layout = [letters_per_key]*(available_keys-2)
            # distribute the remaining letters
            for i in range(remaining_keys):
                letter_layout[-1-i] += 1

        # Distribute letters between keys
        keysLayout = ['']*(available_keys-2)
        letter_idx = 0  # alphabet counter
        for i in range(len(letter_layout)):
            for _ in range(letter_layout[i]):
                keysLayout[i] += ALPHABET[letter_idx]
                letter_idx += 1

        # Add language specific letters
        if language == "German":    
            for i in range(len(keysLayout)):
                if 'a' in keysLayout[i]:
                    keysLayout[i] += 'ä'
                if 'o' in keysLayout[i]:
                    keysLayout[i] += 'ö'
                if 'u' in keysLayout[i]:
                    keysLayout[i] += 'ü'
                if 's' in keysLayout[i]:
                    keysLayout[i] += 'ß'
                if 'm' in keysLayout[i]:
                    keysLayout[i] += 'µ'


        # if language == "German":    
        #     keysLayout = ('ABCÄabcä', 'DEFdef', 'GHIghi', 'JKLjkl', 'MNOÖmnoöµ', 'PQRSpqrsß', 'TUVÜtuvü', 'WXYZwxyz')
        # elif language == "English":   
        #     keysLayout = ('abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz')

        self.m = dict((l, str(n)) for n, letters in enumerate(keysLayout, start=2) for l in letters)
        self.word_dict_exact, self.word_dict_contains, self.frequency = {}, {}, {}
        # self.wordMatch = re.compile('[^a-z]+')
        self.wordMatch = re.compile('[^a-zäöüßµ]+', flags=re.IGNORECASE)

        if len(dict_path) > 0:
            self.dict_path = dict_path
            with open(dict_path, "rb") as dictionary:
                dictionary = pickle.load(dictionary)
                self.word_dict_exact = dictionary["word_dict_exact"]
                self.word_dict_contains = dictionary["word_dict_contains"]
                self.frequency = dictionary["word_frequency"]
        else:
            # print(os.listdir())
            # self.dict_path = "\\personal_dicts\\dictionary.json"
            date = datetime.datetime.today()
            self.dict_path = os.path.join("python_code", "personal_dicts", "dictionary_{}_{}_{}_{}_{}_{}.json".format(date.year, date.month, date.day, date.hour, date.minute, date.second))
            with open(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'dicts', language + '.txt'), 'r', encoding="ansi") as f:#"iso-8859-1, latin-1
                self.createDict(f)


    def acquireData(self, word):
        """Translate word into T8 code and add to word to each possible code in dictionary wordList

        Args:
            word (string): Word to be translated into T8 code
        """
        num = ''.join(self.m[c] for c in word)
        for i in range(1, len(word) + 1):
            inp = num[:i]

            if i == len(word):
                if inp not in self.word_dict_exact:
                    self.word_dict_exact[inp] = {word.lower()}
                else:
                    self.word_dict_exact[inp].add(word.lower())
            else:
                if inp not in self.word_dict_contains:
                    self.word_dict_contains[inp] = {word.lower()}
                else:
                    self.word_dict_contains[inp].add(word.lower())


    # def improveData(f):
    #     """Investigate books to acquire data of word occurances to improve dictionary
    #     Also store frequency for each word

    #     Args:
    #         f (TextIOWrapper): Text file with books.
    #     """
    #     for word in wordMatch.split(f.read().lower()):
    #         if word in frequency:
    #             frequency[word] += 1
    #         else:
    #             acquireData(word)
    #             frequency[word] = 1
    #     # howManyWords = len(occurrences)
    #     # print(howManyWords)

    def addWordToDict(self, word):
        """Add new word to dictionary and frequency dict and save as json file.

        Args:
            word (string): Word to be added to dict
        """
        if word not in self.word_dict_exact and len(word) > 0:
            self.acquireData(word)
            self.frequency[word] = 1
            # with open("dictionary.json", "wb") as dict_file: 
            #     pickle.dump(self.wordList, dict_file)
            # with open("frequency.json", "wb") as freq_file: 
            #     pickle.dump(self.frequency, freq_file)
            # with open(self.dict_path, "wb") as dict_file:
            #     dictionary = {"word_dict_exact": self.word_dict_exact,
            #                   "word_dict_contains": self.word_dict_contains,
            #                   "word_frequency": self.frequency}
            #     pickle.dump(dictionary, dict_file, protocol=pickle.HIGHEST_PROTOCOL)
        

    def updateWordFrequency(self, word):
        """Update word frequency. This is called when clicking space or special characters.

        Args:
            word (string): Word that needs to be updated
        """
        if word in self.frequency:
            self.frequency[word] += 1
            self.frequency[word.lower()] += 1


    # def saveWordFrequency(self):
    #     """Save updated word frequency to json file
    #     """
    #     with open("frequency.json", "wb") as freq_file:
    #         pickle.dump(self.frequency, freq_file)


    def updateDict(self):
        """Save updated word frequency to json file
        """
        with open(self.dict_path, "wb") as dict_file:
            dictionary = {"word_dict_exact": self.word_dict_exact,
                          "word_dict_contains": self.word_dict_contains,
                          "word_frequency": self.frequency}
            pickle.dump(dictionary, dict_file, protocol=pickle.HIGHEST_PROTOCOL)


    def saveDict(self, file_name):
        """Save dict as json file.
        """
        # options = QtWidgets.QFileDialog.Options()
        # fileName, _ = QtWidgets.QFileDialog.getSaveFileName("Save Dictionary File", os.path.join("python_code", "personal_dicts"), "JSON File (*.json)", options=options)
        if file_name:
            self.dict_path = file_name
            with open(file_name, 'wb') as dict_file:
                dictionary = {"word_dict_exact": self.word_dict_exact,
                              "word_dict_contains": self.word_dict_contains,
                              "word_frequency": self.frequency}
                pickle.dump(dictionary, dict_file, protocol=pickle.HIGHEST_PROTOCOL) 


    def createDict(self, dictionary_text_file):
        """Create word dictionary and frequency dictionary for prioritizing

        Args:
            dictionary_text_file (TextIOWrapper): Dictionary text file
        """
        for word in self.wordMatch.split(dictionary_text_file.read()):
            self.acquireData(word.lower())
            self.frequency[word.lower()] = 1

        # Save dict to file
        self.updateDict()


    def searchData(self, n):
        """Search for T8 code in dictionary and return matching words and their frequencies

        Args:
            n (string): T8 code input

        Returns:
            list: Contains matching words and their frequencies sorted
        """
        # t=time.time()
        if n not in self.word_dict_exact and n not in self.word_dict_contains:
            return None

        matches_exact, results_contains, results_exact = [], [], []

        # print(n)
        # print(matches_exact = list(self.word_dict_exact[n]))
        # print(n)
        # print(n in self.word_dict_exact)
        if n in self.word_dict_exact:
            matches_exact = list(self.word_dict_exact[n])
            
            # sort matches based on frequency
            results_exact = [x for _, x in sorted(zip(list(map(self.frequency.get, matches_exact)), matches_exact), reverse=True)]
            # print(results_exact)
            # print("exact results")#TODO this doesn't ouput for single input!!
            # print(results_exact)

        if len(n) > 1 and n in self.word_dict_contains and len(matches_exact) < 50:
            matches_contains = self.word_dict_contains[n]
            
            # sort matches based on frequency
            results_contains = [x for _, x in sorted(zip(list(map(self.frequency.get, matches_contains)), matches_contains), reverse=True)][:30]
        # print("Total took {}".format(time.time() - t))

        return results_exact, results_contains
