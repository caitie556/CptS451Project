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
        self.loadBusinessTable()
        self.ui.pushButton.clicked.connect(self.loadPopularTable)
        self.ui.pushButton.clicked.connect(self.loadSuccessfulTable)
        self.ui.stateMenu.currentTextChanged.connect(self.stateChanged)  # tells ui which function to call during event
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipCodeList.itemSelectionChanged.connect(self.zipCodeChanged)
        self.ui.bCategoryList.itemSelectionChanged.connect(self.categoryChanged)

    # gets results of query when performed on business tables in your Yelp DB
    def executeQuery(self, sql_str):
        try:
            # replace current with own info
            conn = psycopg2.connect("dbname='yourdbhere' user='postgres' host='localhost' password='admin'")
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
        sql_str = "Select distinct state FROM Business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:  # add result to stateMenu
                self.ui.stateMenu.addItem(row[0])
        except:
            print("Query failed!")
        self.ui.stateMenu.setCurrentIndex(-1)
        self.ui.stateMenu.clearEditText()

    def loadBusinessTable(self):
        # clear business table before adding new values
        for i in reversed(range(self.ui.businesses.rowCount())):
            self.ui.businesses.removeRow(i)

        sql_str = "SELECT name, address, city, state, stars, review_count, reviewrating, numcheckins  FROM Business;"

        try:
            results = self.executeQuery(sql_str)
            self.ui.businesses.setColumnCount(len(results[0]))  # set number of columns (3)
            self.ui.businesses.setRowCount(len(results))  # set number of rows
            # horizontal header labels
            self.ui.businesses.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'State', 'Stars', 'Review Count', 'Average Rating', '# Check Ins'])

            currentRowCount = 0
            for row in results:  # add results to businesses
                for colCount in range(0, 4):
                    self.ui.businesses.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))

                for cols in range(4, 8):
                    self.ui.businesses.setItem(currentRowCount, cols, QTableWidgetItem(str(row[cols])))

                currentRowCount += 1
        except:
            print("Query Failed!")

    def loadPopularTable(self):
        if len(self.ui.zipCodeList.selectedItems()) != 0:
            # clear popular business table before adding new values
            self.ui.businessespopular.clear()
            self.ui.businessespopular.setRowCount(0)

            zip_code = self.ui.zipCodeList.selectedItems()[0].text()
            city = self.ui.cityList.selectedItems()[0].text()

            sql_str = "SELECT name, review_count, numcheckins FROM Business Where postal_code = '" + zip_code + "' AND city = '" + city + "' ORDER BY numcheckins DESC;"

            try:
                results = self.executeQuery(sql_str)
                self.ui.businessespopular.setColumnCount(3)
                self.ui.businessespopular.setHorizontalHeaderLabels(['Business Name', 'Review Count', '# Check Ins'])
                self.ui.businessespopular.setRowCount(len(results))
                for rowIndex, row in enumerate(results):
                    for colIndex, value in enumerate(row):
                        self.ui.businessespopular.setItem(rowIndex, colIndex, QTableWidgetItem(str(value)))

            except:
                print("Query Failed!")

        else:
            self.ui.businessespopular.clear()
            self.ui.businessespopular.setRowCount(0)

    def loadSuccessfulTable(self):
        if len(self.ui.zipCodeList.selectedItems()) != 0:
            # clear successful business table before adding new values
            self.ui.businessessuccess.clear()
            self.ui.businessessuccess.setRowCount(0)

            zip_code = self.ui.zipCodeList.selectedItems()[0].text()
            city = self.ui.cityList.selectedItems()[0].text()

            sql_str = "SELECT name, stars, reviewrating, review_count FROM Business Where postal_code = '" + zip_code + "' AND city = '" + city + "' AND reviewrating > 3.5 ORDER BY review_count DESC, reviewrating DESC;"

            try:
                results = self.executeQuery(sql_str)
                self.ui.businessessuccess.setColumnCount(4)
                self.ui.businessessuccess.setHorizontalHeaderLabels(
                    ['Business Name', 'Stars', 'Review Rating', 'Number of Reviews'])
                self.ui.businessessuccess.setRowCount(len(results))
                for rowIndex, row in enumerate(results):
                   for colIndex, value in enumerate(row):
                        self.ui.businessessuccess.setItem(rowIndex, colIndex, QTableWidgetItem(str(value)))
            except:
                print("Query Failed!")
        else:
            self.ui.businessessuccess.clear()
            self.ui.businessessuccess.setRowCount(0)

    # uses executeQuery to get list of cities for cityList (listWidget) according to selected state
    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateMenu.currentText()
        if self.ui.stateMenu.currentIndex() >= 0:
            sql_str = "SELECT distinct city FROM Business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:  # add results to cityList
                    self.ui.cityList.addItem(row[0])
                self.updateBusinesses("SELECT name, address, city, state, stars, review_count, reviewrating, numcheckins FROM Business WHERE state ='" + state + "';")
            except:
                print("Query failed!")

    # uses executeQuery to get list of zip codes for zipCodeList (listWidget) according to city and state
    def cityChanged(self):
        self.ui.zipCodeList.clear()
        if len(self.ui.cityList.selectedItems()) != 0:
            state = self.ui.stateMenu.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT distinct postal_code FROM Business WHERE state ='" + state + "' AND city ='" + city + "' ORDER BY postal_code;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:  # add results to zipCodeList
                    self.ui.zipCodeList.addItem(row[0])
                self.updateBusinesses("SELECT name, address, city, state, stars, review_count, reviewrating, numcheckins FROM Business WHERE state ='" + state + "' AND city ='" + city + "';")
            except:
                print("Query failed!")

    # uses executeQuery to get list of categories for bCategoryList (listWidget) according to city, state, and zip code
    def zipCodeChanged(self):
        self.ui.bCategoryList.clear()
        if len(self.ui.cityList.selectedItems()) != 0:
            if len(self.ui.zipCodeList.selectedItems()) != 0:
                state = self.ui.stateMenu.currentText()
                city = self.ui.cityList.selectedItems()[0].text()
                zip = self.ui.zipCodeList.selectedItems()[0].text()
                sql_str = "SELECT DISTINCT BusinessCategories.categoryName FROM BusinessCategories JOIN Business ON BusinessCategories.business_id = Business.business_id WHERE Business.state ='" + state + "' AND Business.city ='" + city + "' AND Business.postal_code ='" + zip + "' ORDER BY BusinessCategories.categoryName;"
                try:
                    results = self.executeQuery(sql_str)
                    for row in results:  # add results to bCategoryList
                        self.ui.bCategoryList.addItem(row[0])
                    self.updateBusinesses("SELECT name, address, city, state, stars, review_count, reviewrating, numcheckins FROM Business WHERE state ='" + state + "' AND city ='" + city + "' AND postal_code ='" + zip + "';")
                except:
                    print("Query failed!")

    def categoryChanged(self):
        if len(self.ui.bCategoryList.selectedItems()) != 0:
            state = self.ui.stateMenu.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zip = self.ui.zipCodeList.selectedItems()[0].text()
            category = self.ui.bCategoryList.selectedItems()[0].text()
            sql_str = "SELECT Business.name, Business.address FROM BusinessCategories JOIN Business ON BusinessCategories.business_id = Business.business_id WHERE Business.state ='" + state + "' AND Business.city ='" + city + "' AND Business.postal_code ='" + zip + "' AND BusinessCategories.categoryName ='" + category + "';"
            self.updateBusinesses(sql_str)

    def updateBusinesses(self, sql_str):
        # clear business table before adding new values
        for i in reversed(range(self.ui.businesses.rowCount())):
            self.ui.businesses.removeRow(i)

        try:
            results = self.executeQuery(sql_str)
            self.ui.businesses.setColumnCount(len(results[0]))  # set number of columns (3)
            self.ui.businesses.setRowCount(len(results))  # set number of rows
            # horizontal header labels
            self.ui.businesses.setHorizontalHeaderLabels(['Business Name', 'Address'])

            currentRowCount = 0
            for row in results:  # add results to businesses
                for colCount in range(0, 4):
                    self.ui.businesses.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))

                for cols in range(4, 8):
                    self.ui.businesses.setItem(currentRowCount, cols, QTableWidgetItem(str(row[cols])))
                currentRowCount += 1
        except:
            print("Query Failed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec_())