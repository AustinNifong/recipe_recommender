from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


test = "Hello world"

#if using Safari, enable remote automation (under develop on the toolbar)
driver = webdriver.Firefox()
driver.get('https://www.amazon.com/afx/ingredients/verify')

#Attempting to offer dropdown menu selection

# select = Select(driver.find_element(By.ID,'afx-ingredients-verify-brand-input'))
# WebDriverWait(driver, 1).until(EC.invisibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[1]")))
# driver.find_element(By.ID,'afx-ingredients-verify-brand-input').click()
# select.select_by_visible_text("Whole Foods")

#Section below worked for me
#Clear the values in the text box
driver.find_element(By.ID,'afx-ingredients-verifier-json-input').clear()

#Input values using the variable test - right now it uses the test string variable, so it'll stop working after verify as no url would be created
driver.find_element(By.ID,'afx-ingredients-verifier-json-input').send_keys(test)

#Click on the verify button
driver.find_element(By.CLASS_NAME,'a-button-input').click()

#Wait a second for the URl link to show up
WebDriverWait(driver, 1).until(EC.invisibility_of_element_located((By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/form/span/span/input')))

#Click the buy button
driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/form/span/span/input').click()

#href_url = driver.find_element(By.ID,'afx-ingredients-encoded').get_attribute('href')

