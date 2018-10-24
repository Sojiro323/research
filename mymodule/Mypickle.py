import pickle
from inspect import currentframe
import os
import sys

def load(path, files):

    if path[-1] != "/":path = path + "/"
    #names = {id(v):k for k,v in currentframe().f_back.f_locals.items()}
    #name = path + names.get(id(file)) + ".pickle"

    if isinstance(files, str):
        name = path + files + ".pickle"
        #print("\nload {0}.pickle".format(files))
        if not os.path.exists(name):
            print('not found directry or file:{0}'.format(name))
            sys.exit()
        with open(name, mode='rb') as f:
            load_file = pickle.load(f)
        return load_file

    return_files = []

    #print("load pickles {0}".format(files))
    for f in files:
        name = path + f + ".pickle"
        if not os.path.exists(name):
            print('not found directry or file:{0}'.format(name))
            sys.exit()
        with open(name, mode='rb') as f:
            load_file = pickle.load(f)
        return_files.append(load_file)

    return return_files

def save_name(path,*files):
    print("\nsave pickle...")

    if path[-1] != "/":path = path + "/"
    names = {id(v):k for k,v in currentframe().f_back.f_locals.items()}

    for f in files:
        name = path + names.get(id(f)) + ".pickle"
        with open(name, mode='wb') as p:
            pickle.dump(f, p)
        print('{0}:{1}'.format(name, len(f)))

def save(path, f, name):
    print("\nsave pickle...")

    if path[-1] != "/":path = path + "/"

    name = path + name + ".pickle"
    with open(name, mode='wb') as p:
        pickle.dump(f, p)
    print('{0}:{1}'.format(name, len(f)))
