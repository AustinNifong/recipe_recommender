
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
import sys

class Window(QDialog):
  
    def __init__(self):
        super(Window, self).__init__()
        self.setStyleSheet("background-color: pink;")
        self.setWindowTitle("Recipe Recommender and Grocery Shopping")
        self.setGeometry(300, 150, 600, 770)

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
        self.output = QComboBox()
        self.output.addItems(["Single recipe", "Meal plan"])
        self.servings = QLineEdit()
        self.meals = QLineEdit()
        self.allergies = QLineEdit()
        self.diet = QComboBox()
        self.diet.addItems(["NA", "vegan"])
        self.pref = QLineEdit()

        self.createForm()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.reject)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.form)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

        self.requirements = QtWidgets.QLabel(self)
        self.requirements.move(240, 470)
        self.requirements.resize(105,30)
        self.define = QtWidgets.QLabel(self)
        self.define.move(230, 500)
        self.define.resize(125,30)

        self.D = QtWidgets.QLabel(self)
        self.D.move(195, 530)
        self.D.resize(70,30)
        self.PS = QtWidgets.QLabel(self)
        self.PS.move(190, 560)
        self.PS.resize(75,30)
        self.PM = QtWidgets.QLabel(self)
        self.PM.move(205, 590)
        self.PM.resize(60,30)
        self.PSPM = QtWidgets.QLabel(self)
        self.PSPM.move(130, 620)
        self.PSPM.resize(135,30)

        self.DV = QtWidgets.QLabel(self)
        self.DV.move(270, 530)
        self.DV.resize(160,30)
        self.PSV = QtWidgets.QLabel(self)
        self.PSV.move(270, 560)
        self.PSV.resize(160,30)
        self.PMV = QtWidgets.QLabel(self)
        self.PMV.move(270, 590)
        self.PMV.resize(160,30)
        self.PSPMV = QtWidgets.QLabel(self)
        self.PSPMV.move(270, 620)
        self.PSPMV.resize(160,30)
  
    def getInfo(self):
        self.validateInput()
        self.printRequirements()

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

        self.all_data['output'] = self.output.currentText()

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

    def printRequirements(self):
        self.requirements.setText('REQUIREMENTS:')
        self.define.setText('Calories/Protein/Fat')

        self.D.setText('Total Daily:')
        self.PS.setText('Per Serving:')
        self.PM.setText('Per Meal:')
        self.PSPM.setText('Per Serving Per Meal:')

        self.caloriesPS = self.getCalories()
        self.caloriesD = self.caloriesPS * self.all_data['servings']
        self.caloriesPM = self.caloriesD / self.all_data['meals']
        self.caloriesPSPM = self.caloriesPS / self.all_data['meals']

        self.proteinD = self.getProtein()
        self.proteinPS = self.proteinD / self.all_data['servings']
        self.proteinPM = self.proteinD / self.all_data['meals']
        self.proteinPSPM = self.proteinPS / self.all_data['meals']

        self.fatD = self.getFat()
        self.fatPS = self.fatD / self.all_data['servings']
        self.fatPM = self.fatD / self.all_data['meals']
        self.fatPSPM = self.fatPS / self.all_data['meals']

        self.DV.setText(str(round(self.caloriesD, 2)) + '/' + str(round(self.proteinD, 2)) + 'g' + '/' + str(round(self.fatD, 2)) + 'g')
        self.PSV.setText(str(round(self.caloriesPS, 2)) + '/' + str(round(self.proteinPS, 2)) + 'g' + '/' + str(round(self.fatPS, 2)) + 'g')
        self.PMV.setText(str(round(self.caloriesPM, 2)) + '/' + str(round(self.proteinPM, 2)) + 'g' + '/' + str(round(self.fatPM, 2)) + 'g')
        self.PSPMV.setText(str(round(self.caloriesPSPM, 2)) + '/' + str(round(self.proteinPSPM, 2)) + 'g' + '/' + str(round(self.fatPSPM, 2)) + 'g')

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

    def getProtein(self):
        return self.all_data['weight'] / 20 * 7

    def getFat(self):
        return self.caloriesD * 0.3 / 9
  
    def createForm(self):
        layout = QFormLayout()
        layout.addRow(QLabel("First Name:"), self.fname)
        layout.addRow(QLabel("Last Name:"), self.lname)
        layout.addRow(QLabel("Email:"), self.email)
        layout.addRow(QLabel("Age:"), self.age)
        layout.addRow(QLabel("Gender:"), self.gender)
        layout.addRow(QLabel("Height(feet):"), self.heightF)
        layout.addRow(QLabel("Height(inches):"), self.heightI)
        layout.addRow(QLabel("Activity:"), self.activity)
        layout.addRow(QLabel("Weight(lbs):"), self.weight)
        layout.addRow(QLabel("Output:"), self.output)
        layout.addRow(QLabel("Number of Servings:"), self.servings)
        layout.addRow(QLabel("Meals per Day:"), self.meals)
        layout.addRow(QLabel("Food Allergies:"), self.allergies)
        layout.addRow(QLabel("Diet:"), self.diet)
        layout.addRow(QLabel("Preferred Meals/Servings:"), self.pref)
        self.form.setLayout(layout)
  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())