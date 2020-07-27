import pickle
with open("/home/danyanyam/flask/Библиотека/data/pickles/portfel.pickle", "rb") as fobj:
    data = pickle.load(fobj)
print(data)