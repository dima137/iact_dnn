# input/output of dictionaries etc.


import zlib
import gzip
import json
import yaml
import copy
import numpy as np
import numbers
import os

#import time


float_vec = np.frompyfunc(float, 1, 1)
int_vec = np.frompyfunc(int, 1, 1)
cplx_vec = np.frompyfunc(complex, 1, 1)
def str_vec(sts):
    return [str(st) for st in sts]


def get_hash(x):
    if type(x) == dict:
        string = yaml.dump(x, default_flow_style=True)
    else:
        string = str(x)
    return zlib.adler32(string) & 0xffffffff

def sub_dict(indict, key_list):
    return {key: indict.get(key) for key in key_list}

def np2py(x):
    if isinstance(x, np.ndarray):
        dtype = x.dtype
    elif isinstance(x, numbers.Number):
        dtype = type(x)
    else:
        return x

    if np.issubdtype(dtype, np.signedinteger):
        return int_vec(x)
    elif np.issubdtype(dtype, float):
        return float_vec(x)
    elif np.issubdtype(dtype, complex):
        return cplx_vec(x)
    elif np.issubdtype(dtype, str):
        return str_vec(x)
    else:
        print('problem in type conversion in np2py')
        print(dtype)
        return None
 
def array2lists(x):
    """
    Convert an array x to list of lists.
    if x is a number, return a number
    if x is an array, return a list of list of lists ...
        for quicker run, make the last dimension the longest
    otherwise return x itself
    """
    if not isinstance(x, np.ndarray):
        return x

    dims = x.shape
    if len(dims) == 1:
        return list(x)
    else:
        res = []
        for i in range(dims[0]):
            res.append(array2lists(x[i]))
        return res


def bin_dict2dict(dct):
    res = copy.deepcopy(dct)
    for key in res.keys():
        if isinstance(res[key], dict):
            res[key] = bin_dict2dict(res[key])
        else:
            res[key] = array2lists(np2py(res[key]))
    return res

def u_dict2dict(dct):
    """
    Transform a dictionary of unicode characters into python strings
    possibly obsolete in python3
    
    """
    return dct


def loaddict(fn, silent=0):
    if os.path.isfile(fn):
        if fn.endswith('gz'):
            f = gzip.open(fn, 'r')
            content = f.read()
            f.close()
        else:
            f = open(fn)
            content = f.read()
            f.close()
    else:
        if not silent:
            print('Dictionary with filename %s not found' % fn)
            print('Creating an empty dictionary')
        return {}

    if fn.find('json') != -1:
        return u_dict2dict(json.loads(content))
    elif fn.find('yaml') != -1:
        return yaml.load(content, Loader=yaml.FullLoader)
    elif fn.find('fit') != -1:
        #hdu = pyfits.open(fn)
        #return hdu2dict(hdu)
        # not yet implemented
        return None

def savedict(dct, fn, expand=False, silent=False):
    if fn.find('json') != -1:
        savejson(dct, fn=fn, silent=silent)
    elif fn.find('yaml') != -1:
        saveyaml(dct, fn=fn, expand=expand, silent=silent)
    elif fn.find('fit') != -1:
        print('cannot save fits yet')
    # chmod: user - rw, group - rw, other - r
    os.chmod(fn, 0o664)
    return None

def savejson(dct, fn=None, silent=False):
    #t0 = time.clock()
    #print 'python data reformatting:'
    dct = bin_dict2dict(dct)
    #print time.clock() - t0
    
    if fn is None:
        return json.dumps(dct)
    elif fn.find('gz') == -1:
        #t0 = time.clock()
        #print 'write uncompressed data:'

        f = open(fn, 'wb')
        json.dump(dct, f)
        f.close()
        #print time.clock() - t0
    else:
        #t0 = time.clock()
        #print 'write compressed data:'
        #content = json.dumps(dct)
        f = gzip.open(fn, 'wb')
        f.write(json.dumps(dct))
        f.close()
        #print time.clock() - t0
    if not silent:
        print('save dict to file:')
        print(fn)
    return None


def saveyaml(dct, fn=None, expand=False, silent=False):
    dct_new = bin_dict2dict(dct)
    dct_new = u_dict2dict(dct_new)
    if fn is None:
        f = None
    else:
        if not silent:
            print('save dict to file:')
            print(fn)
        f = open(fn, 'w')
    yaml.dump(dct_new, f, default_flow_style=(not expand), allow_unicode=True)
    return None





