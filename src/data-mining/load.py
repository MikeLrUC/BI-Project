import os
import datetime
import numpy as np
import pandas as pd
from coords import Database, DATAPATH

def binning(df, column, n=30):
    counts = df[column].value_counts(dropna=False)
    for i, value in enumerate(df[[column]].values):
        if not (counts[value[0]] >= 30) or value[0] is np.nan:
            df.at[i, column] = "other" 

def get_age(entry):
    current_year = datetime.date.today().year
    words = entry.split(" ")
    for word in words:
        try:
            value = int(word)
            if 1700 <= value <= current_year:
                return current_year - value
        except ValueError:
            pass
    return 0

def bound(entry):
    return max(min(entry, 100), 0)


def main():
    query = '''
    SELECT  facts_rating.id, facts_rating.rating,
            category.name as "category", 
            region.name as "region", 
            wine.name as "wine_name", wine.designation, wine.varietal, wine.alcohol, wine.price,
            winery.name as "winery",
            reviewer.reviewer
    FROM facts_rating 
    JOIN category ON facts_rating.category_id = category.id 
    JOIN region ON facts_rating.region_id = region.id
    JOIN wine ON facts_rating.wine_id = wine.id
    JOIN winery ON facts_rating.winery_id = winery.id
    JOIN reviewer ON facts_rating.reviewer_id = reviewer.id
    ORDER BY id;
    '''

    # Load Database data
    db = Database()
    df = db.execute(query)

    # Get columns by datatype dict
    columns_by_datatypes = df.columns.to_series().groupby(df.dtypes).groups
    data_dict = eval(str(columns_by_datatypes).replace("{", "{'").replace("], ","], '").replace(": [", "': ["))
    
    # Convert blanks to NaN
    for column in data_dict["object"]:
        df[column] = df[column].apply(lambda entry: np.nan if entry == "" else entry)

    # Apply Data Transformations mentioned in the notebook
    binning_cols = ["designation", "varietal", "winery", "reviewer"]
    ohe_cols = ["category"] + binning_cols

    # Get coordinates from region
    coords_df = pd.read_csv(DATAPATH + "coords.csv")
    df = pd.merge(df, coords_df, on="region")
    df[["lat", "lng"]] = df[["lat", "lng"]].fillna(-200)

    # Get wine age
    df["age"] = df["wine_name"].apply(get_age)

    # Bound alcohol values
    df["alcohol"] = df["alcohol"].apply(bound)

    # Binning
    for bc in binning_cols:
        binning(df, bc)

    # One-Hot Encoding
    df = pd.get_dummies(df, columns=ohe_cols)

    # Dropping vars
    df = df.drop(["id", "region", "wine_name"], axis=1)
    return df

if __name__ == "__main__":
    print(main())