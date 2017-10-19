from uuid import uuid4
from collections import defaultdict

import pickle
import face_recognition

def check_file(fname):
    try:
        f = open(fname, 'rb')
    except IOError:
        f = open(fname, 'wb')
        pickle.dump({}, f)
    finally:
        f.close()

def load(fname):
    obj = {}
    with open(fname, 'rb') as f:
        obj = pickle.load(f)
    return obj

def dump(fname, obj):
    with open(fname, 'wb') as f:
        pickle.dump(dict(obj), f)

def load_id_to_name():
    fname = 'id_to_name.pickle'
    check_file(fname)
    return defaultdict(lambda : 'Unknown', load(fname))


def dump_id_to_name(dic):
    dump('id_to_name.pickle', dic)

def load_encodings():
    fname = 'encodings.pickle'
    check_file(fname)
    return defaultdict(lambda : 'Unknown', load(fname))

def dump_encodings(dic):
    dump('encodings.pickle', dic)

def create_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    return face_recognition.face_encodings(image)[0]

def add_photo(name, image_path):
    enc = create_encoding(image_path)

    id_to_name = load_id_to_name()
    encs = load_encodings()

    uid = uuid4().hex

    encs[uid] = enc
    dump_encodings(encs)

    id_to_name[uid] = name
    dump_id_to_name(id_to_name)

def remove_person(person_name):
    id_to_name = load_id_to_name()
    encs = load_encodings()

    for uid, name in id_to_name.items():
        if name == person_name:
            del encs[uid]
            del id_to_name[uid]

    dump_id_to_name(id_to_name)
    dump_encodings(encs)
