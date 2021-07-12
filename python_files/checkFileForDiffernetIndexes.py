# pip install openpyxl, pandas, unicodecsv
import pandas as pd
import unicodecsv

output = ['CP communication unit', 'Energy stop (wh)', 'Energy initial (wh)', 'Csid', 'Start timestamp',
          'End timestamp']


# cleanses all 0s, NaNs and Nulls out of the DataFrame
def cleanNull(data):
    print("Before 0kWh cleaning", len(data))
    data = data[data['Energy consumed (wh)'] != '']
    data = data[data['Energy consumed (wh)'].astype('float').notnull()]
    data = data[data['Energy consumed (wh)'].astype('float') != 0]
    print("After 0kWh cleaning", len(data))
    return data


# reads a CSV file
def read_csv(path):
    with open(path, "rb") as f:
        reader = list(unicodecsv.DictReader(f, delimiter=";"))
        return reader


# converts excel .xlsx file into a pandas.Dataframe
# Syntax e.g. 2021-06-01 00:00:00+02:00
def getWrongIndexes(path):
    data = cleanNull(pd.DataFrame(read_csv(path)))
    data['Energy stop (wh)'] = data['Energy stop (wh)'].astype('float')
    data['Energy initial (wh)'] = data['Energy initial (wh)'].astype('float')
    data['Energy consumed (wh)'] = data['Energy consumed (wh)'].astype('float')
    # Grouping every 'CP communication unit' in month
    grouped_df = data.groupby(['CP communication unit'], axis=0, as_index=False)

    data_copy = pd.DataFrame()
    for key, item in grouped_df:
        group = grouped_df.get_group(key) \
            .assign(total=grouped_df.get_group(key)['Energy initial (wh)'].astype(int)) \
            .sort_values(by=['Energy initial (wh)'], axis=0)
        group = group[output]
        group['Energy initial (wh)'] = group['Energy initial (wh)'].shift(-1)
        group = group[group['Energy initial (wh)'].notnull()]
        group = group[group['Energy stop (wh)'] - group['Energy initial (wh)'] != 0]
        data_copy = data_copy.append(group)
    data_copy = data_copy[data_copy['Energy initial (wh)'].notnull()]
    return data_copy
