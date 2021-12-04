from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import pandas as pd
import numpy as np
import random
import urllib.request
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import os
import json
import webbrowser
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

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

#Exactly the same as allergy_filter. Only this time we return the df elements containing the search_term
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
    filtered_list = [random.sample(ind_list, k = meals) for i in range(0,3)]
    return filtered_list


class HyperlinkLabel(QLabel):
   def __init__(self, parent=None):
      super().__init__()
      self.setStyleSheet('font-size: 35px')
      self.setOpenExternalLinks(True)
      self.setParent(parent)


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
      self.leftlist.insertItem (2, 'Ingredients' )
		
      self.stack1 = QWidget()
      self.stack2 = QWidget()
      self.stack3 = QWidget()
		
      self.stack1UI()
		
      self.Stack = QStackedWidget (self)
      self.Stack.addWidget(self.stack1)
      self.Stack.addWidget(self.stack2)
      self.Stack.addWidget(self.stack3)
		
      hbox = QHBoxLayout(self)
      hbox.addWidget(self.leftlist)
      hbox.addWidget(self.Stack)

      self.setLayout(hbox)
      self.leftlist.currentRowChanged.connect(self.display)
      self.setGeometry(300, 50, 770, 770)
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
      myFont = QtGui.QFont()
      myFont.setBold(True)
      self.requirements.setText('REQUIREMENTS (Calories/Protein/Fat):')
      self.requirements.setFont(myFont)

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

   def refresh(self):
      if self.all_data['output'] == 'Single recipe':
         self.layout2.removeWidget(self.r1)
         self.layout2.removeWidget(self.r2)
         self.layout2.removeWidget(self.r3)
         self.layout2.removeWidget(self.r4)
         self.layout2.removeWidget(self.r5)

         r = ind_recipes(self.x, self.caloriesPM, self.proteinPM, self.fatPM, self.all_data['preferences'], self.all_data['diet'], self.all_data['allergies'])

         self.r1 = QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Title'].iloc[0] + '\n\n' + 
            'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Serving_size'].iloc[0]) + '\n' + 
            'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Prep_time'].iloc[0]) + '\n' + 
            'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Average_rating'].iloc[0], 2)) + '\n' + 
            'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'No_of_reviews'].iloc[0]) + '\n' + 
            'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Calories'].iloc[0]))
         self.r2 = QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Title'].iloc[0] + '\n\n' + 
            'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Serving_size'].iloc[0]) + '\n' + 
            'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Prep_time'].iloc[0]) + '\n' + 
            'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Average_rating'].iloc[0], 2)) + '\n' + 
            'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'No_of_reviews'].iloc[0]) + '\n' + 
            'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Calories'].iloc[0]))
         self.r3 = QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Title'].iloc[0] + '\n\n' + 
            'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Serving_size'].iloc[0]) + '\n' + 
            'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Prep_time'].iloc[0]) + '\n' + 
            'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Average_rating'].iloc[0], 2)) + '\n' + 
            'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'No_of_reviews'].iloc[0]) + '\n' + 
            'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Calories'].iloc[0]))
         self.r4 = QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Title'].iloc[0] + '\n\n' + 
            'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Serving_size'].iloc[0]) + '\n' + 
            'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Prep_time'].iloc[0]) + '\n' + 
            'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Average_rating'].iloc[0], 2)) + '\n' + 
            'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'No_of_reviews'].iloc[0]) + '\n' + 
            'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Calories'].iloc[0]))
         self.r5 = QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Title'].iloc[0] + '\n\n' + 
            'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Serving_size'].iloc[0]) + '\n' + 
            'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Prep_time'].iloc[0]) + '\n' + 
            'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Average_rating'].iloc[0], 2)) + '\n' + 
            'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'No_of_reviews'].iloc[0]) + '\n' + 
            'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Calories'].iloc[0]))

         self.recipes.addWidget(self.r1)
         self.recipes.addWidget(self.r2)
         self.recipes.addWidget(self.r3)
         self.recipes.addWidget(self.r4)
         self.recipes.addWidget(self.r5)
      else:
         self.layout2.removeWidget(self.m1)
         self.layout2.removeWidget(self.m2)
         self.layout2.removeWidget(self.m3)

         m = meal_plan(self.x, self.caloriesPM, self.proteinPM, self.fatPM, self.all_data['diet'], self.all_data['allergies'], self.all_data['meals'])

         text1 = 'MEAL PLAN 1'
         for t in range(self.all_data['meals']):
            text1 += '\n\n' + df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'Title'].iloc[0] + '\n\n' + 'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'Serving_size'].iloc[0]) + '\n' + 'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'Prep_time'].iloc[0]) + '\n' + 'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'Average_rating'].iloc[0], 2)) + '\n' + 'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'No_of_reviews'].iloc[0]) + '\n' + 'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'Calories'].iloc[0])
         self.m1 = QRadioButton(text1)

         text2 = 'MEAL PLAN 2'
         for t in range(self.all_data['meals']):
            text2 += '\n\n' + df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'Title'].iloc[0] + '\n\n' + 'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'Serving_size'].iloc[0]) + '\n' + 'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'Prep_time'].iloc[0]) + '\n' + 'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'Average_rating'].iloc[0], 2)) + '\n' + 'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'No_of_reviews'].iloc[0]) + '\n' + 'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'Calories'].iloc[0])
         self.m2 = QRadioButton(text2)

         text3 = 'MEAL PLAN 3'
         for t in range(self.all_data['meals']):
            text3 += '\n\n' + df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'Title'].iloc[0] + '\n\n' + 'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'Serving_size'].iloc[0]) + '\n' + 'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'Prep_time'].iloc[0]) + '\n' + 'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'Average_rating'].iloc[0], 2)) + '\n' + 'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'No_of_reviews'].iloc[0]) + '\n' + 'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'Calories'].iloc[0])
         self.m3 = QRadioButton(text3)

         self.plan.addWidget(self.m1)
         self.plan.addWidget(self.m2)
         self.plan.addWidget(self.m3)

   def getIngredients(self):
      self.requirements.setText('')
      self.D.setText('')
      self.PM.setText('')
      self.DV.setText('')
      self.PMV.setText('')

      linkTemplate = '<a href={0}>{1}</a>'

      if self.all_data['output'] == 'Single recipe':
         if self.r1.isChecked():
            idd = df_recipes.loc[df_recipes['Title'] == self.r1.text().split('\n')[0], 'RecipeID'].iloc[0]
         elif self.r2.isChecked():
            idd = df_recipes.loc[df_recipes['Title'] == self.r2.text().split('\n')[0], 'RecipeID'].iloc[0]
         elif self.r3.isChecked():
            idd = df_recipes.loc[df_recipes['Title'] == self.r3.text().split('\n')[0], 'RecipeID'].iloc[0]
         elif self.r4.isChecked():
            idd = df_recipes.loc[df_recipes['Title'] == self.r4.text().split('\n')[0], 'RecipeID'].iloc[0]
         elif self.r5.isChecked():
            idd = df_recipes.loc[df_recipes['Title'] == self.r5.text().split('\n')[0], 'RecipeID'].iloc[0]
         idds = [idd]
         ingg = df_rec2ing.loc[df_rec2ing['RecipeID'] == idd, 'IngredientID'].tolist()
         ing = ""
         for i in ingg:
            ing += df_ing.loc[df_ing['IngredientID'] == i, 'IngredientName'].iloc[0]
            ing += '\n'

         self.url = df_recipes.loc[df_recipes['RecipeID'] == idd, 'Image'].iloc[0] 
         self.data = urllib.request.urlopen(self.url).read()
         self.pixmap = QPixmap()
         self.pixmap.loadFromData(self.data)
         self.pixmap = self.pixmap.scaled(250, 200)
         self.im1.setPixmap(self.pixmap)
         self.layout2.addWidget(self.im1)

         self.link1.setText(linkTemplate.format('https://www.allrecipes.com/recipe/' + str(idd), 'Link to Recipe'))
         self.link1.setOpenExternalLinks(True)
         self.layout2.addWidget(self.link1)
      else:
         mm = []
         if self.m1.isChecked():
            for t in range(self.all_data['meals']):
               mm.append(self.m1.text().split('\n')[8*t+2])
         elif self.m2.isChecked():
            for t in range(self.all_data['meals']):
               mm.append(self.m2.text().split('\n')[8*t+2])
         elif self.m3.isChecked():
            for t in range(self.all_data['meals']):
               mm.append(self.m3.text().split('\n')[8*t+2])
         idds = []
         ing = ""

         for t in range(len(mm)):
            idd = df_recipes.loc[df_recipes['Title'] == mm[t], 'RecipeID'].iloc[0]
            idds.append(idd)
            ingg = df_rec2ing.loc[df_rec2ing['RecipeID'] == idd, 'IngredientID'].tolist()

            self.layout2.addWidget(QLabel('https://www.allrecipes.com/recipe/' + str(idd), self))

            for i in ingg:
               if df_ing.loc[df_ing['IngredientID'] == i, 'IngredientName'].iloc[0] not in ing:
                  ing += df_ing.loc[df_ing['IngredientID'] == i, 'IngredientName'].iloc[0]
                  ing += '\n'
      
      self.stack3UI(ing, idds)

   def openAmazon(self):
      global driver
      driver = webdriver.Chrome()
      driver.get("file://" + os.path.realpath("toAmazon.html"))
      driver.implicitly_wait(10)
      driver.find_element_by_name('button').click()
      # driver.find_element(By.NAME, 'button').click()
		
   def stack1UI(self):
      self.layout1 = QFormLayout()
      self.layout1.addRow(QLabel("Age:"), self.age)
      self.layout1.addRow(QLabel("Gender:"), self.gender)
      self.layout1.addRow(QLabel("Height(feet):"), self.heightF)
      self.layout1.addRow(QLabel("Height(inches):"), self.heightI)
      self.layout1.addRow(QLabel("Activity:"), self.activity)
      self.layout1.addRow(QLabel("Weight(lbs):"), self.weight)
      self.layout1.addRow(QLabel("Output:"), self.output)
      self.layout1.addRow(QLabel("Time Spent Cooking?"), self.prep)
      self.layout1.addRow(QLabel("Meals per Day:"), self.meals)
      self.layout1.addRow(QLabel("Food Allergies:"), self.allergies)
      self.layout1.addRow(QLabel("Diet:"), self.diet)
      self.layout1.addRow(QLabel("Preferred Ingredient (required for individual recipe):"), self.pref)
      
      self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
      self.buttonBox.accepted.connect(self.getInfo)
      self.layout1.addWidget(self.buttonBox)

      self.requirements = QtWidgets.QLabel(self)
      self.requirements.move(330, 600)
      self.requirements.resize(505,30)

      self.D = QtWidgets.QLabel(self)
      self.D.move(340, 630)
      self.D.resize(70,30)
      self.PM = QtWidgets.QLabel(self)
      self.PM.move(345, 660)
      self.PM.resize(60,30)

      self.DV = QtWidgets.QLabel(self)
      self.DV.move(415, 630)
      self.DV.resize(160,30)
      self.PMV = QtWidgets.QLabel(self)
      self.PMV.move(410, 660)
      self.PMV.resize(160,30)

      self.stack1.setLayout(self.layout1)
		
   def stack2UI(self):
      self.layout2 = QFormLayout()

      if self.all_data['prep'] == "Low":
         self.x = 1
      elif self.all_data['prep'] == "Medium":
         self.x = 3
      else:
         self.x = 5

      myFont = QtGui.QFont()
      myFont.setBold(True)

      if self.all_data['output'] == 'Single recipe':
         self.rec = QtWidgets.QLabel(self)
         self.rec.setText('Recommended Recipes:')
         self.rec.setFont(myFont)
         self.layout2.addWidget(self.rec)

         self.recipes = QHBoxLayout()

         r = ind_recipes(self.x, self.caloriesPM, self.proteinPM, self.fatPM, self.all_data['preferences'], self.all_data['diet'], self.all_data['allergies'])

         self.r1 = QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Title'].iloc[0] + '\n\n' + 
            'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Serving_size'].iloc[0]) + '\n' + 
            'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Prep_time'].iloc[0]) + '\n' + 
            'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Average_rating'].iloc[0], 2)) + '\n' + 
            'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'No_of_reviews'].iloc[0]) + '\n' + 
            'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[0], 'Calories'].iloc[0]))
         self.r2 = QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Title'].iloc[0] + '\n\n' + 
            'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Serving_size'].iloc[0]) + '\n' + 
            'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Prep_time'].iloc[0]) + '\n' + 
            'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Average_rating'].iloc[0], 2)) + '\n' + 
            'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'No_of_reviews'].iloc[0]) + '\n' + 
            'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[1], 'Calories'].iloc[0]))
         self.r3 = QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Title'].iloc[0] + '\n\n' + 
            'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Serving_size'].iloc[0]) + '\n' + 
            'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Prep_time'].iloc[0]) + '\n' + 
            'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Average_rating'].iloc[0], 2)) + '\n' + 
            'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'No_of_reviews'].iloc[0]) + '\n' + 
            'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[2], 'Calories'].iloc[0]))
         self.r4 = QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Title'].iloc[0] + '\n\n' + 
            'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Serving_size'].iloc[0]) + '\n' + 
            'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Prep_time'].iloc[0]) + '\n' + 
            'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Average_rating'].iloc[0], 2)) + '\n' + 
            'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'No_of_reviews'].iloc[0]) + '\n' + 
            'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[3], 'Calories'].iloc[0]))
         self.r5 = QRadioButton(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Title'].iloc[0] + '\n\n' + 
            'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Serving_size'].iloc[0]) + '\n' + 
            'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Prep_time'].iloc[0]) + '\n' + 
            'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Average_rating'].iloc[0], 2)) + '\n' + 
            'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'No_of_reviews'].iloc[0]) + '\n' + 
            'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == r[4], 'Calories'].iloc[0]))

         self.recipes.addWidget(self.r1)
         self.recipes.addWidget(self.r2)
         self.recipes.addWidget(self.r3)
         self.recipes.addWidget(self.r4)
         self.recipes.addWidget(self.r5)

         self.layout2.addRow(self.recipes)
      else:
         self.rec = QtWidgets.QLabel(self)
         self.rec.setText('Recommended Meal Plans:')
         self.rec.setFont(myFont)
         self.layout2.addWidget(self.rec)

         m = meal_plan(self.x, self.caloriesPM, self.proteinPM, self.fatPM, self.all_data['diet'], self.all_data['allergies'], self.all_data['meals'])

         text1 = 'MEAL PLAN 1'
         for t in range(self.all_data['meals']):
            text1 += '\n\n' + df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'Title'].iloc[0] + '\n\n' + 'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'Serving_size'].iloc[0]) + '\n' + 'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'Prep_time'].iloc[0]) + '\n' + 'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'Average_rating'].iloc[0], 2)) + '\n' + 'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'No_of_reviews'].iloc[0]) + '\n' + 'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[0][t], 'Calories'].iloc[0])
         self.m1 = QRadioButton(text1)

         text2 = 'MEAL PLAN 2'
         for t in range(self.all_data['meals']):
            text2 += '\n\n' + df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'Title'].iloc[0] + '\n\n' + 'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'Serving_size'].iloc[0]) + '\n' + 'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'Prep_time'].iloc[0]) + '\n' + 'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'Average_rating'].iloc[0], 2)) + '\n' + 'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'No_of_reviews'].iloc[0]) + '\n' + 'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[1][t], 'Calories'].iloc[0])
         self.m2 = QRadioButton(text2)

         text3 = 'MEAL PLAN 3'
         for t in range(self.all_data['meals']):
            text3 += '\n\n' + df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'Title'].iloc[0] + '\n\n' + 'Serving Size: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'Serving_size'].iloc[0]) + '\n' + 'Prep Time: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'Prep_time'].iloc[0]) + '\n' + 'Average Rating: ' + str(round(df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'Average_rating'].iloc[0], 2)) + '\n' + 'Reviews: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'No_of_reviews'].iloc[0]) + '\n' + 'Calories: ' + str(df_recipes.loc[df_recipes['RecipeID'] == m[2][t], 'Calories'].iloc[0])
         self.m3 = QRadioButton(text3)

         self.plan = QHBoxLayout()

         self.plan.addWidget(self.m1)
         self.plan.addWidget(self.m2)
         self.plan.addWidget(self.m3)

         self.layout2.addRow(self.plan)

      self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
      self.buttonBox.accepted.connect(self.getIngredients)
      self.layout2.addWidget(self.buttonBox)

      button = QPushButton('Refresh', self)
      self.layout2.addWidget(button)
      button.clicked.connect(self.refresh)

      self.im1 = QtWidgets.QLabel(self)
      self.link1 = QtWidgets.QLabel(self)
      
      self.stack2.setLayout(self.layout2)

   def stack3UI(self, ing, idds):
      self.layout3 = QFormLayout()

      if self.all_data['prep'] == "Low":
         self.x = 1
      elif self.all_data['prep'] == "Medium":
         self.x = 3
      else:
         self.x = 5

      linkTemplate = '<a href={0}>{1}</a>'

      myFont = QtGui.QFont()
      myFont.setBold(True)
      
      self.rec = QtWidgets.QLabel(self)
      self.rec.setText('Ingredients:')
      self.rec.setFont(myFont)
      self.layout3.addWidget(self.rec)

      self.ingr = QtWidgets.QLabel(self)
      self.ingr.setText(ing)
      self.layout3.addWidget(self.ingr)

      ingList = []
      unitList = []
      amountList = []

      ingId = []
      for rID in idds:
          newDF = df_rec2ing.loc[df_rec2ing['RecipeID'] == rID]
          ingId += newDF['IngredientID'].tolist()
          amountList += newDF['Quantity'].tolist()
          unitList += newDF['Unit'].tolist()

      for i,iD in enumerate(ingId):
          index = df_ing[df_ing['IngredientID'] == iD].index[0]
          ingList.append(df_ing.iloc[index]['IngredientName'])

      #adjust units for Amazon
      for i in range(len(unitList)):
          if unitList[i] in ["cup", "clove", "pound", "ounce", "clove", "stalk", "quart", "slice", "pint","gallon", "drop"]:
              unitList[i] = unitList[i].upper() + "S"
          if unitList[i] == "tablespoon":
              unitList[i] = "TBSP"
          if unitList[i] == "teaspoon":
              unitList[i] = "TSP"
          if unitList[i] == "leaf":
              unitList[i] = "LEAVES"
          if unitList[i] == "pinch":
              unitList[i] = "PINCHES"
          if unitList[i] == "dash":
              unitList[i] = "DE_DASH"

      example = {"ingredients": []}

      for ing, un, amt in zip(ingList, unitList,  amountList):
         newD = {"name": ing, 
                     "quantityList":[{"unit": un, "amount": amt}],
                      "exclusiveOverride": "false"}
         example['ingredients'].append(newD)

      myJSON = json.dumps(example)
      f = open('toAmazon.html','w')

      html_content = """<html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width">
          <title>replit</title>
          <link href="style.css" rel="stylesheet" type="text/css" />
        </head>
        <body>
            <form method="POST" action="https://www.amazon.com/afx/ingredients/landing">
           <input type="hidden" name="ingredients" value='""" + myJSON + """'>
           <input type="submit" value="Buy on Amazon" name = "button">
         </form>

          <script src="script.js"></script>
        </body>
      </html>"""

      f.write(html_content)
      f.close()

      button = QPushButton('Buy on Amazon', self)
      self.layout3.addWidget(button)
      button.clicked.connect(self.openAmazon)

      self.stack3.setLayout(self.layout3)
		
   def display(self,i):
      self.Stack.setCurrentIndex(i)
		
def main():
   app = QApplication(sys.argv)
   ex = stacked()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()