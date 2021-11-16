# Datasets ReadMe

This folder contains all the datasets that are used in this application. Most of the files are too large to upload on Github so they should be loaded into this directory on your local machine. The main dataset files are from https://www.kaggle.com/elisaxxygao/foodrecsysv1 and should include:

- core-data_recipe.csv (181.39 MB)
- raw-data_recipe.csv (1.77 GB)
- /raw-data-images (49.7k files)

Using these main datasets, we construct the following datasets below:

- ingredients_raw.csv
  * Contains the raw ingredients list for each recipe.
- recipes.db
  - I would like to eventually aggregate all the csv files into this single database file.
  - Currently contains a table called "isVegan" with the schema {recipe_id: int, isVegan: bool}
