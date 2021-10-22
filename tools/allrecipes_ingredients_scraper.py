import requests
import pandas as pd
import time


raw = pd.read_csv("datasets/id_ingredients.csv")
start, stop = 40000, len(raw)
#print(raw.head())


start_time = time.time()
ingredient_delimiter = "<span class=\"ingredients-item-name\">"
data = []
for i in range(start, stop): #raw.shape[0]:
    if (i % 100 == 0):
        print(i)
        elaspedTime = time.time() - start_time
        print("%.2f" % elaspedTime)
        print()
    
    recipe_id = raw.recipe_id[i]
    #ingredients = raw.ingredients[i] #raw.ingredients.loc[raw.recipe_id == 25930].iloc[0]
    url = "https://www.allrecipes.com/recipe/" + str(recipe_id)
    #ingredients = []
    try:
        r = requests.get(url)
        ingredients = r.text.split(ingredient_delimiter)[1:]
        ingredients = [i.split('</span>')[0].lower().strip() for i in ingredients]
        data.append([recipe_id, ingredients])

        """
        #quantity_delimiter = [i.split()[0].lower() for i in ingredients.split("^")]
        
        j = 0
        for i in range(len(out)):
            stopIndex = out[i].index('</span>')
            ingredient = out[i][:stopIndex].lower()

            stopIndex = ingredient.find(quantity_delimiter[j])
            while stopIndex == -1:
                j += 1
                stopIndex = ingredient.find(quantity_delimiter[j])

            amnt = ingredient[:stopIndex]
            #amnt = amnt.replace("\u2009", "").replace("Â", "")
            amnt = amnt.split('<')[0].strip()

            amounts.append(amnt)
            j += 1
        data.append([recipe_id, amounts])
        """
    except:
        data.append([recipe_id, None])
        
elaspedTime = time.time() - start_time
print("%.2f" % elaspedTime)

df = pd.DataFrame(data, columns = ["recipe_id", "ingredient_amounts"])
#df.to_csv("out/ingredient_amounts_{start}_{stop}.csv".format(start = start, stop = stop), index = False)
