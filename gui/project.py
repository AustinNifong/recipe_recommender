from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys

class stacked(QWidget):

   def __init__(self):
      super(stacked, self).__init__()

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

      self.leftlist = QListWidget ()
      self.leftlist.insertItem (0, 'Form' )
      self.leftlist.insertItem (1, 'Recommendations' )
		
      self.stack1 = QWidget()
      self.stack2 = QWidget()
		
      self.stack1UI()
      self.stack2UI()
		
      self.Stack = QStackedWidget (self)
      self.Stack.addWidget(self.stack1)
      self.Stack.addWidget(self.stack2)
		
      hbox = QHBoxLayout(self)
      hbox.addWidget(self.leftlist)
      hbox.addWidget(self.Stack)

      self.setLayout(hbox)
      self.leftlist.currentRowChanged.connect(self.display)
      self.setGeometry(300, 150, 600, 770)
      self.setWindowTitle('Recipe Recommender and Grocery Shopping')
      self.show()

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

      self.caloriesPS = round(self.getCalories(), 2)
      self.caloriesD = round(self.caloriesPS * self.all_data['servings'], 2)
      self.caloriesPM = round(self.caloriesD / self.all_data['meals'], 2)
      self.caloriesPSPM = round(self.caloriesPS / self.all_data['meals'], 2)

      self.proteinD = round(self.getProtein(), 2)
      self.proteinPS = round(self.proteinD / self.all_data['servings'], 2)
      self.proteinPM = round(self.proteinD / self.all_data['meals'], 2)
      self.proteinPSPM = round(self.proteinPS / self.all_data['meals'], 2)

      self.fatD = round(self.getFat(), 2)
      self.fatPS = round(self.fatD / self.all_data['servings'], 2)
      self.fatPM = round(self.fatD / self.all_data['meals'], 2)
      self.fatPSPM = round(self.fatPS / self.all_data['meals'], 2)

      self.DV.setText(str(self.caloriesD) + '/' + str(self.proteinD) + 'g/' + str(self.fatD) + 'g')
      self.PSV.setText(str(self.caloriesPS) + '/' + str(self.proteinPS) + 'g/' + str(self.fatPS) + 'g')
      self.PMV.setText(str(self.caloriesPM) + '/' + str(self.proteinPM) + 'g/' + str(self.fatPM) + 'g')
      self.PSPMV.setText(str(self.caloriesPSPM) + '/' + str(self.proteinPSPM) + 'g/' + str(self.fatPSPM) + 'g')

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
		
   def stack1UI(self):
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
      
      self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
      self.buttonBox.accepted.connect(self.getInfo)
      layout.addWidget(self.buttonBox)

      self.requirements = QtWidgets.QLabel(self)
      self.requirements.move(300, 570)
      self.requirements.resize(105,30)
      self.define = QtWidgets.QLabel(self)
      self.define.move(290, 600)
      self.define.resize(125,30)

      self.D = QtWidgets.QLabel(self)
      self.D.move(255, 630)
      self.D.resize(70,30)
      self.PS = QtWidgets.QLabel(self)
      self.PS.move(250, 660)
      self.PS.resize(75,30)
      self.PM = QtWidgets.QLabel(self)
      self.PM.move(265, 690)
      self.PM.resize(60,30)
      self.PSPM = QtWidgets.QLabel(self)
      self.PSPM.move(190, 720)
      self.PSPM.resize(135,30)

      self.DV = QtWidgets.QLabel(self)
      self.DV.move(330, 630)
      self.DV.resize(160,30)
      self.PSV = QtWidgets.QLabel(self)
      self.PSV.move(330, 660)
      self.PSV.resize(160,30)
      self.PMV = QtWidgets.QLabel(self)
      self.PMV.move(330, 690)
      self.PMV.resize(160,30)
      self.PSPMV = QtWidgets.QLabel(self)
      self.PSPMV.move(330, 720)
      self.PSPMV.resize(160,30)

      self.stack1.setLayout(layout)
		
   def stack2UI(self):
      layout = QFormLayout()
      sex = QHBoxLayout()
      sex.addWidget(QRadioButton("Male"))
      sex.addWidget(QRadioButton("Female"))
      layout.addRow(QLabel("Sex"),sex)
      self.stack2.setLayout(layout)
		
   def display(self,i):
      self.Stack.setCurrentIndex(i)
		
def main():
   app = QApplication(sys.argv)
   ex = stacked()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()