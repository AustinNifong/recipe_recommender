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
        if not os.path.exists("recipe_name_index"):
            os.mkdir("recipe_name_index")

        schema = Schema(
            recipe_name=TEXT,
            recipe_id=NUMERIC(stored=True))

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
    query: 
        a query string
        e.g. "greek salad", "mushroom pizza", "blueberry muffin", etc.
    numResults: 
        the top N number of results to return
        default is 20 results

    @output
    A list of recipe_id's that correspond to the most relevant query results.
    """
    def searchRecipes(self, query: str, numResults: int=20) -> list:
        if not os.path.exists("recipe_name_index"):
            raise RuntimeError("Recipes must be indexed first. Call createIndex at least once before searching for recipes")

        ix = open_dir("recipe_name_index")
        results = []
        with ix.searcher() as searcher:
            parser = QueryParser("recipe_name", ix.schema)
            myquery = parser.parse(query)
            queryResults = searcher.search(myquery, limit=numResults)
            for result in queryResults:
                results.append(result['recipe_id'])
        return results


# Example Usage Below:
def main():
    # create a RecipeSearch object 
    searcher = RecipeSearch()

    ### ----- This function only needs to be run once to store index information on your local computer ----- ###
    # searcher.createIndex(path="../datasets/core-data_recipe.csv")
    ### ----------------------------------------------------------------------------------------------------- ###

    # search for recipes given a query and an optional number of results
    res = searcher.searchRecipes(query="blueberry muffin", numResults=10)
    print(res)

if __name__ == "__main__":
    main()
            



        
            
