# pip install openpyxl, pandas, unicodecsv
import pandas as pd
import unicodecsv

output = ['CP communication unit', 'End timestamp', 'Start timestamp', 'Csid']


# cleanses all 0s, NaNs and Nulls out of the DataFrame
def cleanZeroSecondCharges(data):
    print("Before 0sec cleaning", len(data))
    data = data[data['Duration (mins)'] != '']
    data = data[data['Duration (mins)'].astype('float').notnull()]
    data = data[data['Duration (mins)'].astype('float') != 0]
    print("After 0sec cleaning", len(data))
    return data


# reads a CSV file
def read_csv(path):
    with open(path, "rb") as f:
        reader = list(unicodecsv.DictReader(f, delimiter=";"))
        return reader

def getTimeOverlaps(path):
    # Syntax e.g. 2021-06-01 00:00:00+02:00
    # converts excel .xlsx file into a pandas.Dataframe
    data = cleanZeroSecondCharges(pd.DataFrame(read_csv(path)))
    data['Start timestamp'] = pd.to_datetime(data['Start timestamp'])
    data['Energy initial (wh)'] = data['Energy initial (wh)'].astype('float')
    # Grouping every 'CP communication unit' in month
    grouped_df = data.groupby(['CP communication unit'], axis=0, as_index=False)

    data_copy = pd.DataFrame()
    for key, item in grouped_df:
        group = grouped_df.get_group(key) \
            .assign(total=grouped_df.get_group(key)['Energy initial (wh)']) \
            .sort_values(by=['Energy initial (wh)'], axis=0)
        group = group[output]
        group['Start timestamp'] = group['Start timestamp'].shift(-1)
        group = group[group['Start timestamp'].notnull()]
        group = group[group['End timestamp'].astype('str') >= group['Start timestamp'].astype('str')]
        data_copy = data_copy.append(group)
    data_copy = data_copy[data_copy['End timestamp'].notnull()]
    data_copy['Start timestamp'] = data_copy['Start timestamp'].astype('str')
    data_copy['End timestamp'] = data_copy['End timestamp'].astype('str')
    data_copy.to_excel(path[:path.rindex("/") + 1] + "overlapes.xlsx", index=False)
    print("Finished")
