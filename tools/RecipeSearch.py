import os.path

import pandas as pd

from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser


class RecipeSearch:
    """
    @function
    createIndex: Creates an index for recipe names for future querying.
    This function only needs to be run once to initialize the indexes in some storage container.

    @params
    path: path to a recipes csv file containing the recipe_name and recipe_id fields

    @output
    None
    """
    def createIndex(self, path: str) -> None:
        schema = Schema(
            recipe_name=TEXT,
            recipe_id=NUMERIC(stored=True))
        
        if not os.path.exists("recipe_name_index"):
            os.mkdir("recipe_name_index")

        ix = create_in("recipe_name_index", schema)
        ix = open_dir("recipe_name_index")

        df = pd.read_csv(path)
        writer = ix.writer()

        for i in range(df.shape[0]):
            writer.add_document(
                recipe_name=df.iloc[i]['recipe_name'],
                recipe_id=df.iloc[i]['recipe_id']
                )
        writer.commit()
            
    """
    @function
    searchRecipes: finds the most relevant recipes titles

    @params
    query: a query string
    numResults: the top N number of results to return

    @output
    A list of indexes that correspond to the N most relevant query results.
    """
    def searchRecipes(self, query: str, numResults: int) -> list:
        if not os.path.exists("recipe_name_index"):
            raise RuntimeError("Recipes must be indexed first. Call createIndex at least once before searching for recipes")

        ix = open_dir("recipe_name_index")
        results = []
        with ix.searcher() as searcher:
            parser = QueryParser("recipe_name", ix.schema)
            myquery = parser.parse(query)
            queryResults = searcher.search(myquery, limit=numResults)
            for result in queryResults.items():
                results.append(result[0])
        return results

"""
def main():
    searcher = RecipeSearch()
    searcher.createIndex(path="datasets/core-data_recipe.csv")
    res = searcher.searchRecipes(query="pot roast", numResults=10)
    for r in res:
        print(r, ",")
    return

if __name__ == "__main__":
    main()
            
"""



        
            
