from python_files import checkFileForOverlaps as ov\
    , checkFileForDiffernetIndexes as ix\
    , zerokWh_charges as zero
import unicodecsv
import pandas as pd


# reads a CSV file
def read_csv(path):
    with open(path, "rb") as f:
        reader = list(unicodecsv.DictReader(f, delimiter=";"))
        return reader


def getOverlaps(path):
    data = pd.DataFrame(read_csv(path))

    data_time = ov.getTimeOverlaps(data)
    data_index = ix.getWrongIndexes(data)
    data_zero = zero.returnZerokWhCharges(data)
    data_copy = data_index.append(data_time)
    data_copy = data_copy.append(data_zero)

    data['Reason'] = ''
    data = data[~data['Csid'].isin(data_copy['Csid'])]
    data_copy = data_copy.append(data)

    data_copy.to_excel(path[:path.rindex("/") + 1] + "wrong_Indexes.xlsx", index=False)
    print('Done')
