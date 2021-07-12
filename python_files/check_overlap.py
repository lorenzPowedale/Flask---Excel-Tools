from python_files import checkFileForOverlaps as ov, checkFileForDiffernetIndexes as ix

def getOverlaps(path):
    data_time = ov.getTimeOverlaps(path)
    data_index = ix.getWrongIndexes(path)
    data_copy = data_index.append(data_time)
    data_copy.to_excel(path[:path.rindex("/") + 1] + "wrong_Indexes.xlsx", index=False)