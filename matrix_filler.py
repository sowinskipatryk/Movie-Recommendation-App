import pandas as pd

matrix = pd.read_excel('ratings_matrix.xlsx', header=0, index_col=0)

for i in range(500):
    with open(f'rates_{i+1}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            name, rate = line.replace('\n','').split()
            matrix[name].iat[i] = rate

matrix.to_excel('ratings_matrix.xlsx')