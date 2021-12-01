from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import pandas as pd
import numpy as np
import random

df_recipes = pd.read_csv("../datasets/Recipes.csv")
df_ing = pd.read_csv("../datasets/Ingredients.csv")
df_rec2ing = pd.read_csv("../datasets/Rec2Ing.csv")

#Searches through recipe title and ingredient title to find ones that CONTAINS the allergen
#Then filters the df_recipes dataframe to remove the allergens containing recipes
#Doing it this way to reduce time taken on merging datasets
#Searches based on df.str.contains function 
#Applies it directly to the df_recipes dataframe
def allergy_filter(allergies):
    if len(allergies)>=1 and allergies[0]!='':
        alg = [i+'*' for i in allergies]
        
        #get all ingredients whose name matches the allergies; merge it with rec2ing to get a list of recipeIDs
        dfi = df_ing[df_ing.IngredientName.str.lower().str.contains('|'.join(alg), na=False, regex=True)]
        rec2ingID_list = list(df_rec2ing.merge(dfi, on='IngredientID')['RecipeID'])
        
        #get all recipes whose title matches the allergies
        recList = list(df_recipes[df_recipes.Title.str.lower().str.contains('|'.join(alg), na=False, regex=True)]['RecipeID'])
        recList.append(rec2ingID_list)
        dfr = df_recipes[~df_recipes.RecipeID.isin(recList)]
    else:
        dfr = df_recipes
    
    return dfr

#Filter the inputted df using the isVegan attribute based on user input
def vegan_filter(vegan, dfr):
    if vegan == 'Vegan':
        df = dfr[dfr.isVegan=='1']
    elif vegan == "Strictly not vegan":
        df = dfr[dfr.isVegan=='0']
    else:
        df = dfr
        
    return df

#Exactly the same as allergy_filter. Only this time we return the df elemtns containing the search_term
def search_filter(search_term, df):
    if len(search_term)>=1 and search_term[0]!='':
        srch = [i+'*' for i in search_term]

        #get all ingredients whose name matches the allergies; merge it with rec2ing to get a list of recipeIDs
        dfi = df_ing[df_ing.IngredientName.str.lower().str.contains('|'.join(srch), na=False, regex=True)]
        rec2ingID_list = list(df_rec2ing.merge(dfi, on='IngredientID')['RecipeID'])

        #get all recipes whose title matches the allergies
        recList = list(df[df.Title.str.lower().str.contains('|'.join(srch), na=False, regex=True)]['RecipeID'])
        recList.append(rec2ingID_list)
        dfr = df[df.RecipeID.isin(recList)]
    else:
        dfr = df
    
    return dfr

#Filters based on calculated nutritional facts adding a +/- 10% buffer
def cal_filter(cal, protein, fat, df):
    return df[(df.Calories >= 0.9*cal) & (df.Calories <= 1.1*cal) & (df.Protein >= 0.9*protein) & (df.Protein >= 0.9*protein) & (df.Fats >= 0.9*fat) & (df.Fats >= 0.9*fat)]

#Incorporates the above functions to return a list of recipe IDs for individual recipe search
def ind_recipes(x, cals, protein, fat, search_term, vegan, allergies):
    df = cal_filter(cals, protein, fat, search_filter(search_term, vegan_filter(vegan, allergy_filter(allergies))))
    df = df[df.No_of_reviews >= 10]
    df['score'] = (df.Average_rating*np.log10(df.No_of_reviews)) - (x*df.Prep_time/60)
    df.sort_values('score', ascending=False, inplace=True)
    ind_list = list(df['RecipeID'].iloc[0:14])
    filtered_list = random.sample(ind_list, k = 5)
    return filtered_list

#Uses the above functions (not ind_recipes) to return a list of lists
#Each child list corresponds to the meals (so 4 child lists for 4 meals/day)
#Each element in the child list corresponds to the recipe options user can select from (3/5 options per child list - defined by k)
def meal_plan(x, cals, protein, fat, vegan, allergies, meals):
    df = cal_filter(cals, protein, fat, vegan_filter(vegan, allergy_filter(allergies)))
    df = df[df.No_of_reviews >= 10]
    df['score'] = (df.Average_rating*np.log10(df.No_of_reviews)) - (x*df.Prep_time/60)
    df.sort_values('score', ascending=False, inplace=True)
    ind_list = list(df['RecipeID'].iloc[0:5*meals])
    filtered_list = [random.sample(ind_list, k = 3) for i in range(0,meals)]
    return filtered_list


class stacked(QWidget):

   def __init__(self):
      super(stacked, self).__init__()

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
      self.prep = QComboBox()
      self.prep.addItems(["Low", "Medium", "High"])
      self.meals = QLineEdit()
      self.allergies = QLineEdit()
      self.diet = QComboBox()
      self.diet.addItems(["NA", "Vegan"])
      self.pref = QLineEdit()

      self.all_data = {}
      self.all_data['age'] = 30
      self.all_data['gender'] = ""
      self.all_data['height feet'] = 5
      self.all_data['height inches'] = 6
      self.all_data['activity'] = ""
      self.all_data['weight'] = 140
      self.all_data['output'] = ""
      self.all_data['prep'] = "Medium"
      self.all_data['meals'] = 3
      self.all_data['allergies'] = ""
      self.all_data['diet'] = ""
      self.all_data['preferences'] = ""

      self.leftlist = QListWidget ()
      self.leftlist.insertItem (0, 'Form' )
      self.leftlist.insertItem (1, 'Recommendations' )
		
      self.stack1 = QWidget()
      self.stack2 = QWidget()
		
      self.stack1UI()
		
      self.Stack = QStackedWidget (self)
      self.Stack.addWidget(self.stack1)
      self.Stack.addWidget(self.stack2)
		
      hbox = QHBoxLayout(self)
      hbox.addWidget(self.leftlist)
      hbox.addWidget(self.Stack)

      self.setLayout(hbox)
      self.leftlist.currentRowChanged.connect(self.display)
      self.setGeometry(300, 150, 770, 770)
      self.setWindowTitle('Recipe Recommender and Grocery Shopping')
      self.show()

   def getInfo(self):
      self.validateInput()
      self.printRequirements()
      self.stack2UI()

   def validateInput(self):
      if self.age.text().isnumeric():
         self.all_data['age'] = int(self.age.text())

      self.all_data['gender'] = self.gender.text()

      if self.heightF.currentText().isnumeric():
         self.all_data['height feet'] = int(self.heightF.currentText())

      if self.heightI.currentText().isnumeric():
         self.all_data['height inches'] = int(self.heightI.currentText())

      self.all_data['activity'] = self.activity.currentText()

      if self.weight.text().isnumeric():
         self.all_data['weight'] = int(self.weight.text())

      self.all_data['output'] = self.output.currentText()

      self.all_data['prep'] = self.prep.currentText()

      if self.meals.text().isnumeric():
         self.all_data['meals'] = int(self.meals.text())

      self.all_data['allergies'] = self.allergies.text().split(", ")

      self.all_data['diet'] = self.diet.currentText()

      self.all_data['preferences'] = self.pref.text().split(", ")

   def printRequirements(self):
      self.requirements.setText('REQUIREMENTS (Calories/Protein/Fat):')

      self.D.setText('Total Daily:')
      self.PM.setText('Per Meal:')

      self.caloriesD = round(self.getCalories(), 2)
      self.caloriesPM = round(self.caloriesD / self.all_data['meals'], 2)

      self.proteinD = round(self.getProtein(), 2)
      self.proteinPM = round(self.proteinD / self.all_data['meals'], 2)

      self.fatD = round(self.getFat(), 2)
      self.fatPM = round(self.fatD / self.all_data['meals'], 2)

      self.DV.setText(str(self.caloriesD) + '/' + str(self.proteinD) + 'g/' + str(self.fatD) + 'g')
      self.PMV.setText(str(self.caloriesPM) + '/' + str(self.proteinPM) + 'g/' + str(self.fatPM) + 'g')

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
      layout.addRow(QLabel("Age:"), self.age)
      layout.addRow(QLabel("Gender:"), self.gender)
      layout.addRow(QLabel("Height(feet):"), self.heightF)
      layout.addRow(QLabel("Height(inches):"), self.heightI)
      layout.addRow(QLabel("Activity:"), self.activity)
      layout.addRow(QLabel("Weight(lbs):"), self.weight)
      layout.addRow(QLabel("Output:"), self.output)
      layout.addRow(QLabel("Time Spent Cooking?"), self.prep)
      layout.addRow(QLabel("Meals per Day:"), self.meals)
      layout.addRow(QLabel("Food Allergies:"), self.allergies)
      layout.addRow(QLabel("Diet:"), self.diet)
      layout.addRow(QLabel("Preferred Ingredient (required for individual recipe):"), self.pref)
      
      self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
      self.buttonBox.accepted.connect(self.getInfo)
      layout.addWidget(self.buttonBox)

      self.requirements = QtWidgets.QLabel(self)
      self.requirements.move(330, 570)
      self.requirements.resize(505,30)

      self.D = QtWidgets.QLabel(self)
      self.D.move(340, 600)
      self.D.resize(70,30)
      self.PM = QtWidgets.QLabel(self)
      self.PM.move(345, 630)
      self.PM.resize(60,30)

      self.DV = QtWidgets.QLabel(self)
      self.DV.move(415, 600)
      self.DV.resize(160,30)
      self.PMV = QtWidgets.QLabel(self)
      self.PMV.move(410, 630)
      self.PMV.resize(160,30)

      self.stack1.setLayout(layout)
		
   def stack2UI(self):
      layout = QFormLayout()

      if self.all_data['prep'] == "Low":
         x = 1
      elif self.all_data['prep'] == "Medium":
         x = 3
      else:
         x = 5

      if self.all_data['output'] == 'Single recipe':
         self.rec = QtWidgets.QLabel(self)
         self.rec.setText('Recommended Recipes:')
         layout.addWidget(self.rec)

         r = ind_recipes(x, self.caloriesPM, self.proteinPM, self.fatPM, self.all_data['preferences'], self.all_data['diet'], self.all_data['allergies'])

         recipes = QHBoxLayout()
         recipes.addWidget(QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Title'].iloc[0]))
         recipes.addWidget(QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Title'].iloc[0]))
         recipes.addWidget(QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Title'].iloc[0]))
         recipes.addWidget(QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Title'].iloc[0]))
         recipes.addWidget(QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Title'].iloc[0]))
         layout.addRow(recipes)
      else:
         self.rec = QtWidgets.QLabel(self)
         self.rec.setText('Recommended Meal Plans:')
         layout.addWidget(self.rec)

         r = meal_plan(x, self.caloriesPM, self.proteinPM, self.fatPM, self.all_data['diet'], self.all_data['allergies'], self.all_data['meals'])

         print(r)

         plan = QHBoxLayout()
         plan.addWidget(QRadioButton("Meal Plan 1"))
         plan.addWidget(QRadioButton("Meal Plan 2"))
         plan.addWidget(QRadioButton("Meal Plan 3"))
         layout.addRow(plan)
      
      self.stack2.setLayout(layout)
		
   def display(self,i):
      self.Stack.setCurrentIndex(i)
		
def main():
   app = QApplication(sys.argv)
   ex = stacked()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()