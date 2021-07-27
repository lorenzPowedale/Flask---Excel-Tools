import pandas as pd
import unicodecsv


# reads a CSV file
def read_csv(path):
    with open(path, "rb") as f:
        reader = list(unicodecsv.DictReader(f, delimiter=";"))
        return reader


data1 = pd.DataFrame(read_csv('/Users/lorenz/Downloads/ENECO Te Corrigeren Laadsessies_ODB.csv'))
data2 = pd.DataFrame(read_csv('/Users/lorenz/Downloads/wrong_indexes.csv'))

DATABASE = pd.DataFrame(data1.iloc[:, 7])
EXCLUDE = pd.DataFrame(data2.iloc[:, 0])

DATABASE.columns = ['CP communication unit']
EXCLUDE.columns = ['CP communication unit']

DATABASE = DATABASE.groupby('CP communication unit').first()
EXCLUDE = EXCLUDE.groupby('CP communication unit').first()
# rows in USERS and EXCLUDE with the same email
duplicates = pd.merge(DATABASE, EXCLUDE,left_index=True,right_index=True)

# drop the indices from USERS
DATABASE = DATABASE.drop(duplicates.index)
print(len(EXCLUDE))
print(DATABASE)
print(len(DATABASE))






