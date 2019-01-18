# load the dataset
data = open('data/corpus').read()

# split the dataset into training test and validation datasets
data['label'] = '__label__' + data['label'].astype(str)

data.iloc[0:int(len(data)*0.8)].to_tcsv('train.txt', sep='\t', index = False, header = False)
data.iloc[int(len(data)*0.8):int(len(data)*0.9)].to_csv('test.txt', sep='\t', index = False, header = False)
data.iloc[int(len(data)*0.9):].to_csv('dev.txt', sep='\t', index = False, header = False)

