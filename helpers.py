import inspect
from os import listdir
from os.path import isfile, join
import settings


def csv_files():
    return [f for f in listdir(settings.MODEL_DIR) if
            isfile(join(settings.MODEL_DIR, f)) and f.endswith(settings.FILE_EXTENTION)]
def get_class_members(klass):
    ret = dir(klass)
    if hasattr(klass,'__bases__'):
        for base in klass.__bases__:
            ret = ret + get_class_members(base)
    return ret


def uniq( seq ):
    """ the 'set()' way ( use dict when there's no set ) """
    return list(set(seq))


def get_object_attrs( obj ):
    # code borrowed from the rlcompleter module ( see the code for Completer::attr_matches() )
    ret = dir( obj )
    ## if "__builtins__" in ret:
    ##    ret.remove("__builtins__")

    if hasattr( obj, '__class__'):
        ret.append('__class__')
        ret.extend( get_class_members(obj.__class__) )

        ret = uniq( ret )

    return ret

def a(cls):
    variables = [i for i in dir(cls) if not inspect.ismethod(i)]
    return variables

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1