from pprint import pprint
import pickle
with open("/home/danyanyam/flask/Библиотека/data/pickles/portfel.pickle", "rb") as fobj:
    data = pickle.load(fobj)
pprint(data)