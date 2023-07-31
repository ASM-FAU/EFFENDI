from PyQt5 import QtWidgets
from gui.gui import Ui_MainWindow
from gui import T8WordMatching


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.pushButton1.clicked.connect(lambda: self.clicked("2"))
        self.pushButton2.clicked.connect(lambda: self.clicked("3"))
        self.pushButton3.clicked.connect(lambda: self.clicked("4"))
        self.pushButton4.clicked.connect(lambda: self.clicked("5"))
        self.pushButton5.clicked.connect(lambda: self.search())
        self.pushButton6.clicked.connect(lambda: self.clicked("space"))
        self.pushButton7.clicked.connect(lambda: self.clicked("6"))
        self.pushButton8.clicked.connect(lambda: self.clicked("7"))
        self.pushButton9.clicked.connect(lambda: self.clicked("8"))
        self.pushButton10.clicked.connect(lambda: self.clicked("9"))

    def clicked(self, button):
        if button == "space":
            self.label.setText("No Entry")
            self.label_3.setText("")
        else:
            if self.label.text() == "No Entry":
                self.label.setText("")
            self.label.setText(self.label.text() + button)
            self.search()
            print(self.label.text())

    def search(self):
        results = T8WordMatching.search(self.label.text())
        text = ""
        i = 1
        if not results:
            self.label_3.setText("No suggestions found.")
        else:
            for m, o in results[0]:
                if i % 5 == 0:
                    text = text + m + ", \n"
                else:
                    text = text + m + ", "
                i += 1
            for m, o in results[1]:
                if i % 5 == 0:
                    text = text + m + ", \n"
                else:
                    text = text + m + ", "
                i += 1
        self.label_3.setText(text[:30])