import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone1App.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()  # loads list of states into stateList on UI
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)  # tells ui which function to call during event
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)

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

    # uses executeQuery to get list of states for stateList (comboBox)
    def loadStateList(self):
        self.ui.stateList.clear()
        # query to be run on business table
        sql_str = "Select distinct state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:  # add result to stateList
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed!")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    # uses executeQuery to get list of cities for cityList (listWidget) according to selected state
    # and businesses for businessTable (table) according to selected state
    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if self.ui.stateList.currentIndex() >= 0:
            # query to be run on business table
            sql_str = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:  # add results to cityList
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed!")

            # clear business table before adding new values
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)

            # query to be run on business table
            sql_str = "SELECT name,city,state FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section (""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)   # horizontal header style
                self.ui.businessTable.setColumnCount(len(results[0]))   # set number of columns (3)
                self.ui.businessTable.setRowCount(len(results))         # set number of rows
                # horizontal header labels
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
                # resize columns
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                currentRowCount = 0
                for row in results:  # add results to businessTable
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed!")

    # uses executeQuery to get list of businesses for businessTable (table) according to city and state
    def cityChanged(self):
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0:
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT name,city,state FROM business WHERE state ='" + state + "' AND city= '" + city + "' ORDER BY name;"

            # clear business table before adding new values
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)

            try:
                results = self.executeQuery(sql_str)
                style = "::section (""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)  # horizontal header style
                self.ui.businessTable.setColumnCount(len(results[0]))  # set number of columns (3)
                self.ui.businessTable.setRowCount(len(results))  # set number of rows
                # horizontal header labels
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
                # resize columns
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                currentRowCount = 0
                for row in results:  # add results to businessTable
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())
