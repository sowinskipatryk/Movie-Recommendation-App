import pandas as pd

df = pd.read_excel('./excel files/ratings_matrix.xlsx', index_col="Movie Id",
                   header=0)

for column in df:
    if not (df[column].isnull().values == False).sum():
        del df[column]
df.to_excel('./excel files/rating_matrix_no_nulls.xlsx')
