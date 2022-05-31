import names
import random
import pandas as pd

df = pd.read_excel('./excel_files/friends.xlsx', header=0, index_col=0)

friends_num = df['Name'].shape[0]

for i in range(friends_num):
    name, surname = names.get_full_name().split()
    username = name.lower() + surname[:3].lower() + str(random.randint(1,9))
    df['Name'].at[i+1] = name
    df['Surname'].at[i+1] = surname
    df['Username'].at[i+1] = username

df.to_excel('./excel_files/friends_randomized.xlsx')
