
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
import sys

class Window(QDialog):
  
    def __init__(self):
        super(Window, self).__init__()
        self.setStyleSheet("background-color: pink;")
        self.setWindowTitle("Recipe Recommender and Grocery Shopping")
        self.setGeometry(300, 150, 1000, 800)

        self.form = QGroupBox("Dietary Metrics")
        self.fname = QLineEdit()
        self.lname = QLineEdit()
        self.email = QLineEdit()
        self.age = QSpinBox()
        self.gender = QLineEdit()
        self.heightF = QComboBox()
        self.heightF.addItems(["0", "1", "2", "3", "4", "5", "6", "7"])
        self.heightI = QComboBox()
        self.heightI.addItems(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
        self.activity = QComboBox()
        self.activity.addItems(["little-no exercise", "light exercise, 1-3 days/week", "moderate exercise, 3-5 days/week", "hard exercise, 6-7 days a week", "very hard exercise or 2x training"])
        self.weight = QLineEdit()
        self.servings = QLineEdit()
        self.meals = QLineEdit()
        self.allergies = QLineEdit()
        self.diet = QComboBox()
        self.diet.addItems(["NA", "vegetarian", "vegan", "pescatarian"])
        self.pref = QLineEdit()

        self.createForm()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.reject)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.form)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

        self.results = QtWidgets.QLabel(self)
        self.results.move(460, 480)
        self.results.resize(65,30)
        self.CPS = QtWidgets.QLabel(self)
        self.CPS.move(395, 510)
        self.CPS.resize(130,30)
        self.C = QtWidgets.QLabel(self)
        self.C.move(405, 540)
        self.C.resize(120,30)
        self.CPSPM = QtWidgets.QLabel(self)
        self.CPSPM.move(340, 570)
        self.CPSPM.resize(185,30)
        self.CPM = QtWidgets.QLabel(self)
        self.CPM.move(415, 600)
        self.CPM.resize(110,30)

        self.CPSV = QtWidgets.QLabel(self)
        self.CPSV.move(535, 510)
        self.CPSV.resize(55,30)
        self.CV = QtWidgets.QLabel(self)
        self.CV.move(535, 540)
        self.CV.resize(55,30)
        self.CPSPMV = QtWidgets.QLabel(self)
        self.CPSPMV.move(535, 570)
        self.CPSPMV.resize(55,30)
        self.CPMV = QtWidgets.QLabel(self)
        self.CPMV.move(535, 600)
        self.CPMV.resize(55,30)
  
    def getInfo(self):
        print("Person First Name : {0}".format(self.fname.text()))
        print("Person Last Name : {0}".format(self.lname.text()))
        print("Person Email : {0}".format(self.email.text()))
        print("Age : {0}".format(self.age.text()))
        print("Gender : {0}".format(self.gender.text()))
        print("Height(feet) : {0}".format(self.heightF.currentText()))
        print("Height(inches) : {0}".format(self.heightI.currentText()))
        print("Activity : {0}".format(self.activity.currentText()))
        print("Weight : {0}".format(self.weight.text()))
        print("Number of Servings : {0}".format(self.servings.text()))
        print("Meals per Day : {0}".format(self.meals.text()))
        print("Allergies : {0}".format(self.allergies.text()))
        print("Diet : {0}".format(self.diet.currentText()))
        print("Preferred Meals/Ingredients : {0}".format(self.pref.text()))
        self.validateInput()
        self.printCalories()

    def validateInput(self):
        self.all_data = {}

        self.all_data['first name'] = self.fname.text()
        self.all_data['last name'] = self.lname.text()

        if '@' in self.email.text():
            self.all_data['email'] = self.email.text()
        else:
            self.all_data['email'] = ""

        if self.age.text().isnumeric():
            self.all_data['age'] = int(self.age.text())
        else:
            self.all_data['age'] = 30

        self.all_data['gender'] = self.gender.text()

        if self.heightF.currentText().isnumeric():
            self.all_data['height feet'] = int(self.heightF.currentText())
        else:
            self.all_data['height feet'] = 5

        if self.heightI.currentText().isnumeric():
            self.all_data['height inches'] = int(self.heightI.currentText())
        else:
            self.all_data['height inches'] = 6

        self.all_data['activity'] = self.activity.currentText()

        if self.weight.text().isnumeric():
            self.all_data['weight'] = int(self.weight.text())
        else:
            self.all_data['weight'] = 140

        if self.servings.text().isnumeric():
            self.all_data['servings'] = int(self.servings.text())
        else:
            self.all_data['servings'] = 1

        if self.meals.text().isnumeric():
            self.all_data['meals'] = int(self.meals.text())
        else:
            self.all_data['meals'] = 3

        self.all_data['allergies'] = self.allergies.text().split(", ")

        self.all_data['diet'] = self.diet.currentText()

        self.all_data['preferences'] = self.pref.text().split(", ")

    def printCalories(self):
        self.results.setText('RESULTS:')

        self.caloriesPS = self.getCalories()
        print("Calories per Serving: {0}".format(self.caloriesPS))
        self.CPS.setText('Calories per Serving:')
        self.CPSV.setText(str(round(self.caloriesPS, 2)))
        
        self.calories = self.caloriesPS * self.all_data['servings']
        print("Calories: {0}".format(self.calories))
        self.C.setText('Total DailyCalories:')
        self.CV.setText(str(round(self.calories, 2)))
        
        self.caloriesPSPM = self.caloriesPS / self.all_data['meals']
        print("Calories per Serving per Meal: {0}".format(self.caloriesPSPM))
        self.CPSPM.setText('Calories per Serving per Meal:')
        self.CPSPMV.setText(str(round(self.caloriesPSPM, 2)))
        
        self.caloriesPM = self.calories / self.all_data['meals']
        print("Calories per Meal: {0}".format(self.caloriesPM))
        self.CPM.setText('Calories per Meal:')
        self.CPMV.setText(str(round(self.caloriesPM, 2)))

    def getCalories(self):
    	if self.activity.currentText() == "light exercise, 1-3 days/week":
    		if self.gender.text() == "male":
    			return (88.362 + (13.397 * self.all_data['weight'] / 2.205) + (4.799 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (5.677 * self.all_data['age'])) * 1.375
    		if self.gender.text() == "female":
    			return (447.593 + (9.247 * self.all_data['weight'] / 2.205) + (3.098 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (4.33 * self.all_data['age'])) * 1.375
    		else:
    			return (267.9775 + (11.322 * self.all_data['weight'] / 2.205) + (3.9485 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (5.0035 * self.all_data['age'])) * 1.375
    	elif self.activity.currentText() == "moderate exercise, 3-5 days/week":
    		if self.gender.text() == "male":
    			return (88.362 + (13.397 * self.all_data['weight'] / 2.205) + (4.799 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (5.677 * self.all_data['age'])) * 1.55
    		if self.gender.text() == "female":
    			return (447.593 + (9.247 * self.all_data['weight'] / 2.205) + (3.098 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (4.33 * self.all_data['age'])) * 1.55
    		else:
    			return (267.9775 + (11.322 * self.all_data['weight'] / 2.205) + (3.9485 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (5.0035 * self.all_data['age'])) * 1.55
    	elif self.activity.currentText() == "hard exercise, 6-7 days a week":
    		if self.gender.text() == "male":
    			return (88.362 + (13.397 * self.all_data['weight'] / 2.205) + (4.799 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (5.677 * self.all_data['age'])) * 1.725
    		if self.gender.text() == "female":
    			return (447.593 + (9.247 * self.all_data['weight'] / 2.205) + (3.098 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (4.33 * self.all_data['age'])) * 1.725
    		else:
    			return (267.9775 + (11.322 * self.all_data['weight'] / 2.205) + (3.9485 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (5.0035 * self.all_data['age'])) * 1.725
    	elif self.activity.currentText() == "very hard exercise or 2x training":
    		if self.gender.text() == "male":
    			return (88.362 + (13.397 * self.all_data['weight'] / 2.205) + (4.799 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (5.677 * self.all_data['age'])) * 1.9
    		if self.gender.text() == "female":
    			return (447.593 + (9.247 * self.all_data['weight'] / 2.205) + (3.098 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (4.33 * self.all_data['age'])) * 1.9
    		else:
    			return (267.9775 + (11.322 * self.all_data['weight'] / 2.205) + (3.9485 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (5.0035 * self.all_data['age'])) * 1.9
    	else:
	    	if self.gender.text() == "male":
    			return (88.362 + (13.397 * self.all_data['weight'] / 2.205) + (4.799 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (5.677 * self.all_data['age'])) * 1.2
    		if self.gender.text() == "female":
    			return (447.593 + (9.247 * self.all_data['weight'] / 2.205) + (3.098 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (4.33 * self.all_data['age'])) * 1.2
    		else:
    			return (267.9775 + (11.322 * self.all_data['weight'] / 2.205) + (3.9485 * (self.all_data['height feet'] * 12 + self.all_data['height inches']) * 2.54) - (5.0035 * self.all_data['age'])) * 1.2
  
    def createForm(self):
        layout = QFormLayout()
        layout.addRow(QLabel("First Name"), self.fname)
        layout.addRow(QLabel("Last Name"), self.lname)
        layout.addRow(QLabel("Email"), self.email)
        layout.addRow(QLabel("Age"), self.age)
        layout.addRow(QLabel("Gender"), self.gender)
        layout.addRow(QLabel("Height(feet)"), self.heightF)
        layout.addRow(QLabel("Height(inches)"), self.heightI)
        layout.addRow(QLabel("Activity"), self.activity)
        layout.addRow(QLabel("Weight(lbs)"), self.weight)
        layout.addRow(QLabel("Number of Servings"), self.servings)
        layout.addRow(QLabel("Meals per Day"), self.meals)
        layout.addRow(QLabel("Food Allergies"), self.allergies)
        layout.addRow(QLabel("Diet"), self.diet)
        layout.addRow(QLabel("Preferred Meals/Servings"), self.pref)
        self.form.setLayout(layout)
  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())