# pip install openpyxl, pandas, unicodecsv
import pandas as pd
import unicodecsv


# cleanses all 0s, NaNs and Nulls out of the DataFrame
def cleanNull(data):
    print("Before 0kWh cleaning", len(data))
    data = data[data['Energy consumed (wh)'] != '']
    data = data[data['Energy consumed (wh)'].astype('float').notnull()]
    data = data[data['Energy consumed (wh)'].astype('float') != 0]
    print("After 0kWh cleaning", len(data))
    return data



# converts excel .xlsx file into a pandas.Dataframe
# Syntax e.g. 2021-06-01 00:00:00+02:00
def getWrongIndexes(df):
    data = cleanNull(df)
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

        group['Energy initial (wh)'] = group['Energy initial (wh)'].shift(-1)
        group = group[group['Energy initial (wh)'].notnull()]
        group = group[group['Energy stop (wh)'] - group['Energy initial (wh)'] != 0]
        data_copy = data_copy.append(group)
    data_copy = data_copy[data_copy['Energy initial (wh)'].notnull()]
    data_copy['Reason'] = 'gap'
    return data_copy