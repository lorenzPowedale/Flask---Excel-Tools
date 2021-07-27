# pip install openpyxl pandas unicodecsv
import pandas as pd
import unicodecsv


# cleanses all 0s, NaNs and Nulls out of the DataFrame
def cleanNull(data):
    print("Before 0kWh cleaning", len(data))
    data = data[data['Energy consumed (wh)'] != '']
    data = data[data['Energy consumed (wh)'].astype('float').notnull()]
    # data = data[data['Energy consumed (wh)'].astype('float') != 0]
    print("After 0kWh cleaning", len(data))
    return data


def getTimeOverlaps(df):
    # Syntax e.g. 2021-06-01 00:00:00+02:00
    # converts excel .xlsx file into a pandas.Dataframe
    data = cleanNull(df)
    data['Start timestamp'] = pd.to_datetime(data['Start timestamp'])
    data['Energy initial (wh)'] = data['Energy initial (wh)'].astype('float')
    # Grouping every 'CP communication unit' in month
    grouped_df = data.groupby(['CP communication unit'], axis=0, as_index=False)

    data_copy = pd.DataFrame()
    for key, item in grouped_df:
        group = grouped_df.get_group(key) \
            .assign(total=grouped_df.get_group(key)['Energy initial (wh)']) \
            .sort_values(by=['Energy initial (wh)'], axis=0)
        group['Start timestamp'] = group['Start timestamp'].shift(-1)
        group = group[group['Start timestamp'].notnull()]
        group = group[group['End timestamp'].astype('str') >= group['Start timestamp'].astype('str')]
        data_copy = data_copy.append(group)
    data_copy = data_copy[data_copy['End timestamp'].notnull()]
    data_copy['Start timestamp'] = data_copy['Start timestamp'].astype('str')
    data_copy['End timestamp'] = data_copy['End timestamp'].astype('str')
    data_copy['Reason'] = 'overlap'
    print("Finished")
    return data_copy
