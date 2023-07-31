from gui import T8WordMatching
import random
import os
import sys

from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    currentWords = []
    buttonInputList = []
    text = ""

    def __init__(self):
        super(Ui, self).__init__()
        # uic.loadUi(os.path.join(os.getcwd(), 'python_code', 'ui', 'new_keyboard.ui'), self)
        uic.loadUi(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ui', 'new_keyboard.ui'), self)
        #########################################################################
        # T8 Buttons
        self.buttons = []

        self.button1 = self.findChild(QtWidgets.QPushButton, 'pushButton0')
        self.button1.clicked.connect(lambda: self.clicked("2"))
        self.button2 = self.findChild(QtWidgets.QPushButton, 'pushButton1')
        self.button2.clicked.connect(lambda: self.clicked("3"))
        self.button3 = self.findChild(QtWidgets.QPushButton, 'pushButton2')
        self.button3.clicked.connect(lambda: self.clicked("4"))
        self.button4 = self.findChild(QtWidgets.QPushButton, 'pushButton3')
        self.button4.clicked.connect(lambda: self.clicked("5"))
        self.button5 = self.findChild(QtWidgets.QPushButton, 'pushButton4')
        self.button5.clicked.connect(lambda: self.nextClicked())

        self.button6 = self.findChild(QtWidgets.QPushButton, 'pushButton5')
        self.button6.clicked.connect(lambda: self.spaceClicked())
        self.button7 = self.findChild(QtWidgets.QPushButton, 'pushButton6')
        self.button7.clicked.connect(lambda: self.clicked("6"))
        self.button8 = self.findChild(QtWidgets.QPushButton, 'pushButton7')
        self.button8.clicked.connect(lambda: self.clicked("7"))
        self.button9 = self.findChild(QtWidgets.QPushButton, 'pushButton8')
        self.button9.clicked.connect(lambda: self.clicked("8"))
        self.button10 = self.findChild(QtWidgets.QPushButton, 'pushButton9')
        self.button10.clicked.connect(lambda: self.clicked("9"))
        # Backspace - triggered through long pressing next button (1)
        self.button_backspace = self.findChild(QtWidgets.QPushButton, 'backspace')
        self.button_backspace.clicked.connect(lambda: self.backspaceClicked())
        # Enter - triggered through long pressing space button (10)
        self.button_enter = self.findChild(QtWidgets.QPushButton, 'enter')
        self.button_enter.clicked.connect(lambda: self.enterClicked())


        self.label_phrases.setText(self.randomSentences())

        self.buttons.append(self.button1)
        self.buttons.append(self.button2)
        self.buttons.append(self.button3)
        self.buttons.append(self.button4)
        self.buttons.append(self.button5)
        self.buttons.append(self.button6)
        self.buttons.append(self.button7)
        self.buttons.append(self.button8)
        self.buttons.append(self.button9)
        self.buttons.append(self.button10)

        ###########################################################################
        # Letter buttons
        self.button_a = self.findChild(QtWidgets.QPushButton, 'pushButton_a')
        self.button_a.clicked.connect(lambda: self.onScreenKeyboard("a"))
        self.button_b = self.findChild(QtWidgets.QPushButton, 'pushButton_b')
        self.button_b.clicked.connect(lambda: self.onScreenKeyboard("b"))
        self.button_c = self.findChild(QtWidgets.QPushButton, 'pushButton_c')
        self.button_c.clicked.connect(lambda: self.onScreenKeyboard("c"))
        self.button_d = self.findChild(QtWidgets.QPushButton, 'pushButton_d')
        self.button_d.clicked.connect(lambda: self.onScreenKeyboard("d"))
        self.button_e = self.findChild(QtWidgets.QPushButton, 'pushButton_e')
        self.button_e.clicked.connect(lambda: self.onScreenKeyboard("e"))
        self.button_f = self.findChild(QtWidgets.QPushButton, 'pushButton_f')
        self.button_f.clicked.connect(lambda: self.onScreenKeyboard("f"))
        self.button_g = self.findChild(QtWidgets.QPushButton, 'pushButton_g')
        self.button_g.clicked.connect(lambda: self.onScreenKeyboard("g"))
        self.button_h = self.findChild(QtWidgets.QPushButton, 'pushButton_h')
        self.button_h.clicked.connect(lambda: self.onScreenKeyboard("h"))
        self.button_i = self.findChild(QtWidgets.QPushButton, 'pushButton_i')
        self.button_i.clicked.connect(lambda: self.onScreenKeyboard("i"))
        self.button_j = self.findChild(QtWidgets.QPushButton, 'pushButton_j')
        self.button_j.clicked.connect(lambda: self.onScreenKeyboard("j"))
        self.button_k = self.findChild(QtWidgets.QPushButton, 'pushButton_k')
        self.button_k.clicked.connect(lambda: self.onScreenKeyboard("k"))
        self.button_l = self.findChild(QtWidgets.QPushButton, 'pushButton_l')
        self.button_l.clicked.connect(lambda: self.onScreenKeyboard("l"))
        self.button_m = self.findChild(QtWidgets.QPushButton, 'pushButton_m')
        self.button_m.clicked.connect(lambda: self.onScreenKeyboard("m"))
        self.button_n = self.findChild(QtWidgets.QPushButton, 'pushButton_n')
        self.button_n.clicked.connect(lambda: self.onScreenKeyboard("n"))
        self.button_o = self.findChild(QtWidgets.QPushButton, 'pushButton_o')
        self.button_o.clicked.connect(lambda: self.onScreenKeyboard("o"))
        self.button_p = self.findChild(QtWidgets.QPushButton, 'pushButton_p')
        self.button_p.clicked.connect(lambda: self.onScreenKeyboard("p"))
        self.button_q = self.findChild(QtWidgets.QPushButton, 'pushButton_q')
        self.button_q.clicked.connect(lambda: self.onScreenKeyboard("q"))
        self.button_r = self.findChild(QtWidgets.QPushButton, 'pushButton_r')
        self.button_r.clicked.connect(lambda: self.onScreenKeyboard("r"))
        self.button_s = self.findChild(QtWidgets.QPushButton, 'pushButton_s')
        self.button_s.clicked.connect(lambda: self.onScreenKeyboard("s"))
        self.button_t = self.findChild(QtWidgets.QPushButton, 'pushButton_t')
        self.button_t.clicked.connect(lambda: self.onScreenKeyboard("t"))
        self.button_u = self.findChild(QtWidgets.QPushButton, 'pushButton_u')
        self.button_u.clicked.connect(lambda: self.onScreenKeyboard("u"))
        self.button_v = self.findChild(QtWidgets.QPushButton, 'pushButton_v')
        self.button_v.clicked.connect(lambda: self.onScreenKeyboard("v"))
        self.button_w = self.findChild(QtWidgets.QPushButton, 'pushButton_w')
        self.button_w.clicked.connect(lambda: self.onScreenKeyboard("w"))
        self.button_x = self.findChild(QtWidgets.QPushButton, 'pushButton_x')
        self.button_x.clicked.connect(lambda: self.onScreenKeyboard("x"))
        self.button_y = self.findChild(QtWidgets.QPushButton, 'pushButton_y')
        self.button_y.clicked.connect(lambda: self.onScreenKeyboard("y"))
        self.button_z = self.findChild(QtWidgets.QPushButton, 'pushButton_z')
        self.button_z.clicked.connect(lambda: self.onScreenKeyboard("z"))

        # Backspace
        self.pushButton_backspace = self.findChild(QtWidgets.QPushButton, 'pushButton_backspace')
        self.pushButton_backspace.clicked.connect(lambda: self.onScreenBackspace())
        # Shift
        self.pushButton_shift = self.findChild(QtWidgets.QPushButton, 'pushButton_shift')
        self.pushButton_shift.clicked.connect(lambda: self.toggleShift())
        self.pushButton_shift_2 = self.findChild(QtWidgets.QPushButton, 'pushButton_shift_2')
        self.pushButton_shift_2.clicked.connect(lambda: self.toggleShift())
        self.shift = False

        ###########################################################################
        # Numbers
        self.pushButton_num1 = self.findChild(QtWidgets.QPushButton, 'pushButton_num1')
        self.pushButton_num1.clicked.connect(lambda: self.insertSpecialCharacters("1"))
        self.pushButton_num2 = self.findChild(QtWidgets.QPushButton, 'pushButton_num2')
        self.pushButton_num2.clicked.connect(lambda: self.insertSpecialCharacters("2"))
        self.pushButton_num3 = self.findChild(QtWidgets.QPushButton, 'pushButton_num3')
        self.pushButton_num3.clicked.connect(lambda: self.insertSpecialCharacters("3"))
        self.pushButton_num4 = self.findChild(QtWidgets.QPushButton, 'pushButton_num4')
        self.pushButton_num4.clicked.connect(lambda: self.insertSpecialCharacters("4"))
        self.pushButton_num5 = self.findChild(QtWidgets.QPushButton, 'pushButton_num5')
        self.pushButton_num5.clicked.connect(lambda: self.insertSpecialCharacters("5"))
        self.pushButton_num6 = self.findChild(QtWidgets.QPushButton, 'pushButton_num6')
        self.pushButton_num6.clicked.connect(lambda: self.insertSpecialCharacters("6"))
        self.pushButton_num7 = self.findChild(QtWidgets.QPushButton, 'pushButton_num7')
        self.pushButton_num7.clicked.connect(lambda: self.insertSpecialCharacters("7"))
        self.pushButton_num8 = self.findChild(QtWidgets.QPushButton, 'pushButton_num8')
        self.pushButton_num8.clicked.connect(lambda: self.insertSpecialCharacters("8"))
        self.pushButton_num9 = self.findChild(QtWidgets.QPushButton, 'pushButton_num9')
        self.pushButton_num9.clicked.connect(lambda: self.insertSpecialCharacters("9"))
        self.pushButton_num0 = self.findChild(QtWidgets.QPushButton, 'pushButton_num0')
        self.pushButton_num0.clicked.connect(lambda: self.insertSpecialCharacters("0"))

        ###########################################################################
        # Special Characters
        self.pushButton_exclamation = self.findChild(QtWidgets.QPushButton, 'pushButton_exclamation')
        self.pushButton_exclamation.clicked.connect(lambda: self.insertSpecialCharacters("!"))
        self.pushButton_comma = self.findChild(QtWidgets.QPushButton, 'pushButton_comma')
        self.pushButton_comma.clicked.connect(lambda: self.insertSpecialCharacters(","))
        self.pushButton_colon = self.findChild(QtWidgets.QPushButton, 'pushButton_colon')
        self.pushButton_colon.clicked.connect(lambda: self.insertSpecialCharacters(":"))
        self.pushButton_dot = self.findChild(QtWidgets.QPushButton, 'pushButton_dot')
        self.pushButton_dot.clicked.connect(lambda: self.insertSpecialCharacters("."))
        self.pushButton_quotes = self.findChild(QtWidgets.QPushButton, 'pushButton_quotes')
        self.pushButton_quotes.clicked.connect(lambda: self.insertSpecialCharacters("\""))
        self.pushButton_question = self.findChild(QtWidgets.QPushButton, 'pushButton_question')
        self.pushButton_question.clicked.connect(lambda: self.insertSpecialCharacters("?"))
        self.pushButton_bracket_open = self.findChild(QtWidgets.QPushButton, 'pushButton_bracket_open')
        self.pushButton_bracket_open.clicked.connect(lambda: self.insertSpecialCharacters("("))
        self.pushButton_bracket_close = self.findChild(QtWidgets.QPushButton, 'pushButton_bracket_close')
        self.pushButton_bracket_close.clicked.connect(lambda: self.insertSpecialCharacters(")"))
        self.pushButton_plus = self.findChild(QtWidgets.QPushButton, 'pushButton_plus')
        self.pushButton_plus.clicked.connect(lambda: self.insertSpecialCharacters("+"))
        self.pushButton_minus = self.findChild(QtWidgets.QPushButton, 'pushButton_minus')
        self.pushButton_minus.clicked.connect(lambda: self.insertSpecialCharacters("-"))
        self.pushButton_slash = self.findChild(QtWidgets.QPushButton, 'pushButton_slash')
        self.pushButton_slash.clicked.connect(lambda: self.insertSpecialCharacters("/"))
        self.pushButton_star = self.findChild(QtWidgets.QPushButton, 'pushButton_star')
        self.pushButton_star.clicked.connect(lambda: self.insertSpecialCharacters("*"))

        # Add new word to dict
        self.pushButton_add_to_dict.clicked.connect(lambda: self.addWordToDict())
        # Update word frequency
        self.pushButton_update_word_freq.clicked.connect(lambda: T8WordMatching.saveWordFrequency())
        # List containing 1 for each upper case and 0 for each lower case for the current word.
        self.letter_case_list = []

        self.show()


    def addWordToDict(self):
        """Add new word to dictionary
        """
        T8WordMatching.addWordToDict(self.lineEdit_add_to_dict.text())
        self.lineEdit_add_to_dict.clear()
        
        if len(self.buttonInputList) >= 1:
            self.generateText()

        self.lineEdit_written_text.setFocus() # move cursor to lineEdit


    def clicked(self, button):
        """Append pressed button to input button list and find new matching words

        Args:
            button (string): Input buttons
        """
        self.buttonInputList.append(button)
        self.label_keyboard_input.setText(''.join([str(elem) for elem in self.buttonInputList]))

        if len(self.buttonInputList) >= 1:
            self.generateText()

        self.lineEdit_written_text.setFocus() # move cursor to lineEdit


    def onScreenKeyboard(self, char):
        """Connects input of onscreen keyboard to add custom words to dictionary

        Args:
            char (string): Input Character from onscreen keyboard
        """
        # Handle shift, make upper case if shift is active
        if self.shift is True:
            char = char.upper()
            self.toggleShift()

        self.lineEdit_add_to_dict.setText(self.lineEdit_add_to_dict.text() + char)


    def toggleShift(self):
        """Toggle both shift buttons synced
        """
        if self.shift is True:
            self.shift = False
            self.pushButton_shift.setDown(False)
            self.pushButton_shift_2.setDown(False)
        else:
            self.shift = True
            self.pushButton_shift.setDown(True)
            self.pushButton_shift_2.setDown(True)


    def onScreenBackspace(self):
        """Remove last character from custom word which shall be added to dict
        """
        self.lineEdit_add_to_dict.setText(self.lineEdit_add_to_dict.text()[:-1])


    def insertSpecialCharacters(self, char):
        """Insert special characters in written text field and clear labels

        Args:
            char (string): Special character
        """
        self.lineEdit_written_text.setText(self.lineEdit_written_text.text() + char)
        if len(self.word_selector_list) > 0 and self.word_selector_list.currentItem() is not None:          
            # Update word frequency dictionary
            T8WordMatching.updateWordFrequency(self.word_selector_list.currentItem().text())
            # Reset labels
            self.label_keyboard_input.setText("")
            self.buttonInputList.clear()
            self.letter_case_list.clear()
            self.selected_word_label.clear()
            self.word_selector_list.clear()

        self.lineEdit_written_text.setFocus() # move cursor to lineEdit

    
    def enterWordSelection(self):
        """Enter currently selected word in written text
        """
        # Find index of first letter of last word.
        last_special_char_idx = 0
        for char_idx in reversed(range(len(self.lineEdit_written_text.text()))):
            if not self.lineEdit_written_text.text()[char_idx].isalpha():
                last_special_char_idx = char_idx + 1
                break
        # Update written text in text field
        static_text = self.lineEdit_written_text.text()[:last_special_char_idx]
        if len(self.word_selector_list) > 0 and self.word_selector_list.currentItem() is not None:
            self.lineEdit_written_text.setText(static_text + self.transformUpperCase(self.word_selector_list.currentItem().text()))
        elif len(self.word_selector_list) == 0:
            self.lineEdit_written_text.setText(static_text)

        self.lineEdit_written_text.setFocus() # move cursor to lineEdit


    def transformUpperCase(self, word):
        """Transform current word to upper case based on letter_case_list

        Args:
            word (string): Word to be transformed to upper case

        Returns:
            string: Transformed word
        """
        transformed_word = []
        for i, letter in enumerate(self.word_selector_list.currentItem().text()):
            if i < len(self.letter_case_list) and self.letter_case_list[i] == 1:
                transformed_word.append(letter.upper())
            else:
                transformed_word.append(letter)
        transformed_word = "".join(transformed_word)
        
        return transformed_word


    def updateLetterCaseList(self, case):
        """Updates letter_case_list based on new input

        Args:
            case (int): 0 for lower case and 1 for upper case
        """
        if case == 0:
            self.letter_case_list.append(case)
        else:   # this is the case for long pressing letter buttons
            self.letter_case_list[-1] = case


    def extractLetterCaseList(self, word):
        """Extracts letter_case_list of a given word. Used when deleting previous word

        Args:
            word (string): Word to extract letter_case_list from
        """
        for char in word:
            if char.isupper():
                self.letter_case_list.append(1)
            else:
                self.letter_case_list.append(0)


    def generateText(self):
        """Search for matching words based on keyboard input
           Fill word selection list with available options
           Use selected option in written text
        """
        results = T8WordMatching.searchData(self.label_keyboard_input.text())
        self.word_selector_list.clear()

        # Update list with word selections
        if results:
            # Matched words with mathing length to T8 code
            for suggested_word, _ in results[0]:
                self.word_selector_list.addItem(suggested_word)
            # Matched words with larger length
            for suggested_word, _ in results[1]:
                self.word_selector_list.addItem(suggested_word)

        self.word_selector_list.setCurrentItem(self.word_selector_list.item(0))

        # Display selected word
        try:
            self.selected_word_label.setText(self.word_selector_list.currentItem().text())
            self.selected_word_label.setStyleSheet('color: green')
        except:
            self.selected_word_label.setText('no matching words!')
            self.selected_word_label.setStyleSheet('color: orange')

        # Use first word option in written text
        self.enterWordSelection()


    def spaceClicked(self):
        """Execute when space button is clicked
        """
        if len(self.word_selector_list) > 0 and self.word_selector_list.currentItem() is not None:            
            # Use current word selection in written text
            self.enterWordSelection()
            # Update word frequency dictionary
            T8WordMatching.updateWordFrequency(self.word_selector_list.currentItem().text())
            # Reset labels
            self.label_keyboard_input.setText("")
            self.buttonInputList.clear()
            self.letter_case_list.clear()
            self.selected_word_label.clear()
            self.word_selector_list.clear()

        self.lineEdit_written_text.setText(self.lineEdit_written_text.text() + " ")
        self.lineEdit_written_text.setFocus() # move cursor to lineEdit


    def enterClicked(self):
        #TODO implement enter button
        pass


    def nextClicked(self):
        """Triggered when clicking next button. Used to iterate through suggested word list
        """
        if len(self.buttonInputList) > 0:
            current_index = self.word_selector_list.currentRow()
            if current_index >= len(self.word_selector_list) - 1:
                self.word_selector_list.setCurrentItem(self.word_selector_list.item(0))
            else:
                self.word_selector_list.setCurrentItem(self.word_selector_list.item(current_index+1))

            try:
                self.selected_word_label.setText(self.word_selector_list.currentItem().text())
                self.selected_word_label.setStyleSheet('color: green')
            except:
                self.selected_word_label.setText('no matching words!')
                self.selected_word_label.setStyleSheet('color: orange')

            # Use current word selection in written text
            self.enterWordSelection()


    def backspaceClicked(self):
        """Triggered when long pressing next button. Delete last character and update all labels. Transform last word to T8.
        """
        if len(self.buttonInputList) > 0:
            self.buttonInputList.pop()
            self.letter_case_list.pop()
            self.label_keyboard_input.setText(''.join([str(elem) for elem in self.buttonInputList]))
            self.generateText()
        else:
            # Check if any text is written
            if self.lineEdit_written_text.text() != "":
                # Delete last char if it is not a letter
                if not self.lineEdit_written_text.text()[-1].isalpha(): # check if last char is a letter
                    self.lineEdit_written_text.setText(self.lineEdit_written_text.text()[:-1])
                
                if len(self.lineEdit_written_text.text()) > 0 and self.lineEdit_written_text.text()[-1].isalpha():
                    # Find index of first letter of last word.
                    last_word_idx = 0
                    for char_idx in reversed(range(len(self.lineEdit_written_text.text()))):
                        if not self.lineEdit_written_text.text()[char_idx].isalpha():
                            last_word_idx = char_idx + 1
                            break
                    # Transform last word to T8 code
                    last_word = self.lineEdit_written_text.text()[last_word_idx:]
                    self.extractLetterCaseList(last_word)
                    self.buttonInputList = list(''.join(T8WordMatching.m[c] for c in last_word.lower()))
                    self.label_keyboard_input.setText(''.join([str(elem) for elem in self.buttonInputList]))
                    self.generateText()

        self.lineEdit_written_text.setFocus() # move cursor to lineEdit
                    

    def randomSentences(self):
        """Return random phrases from a text file as a user task

        Returns:
            string: Contains the random phrase
        """
        with open(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'dicts', 'phrases1.txt')) as phrase_file:
            phrase_file = phrase_file.read().split("\n")
        randomPhrase = random.choice(phrase_file)
        return randomPhrase

