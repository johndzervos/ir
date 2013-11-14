import pickle

loaded_data = pickle.load(open( "SavedInvertedIndex.p", "rb" ))
for i in loaded_data:
    print i, loaded_data[i].keys(), loaded_data[i].values()


