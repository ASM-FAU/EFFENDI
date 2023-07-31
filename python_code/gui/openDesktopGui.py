# from gui import T8WordMatching
import os
import sys

from PyQt5 import QtWidgets, uic, QtCore
from pyautogui import press, typewrite, hotkey
import keyboard
import ctypes


class DesktopUi(QtWidgets.QMainWindow):

    def __init__(self, t8_word_matching):
        super(DesktopUi, self).__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ui', 'desktop_expandable.ui'), self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # window stays always on top
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # removes title bar

        self.t8_word_matching = t8_word_matching
        
        self.positionWindow()
        

        #########################################################################
        # T8 Buttons
        # self.buttons = []

        # self.button1 = self.findChild(QtWidgets.QPushButton, 'pushButton0')
        # self.button1.clicked.connect(lambda: self.clicked("2"))
        # self.button2 = self.findChild(QtWidgets.QPushButton, 'pushButton1')
        # self.button2.clicked.connect(lambda: self.clicked("3"))
        # self.button3 = self.findChild(QtWidgets.QPushButton, 'pushButton2')
        # self.button3.clicked.connect(lambda: self.clicked("4"))
        # self.button4 = self.findChild(QtWidgets.QPushButton, 'pushButton3')
        # self.button4.clicked.connect(lambda: self.clicked("5"))
        # self.button5 = self.findChild(QtWidgets.QPushButton, 'pushButton4')
        # self.button5.clicked.connect(lambda: self.nextClicked())

        # self.button6 = self.findChild(QtWidgets.QPushButton, 'pushButton5')
        # self.button6.clicked.connect(lambda: self.spaceClicked())
        # self.button7 = self.findChild(QtWidgets.QPushButton, 'pushButton6')
        # self.button7.clicked.connect(lambda: self.clicked("6"))
        # self.button8 = self.findChild(QtWidgets.QPushButton, 'pushButton7')
        # self.button8.clicked.connect(lambda: self.clicked("7"))
        # self.button9 = self.findChild(QtWidgets.QPushButton, 'pushButton8')
        # self.button9.clicked.connect(lambda: self.clicked("8"))
        # self.button10 = self.findChild(QtWidgets.QPushButton, 'pushButton9')
        # self.button10.clicked.connect(lambda: self.clicked("9"))
        # # Backspace - triggered through long pressing next button (1)
        # self.button_backspace = self.findChild(QtWidgets.QPushButton, 'backspace')
        # self.button_backspace.clicked.connect(lambda: self.backspaceClicked())
        # # Enter - triggered through long pressing space button (10)
        # self.button_enter = self.findChild(QtWidgets.QPushButton, 'enter')
        # self.button_enter.clicked.connect(lambda: self.enterClicked())

        # self.buttons.append(self.button1)
        # self.buttons.append(self.button2)
        # self.buttons.append(self.button3)
        # self.buttons.append(self.button4)
        # self.buttons.append(self.button5)
        # self.buttons.append(self.button6)
        # self.buttons.append(self.button7)
        # self.buttons.append(self.button8)
        # self.buttons.append(self.button9)
        # self.buttons.append(self.button10)

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

        ###########################################################################
        # Shortcuts
        self.pushButton_copy = self.findChild(QtWidgets.QPushButton, 'pushButton_copy')
        self.pushButton_copy.clicked.connect(lambda: self.controlKeys("c"))
        self.pushButton_paste = self.findChild(QtWidgets.QPushButton, 'pushButton_paste')
        self.pushButton_paste.clicked.connect(lambda: self.controlKeys("v"))
        self.pushButton_cut = self.findChild(QtWidgets.QPushButton, 'pushButton_cut')
        self.pushButton_cut.clicked.connect(lambda: self.controlKeys("x"))
        self.pushButton_select_all = self.findChild(QtWidgets.QPushButton, 'pushButton_select_all')
        self.pushButton_select_all.clicked.connect(lambda: self.controlKeys("a"))
        self.pushButton_save = self.findChild(QtWidgets.QPushButton, 'pushButton_save')
        self.pushButton_save.clicked.connect(lambda: self.controlKeys("s"))
        self.pushButton_revert = self.findChild(QtWidgets.QPushButton, 'pushButton_revert')
        self.pushButton_revert.clicked.connect(lambda: self.controlKeys("z"))
        self.pushButton_find = self.findChild(QtWidgets.QPushButton, 'pushButton_find')
        self.pushButton_find.clicked.connect(lambda: self.controlKeys("f"))
        self.pushButton_print = self.findChild(QtWidgets.QPushButton, 'pushButton_print')
        self.pushButton_print.clicked.connect(lambda: self.controlKeys("p"))

        # Hide and show UI
        self.pushButton_show.hide()
        self.pushButton_hide.clicked.connect(lambda: self.hideUi())
        self.pushButton_show.clicked.connect(lambda: self.showUi())

        # Add new word to dict
        self.pushButton_save_dict.clicked.connect(lambda: self.saveDict())
        self.pushButton_save_dict_as.clicked.connect(lambda: self.saveDictAs())
        # Update word frequency
        self.pushButton_update_dict.clicked.connect(lambda: self.updateDict())
        # Expand window to show add to dict keyboard
        self.pushButton_expand_add_to_dict.clicked.connect(lambda: self.expandWindow())
        self.window_expanded = False
        # Selecting word by mouse
        self.word_selector_list.itemSelectionChanged.connect(lambda: self.enterWordSelection())

        # List containing 1 for each upper case and 0 for each lower case for the current word.
        self.letter_case_list = []
        self.prev_word_len = 0  # stores the length of the previously entered word
        self.focused_window = None  # stores the currently active window
        self.buttonInputList = []   # stores entered T8 code in list

        self.show()

        self.effendi_window_id = ctypes.windll.user32.GetForegroundWindow() # Stores the window ID of the effendi application


    def positionWindow(self):
        """Calculates window position and moves to bottom center of the screen above task bar
        """
        ag = QtWidgets.QDesktopWidget().availableGeometry()
        x = int((ag.width() - self.frameGeometry().width()) / 2)
        y = ag.height() - self.frameGeometry().height()

        self.move(x,y)


    def expandWindow(self):
        """Expands window to show UI to add new words to the dictionary
        """
        if self.window_expanded is False:
            self.setGeometry(self.pos().x(), self.pos().y(), 1144, self.frameGeometry().height())
            self.window_expanded = True
        else:
            self.setGeometry(self.pos().x(), self.pos().y(), 653, self.frameGeometry().height())
            self.window_expanded = False

        self.positionWindow()


    def hideUi(self):
        self.pushButton_show.show()
        self.setGeometry(self.pos().x(), self.pos().y(), 95, 36)
        self.positionWindow()


    def showUi(self):
        self.pushButton_show.hide()
        self.setGeometry(self.pos().x(), self.pos().y(), 653, 174)
        self.positionWindow()


    def updateDict(self):
        """Add new word to dictionary
        """
        self.t8_word_matching.addWordToDict(self.lineEdit_add_to_dict.text())
        self.lineEdit_add_to_dict.clear()
        
        if len(self.buttonInputList) >= 1:
            self.generateText()


    def saveDict(self):
        """Add new word to dictionary
        """
        # self.t8_word_matching.addWordToDict(self.lineEdit_add_to_dict.text())
        # self.lineEdit_add_to_dict.clear()
        self.t8_word_matching.updateDict()
        
        # if len(self.buttonInputList) >= 1:
        #     self.generateText()


    def saveDictAs(self):
        """Save dict as json file
        """
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Dictionary File", os.path.join("python_code", "personal_dicts"), "JSON File (*.json)", options=options)
        self.t8_word_matching.saveDict(file_name)


    def clicked(self, button):
        """Append pressed button to input button list and find new matching words

        Args:
            button (string): Input buttons
        """
        self.buttonInputList.append(button)
        self.label_keyboard_input.setText(''.join([str(elem) for elem in self.buttonInputList]))
        if len(self.buttonInputList) >= 1:
            self.generateText()

        self.focused_window = ctypes.windll.user32.GetForegroundWindow()


    def onScreenKeyboard(self, char):
        """Connects input of onscreen keyboard to add custom words to dictionary

        Args:
            char (string): Input Character from onscreen keyboard
        """
        try:
            self.lineEdit_add_to_dict.setText(self.lineEdit_add_to_dict.text() + char)
        except Exception as e:
            print(e)


    def onScreenBackspace(self):
        """Remove last character from custom word which shall be added to dict
        """
        try:
            self.lineEdit_add_to_dict.setText(self.lineEdit_add_to_dict.text()[:-1])
        except Exception as e:
            print(e)


    def insertSpecialCharacters(self, char):
        """Insert special characters in written text field and clear labels

        Args:
            char (string): Special character
        """
        ctypes.windll.user32.SetForegroundWindow(self.focused_window)

        if len(self.word_selector_list) > 0 and self.word_selector_list.currentItem() is not None:          
            # Update word frequency dictionary
            try:
                self.t8_word_matching.updateWordFrequency(self.word_selector_list.currentItem().text())
            except Exception as e:
                print(e)
            # Reset labels
            self.label_keyboard_input.setText("")
            self.buttonInputList.clear()
            self.letter_case_list.clear()
            self.word_selector_list.clear()

        press(char)
        self.prev_word_len = 0


    def controlKeys(self, key):
        """Control Keys on the onscreen keyboard (copy, paste, save, print, ...)

        Args:
            key (char): The key to be combined with "ctrl"
        """
        # Put previous window into foreground to keep the focus
        ctypes.windll.user32.SetForegroundWindow(self.focused_window)

        if len(self.word_selector_list) > 0 and self.word_selector_list.currentItem() is not None:          
            # Update word frequency dictionary
            try:
                self.t8_word_matching.updateWordFrequency(self.word_selector_list.currentItem().text())
            except Exception as e:
                print(e)
            # Reset labels and lists
            self.label_keyboard_input.setText("")
            self.buttonInputList.clear()
            self.letter_case_list.clear()
            self.word_selector_list.clear()
        
        # Execute Hotkey
        hotkey('ctrl', key)
        self.prev_word_len = 0

    
    def enterWordSelection(self):
        """Enter currently selected word in written text
        """
        # Focus on active window
        ctypes.windll.user32.SetForegroundWindow(self.focused_window)
        # delete previous entered word
        backspace = ['backspace'] * self.prev_word_len
        press(backspace)

        # enter new word
        if len(self.word_selector_list) > 0 and self.word_selector_list.currentItem() is not None:
            # typewrite(self.transformUpperCase(self.word_selector_list.currentItem().text()))
            keyboard.write(self.transformUpperCase(self.word_selector_list.currentItem().text()))   # this works also for special chars like äöü

            self.prev_word_len = len(self.word_selector_list.currentItem().text())
        else:
            self.prev_word_len = 0


    def transformUpperCase(self, word):
        """Transform current word to upper case based on letter_case_list

        Args:
            word (string): Word to be transformed to upper case

        Returns:
            string: Transformed word
        """
        transformed_word = []
        for i, letter in enumerate(word):
            if i < len(self.letter_case_list) and self.letter_case_list[i] == 1 and letter not in ["ß", "µ"]:
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
        results = self.t8_word_matching.searchData(self.label_keyboard_input.text())
        self.word_selector_list.clear()

        print("", flush=True)   # For some weird reason the selection only works when there's a print
        # Update list with word selections
        if results:
            # Matched words with mathing length to T8 code
            for suggested_word in results[0]:
                if suggested_word != "":
                    self.word_selector_list.addItem(self.transformUpperCase(suggested_word))
                    print("", flush=True)  # For some weird reason the selection only works when there's a print
            # Matched words with larger length
            for suggested_word in results[1]:
                if suggested_word != "":
                    self.word_selector_list.addItem(self.transformUpperCase(suggested_word))
                    print("", flush=True)  # For some weird reason the selection only works when there's a print

        self.word_selector_list.setCurrentItem(self.word_selector_list.item(0))
 
        if self.word_selector_list.currentItem() != None and self.word_selector_list.currentItem().text() == "":
            self.word_selector_list.setCurrentItem(self.word_selector_list.item(0))

        # Use first word option in written text
        self.enterWordSelection()


    def spaceClicked(self):
        """Execute when space button is clicked
        """
        if len(self.word_selector_list) > 0 and self.word_selector_list.currentItem() is not None:            
            # Update word frequency dictionary
            self.t8_word_matching.updateWordFrequency(self.word_selector_list.currentItem().text())
        
        # Reset labels
        self.label_keyboard_input.setText("")
        self.buttonInputList.clear()
        self.letter_case_list.clear()
        self.word_selector_list.clear()

        press('space')
        self.prev_word_len = 0


    def enterClicked(self):
        """Execute when enter button is clicked (long pressing space button)
        """
        if len(self.word_selector_list) > 0 and self.word_selector_list.currentItem() is not None:            
            # Update word frequency dictionary
            self.t8_word_matching.updateWordFrequency(self.word_selector_list.currentItem().text())
        
        # Reset labels
        self.label_keyboard_input.setText("")
        self.buttonInputList.clear()
        self.letter_case_list.clear()
        self.word_selector_list.clear()

        press('enter')
        self.prev_word_len = 0


    def nextClicked(self):
        """Triggered when clicking next button. Used to iterate through suggested word list
        """
        print(self.word_selector_list.currentRow())
        if len(self.buttonInputList) > 0:
            current_index = self.word_selector_list.currentRow()
            if current_index >= len(self.word_selector_list) - 1:
                self.word_selector_list.setCurrentItem(self.word_selector_list.item(0))
            else:
                self.word_selector_list.setCurrentItem(self.word_selector_list.item(current_index+1))

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
            press('backspace')

