def toElasticSearchDate(path):
    with open(path, 'r') as file:
            data = file.read().replace('+01', '')
            data = data.replace('+02', '')
            data = data.replace(',', '.')
            file.close()
    with open(path, 'w') as file:
        file.write(data)
        file.close()