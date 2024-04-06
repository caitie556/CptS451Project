import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone2App.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class milestone2(QMainWindow):
    def __init__(self):
        super(milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateMenu()  # loads list of states into stateMenu on UI
        self.ui.stateMenu.currentTextChanged.connect(self.stateChanged)  # tells ui which function to call during event
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipCodeList.itemSelectionChanged.connect(self.zipCodeChanged)
        self.ui.bname.textChanged.connect(self.getBusinessNames)

    # gets results of query when performed on business tables in milestone1db
    def executeQuery(self, sql_str):
        try:
            # replace current with own info
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='admin'")
        except:
            print("Unable to connect to the database!")
            return
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    # uses executeQuery to get list of states for stateMenu (comboBox)
    def loadStateMenu(self):
        self.ui.stateMenu.clear()
        # query to be run on business table
        sql_str = "Select distinct state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:  # add result to stateMenu
                self.ui.stateMenu.addItem(row[0])
        except:
            print("Query failed!")
        self.ui.stateMenu.setCurrentIndex(-1)
        self.ui.stateMenu.clearEditText()

    # uses executeQuery to get list of cities for cityList (listWidget) according to selected state
    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateMenu.currentText()
        if self.ui.stateMenu.currentIndex() >= 0:
            sql_str = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:  # add results to cityList
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed!")

    # uses executeQuery to get list of zip codes for zipCodeList (listWidget) according to city and state
    def cityChanged(self):
        self.ui.zipCodeList.clear()
        state = self.ui.stateMenu.currentText()
        city = self.ui.cityList.selectedItems()[0].text()
        sql_str = "SELECT distinct zipcode FROM business WHERE state ='" + state + "' AND city ='" + city + "' ORDER BY zipcode;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:  # add results to zipCodeList
                self.ui.zipCodeList.addItem(row[0])
        except:
            print("Query failed!")

    # uses executeQuery to get list of categories for bCatagoryList (listWidget) according to city, state, and zip code
    def zipCodeChanged(self):
        self.ui.bCategoryList.clear()
        state = self.ui.stateMenu.currentText()
        city = self.ui.cityList.selectedItems()[0].text()
        zip = self.ui.zipCodeList.selectedItems()[0].text()
        sql_str = "SELECT distinct category FROM business WHERE state ='" + state + "' AND city ='" + city + "'' AND zipcode ='" + zip + "' ORDER BY category;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:  # add results to bCategoryList
                self.ui.bCategoryList.addItem(row[0])
        except:
            print("Query failed!")

    def getBusinessNames(self):
        self.ui.businesses.clear()
        zip = self.ui.zipCodeList.selectedItems()[0].text()
        businessname = self.ui.bname.text()
        sql_str = "SELECT name FROM business WHERE zipcode ='" + zip + "' AND name LIKE '%" + businessname + "%' ORDER BY name;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.businesses.addItem(row[0])
        except:
            print("Query failed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec_())
