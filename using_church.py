# helpers for encoding between python values and church-encoded values

from church import *

num_void_id = 1
num_bool_id = 2
num_pos_int_id = 3
num_neg_int_id = 4
num_list_id = 5
num_pair_id = 6
num_resultpair_id = 7
num_char_id = 8
num_string_id = 9
num_error_id = 10


neg_zero = object()


def bare_numerify(n):
    return n(lambda x: x+1)(0)

def bare_boolify(b):
    return b(lambda _: True)(lambda _: False)

def bare_listify(lst):
    return lst(lambda _: [])(lambda h: lambda t: [h] + bare_listify(t))

def bare_unpairify(pair):
    return pair(lambda head: lambda tail: (head, tail))


class Char(object):
    def __init__(self, c):
        self.c = c

    def __repr__(self):
        return '<Char %r>' % self.c


def churchandtypify(obj, listrecurs):
    if isinstance(obj, (list, tuple)):
        if len(obj) == 0:
            return num_list_id, BARE_NIL
        return num_list_id, listrecurs(obj[0], obj[1:])
    if isinstance(obj, bool):
        if obj:
            return num_bool_id, BARE_TRUE
        return num_bool_id, BARE_FALSE
    if isinstance(obj, int):
        if obj < 0:
            typnum = num_neg_int_id
            obj = -obj
        else:
            typnum = num_pos_int_id
        i = BARE_ZERO
        for x in range(obj):
            i = BARE_SUCC(i)
        return typnum, i
    # zeroes can end up typed as neg_int or pos_int. this lets us make sure
    # calculations work both ways
    if obj is neg_zero:
        return num_neg_int_id, BARE_ZERO
    if isinstance(obj, str):
        if len(obj) == 0:
            return num_string_id, BARE_NIL
        return num_string_id, BARE_PREPEND(bare_churchify(Char(obj[0])))(bare_churchify(obj[1:]))
    if isinstance(obj, Char):
        i = BARE_ZERO
        for x in range(ord(obj.c)):
            i = BARE_SUCC(i)
        return num_char_id, i
    if obj is None:
        return num_void_id, VOID
    raise NotImplemented

def bare_churchify_recurs(first, rest):
    return BARE_PREPEND(bare_churchify(first))(bare_churchify(rest))

def churchify_recurs(first, rest):
    return BARE_VALUEOF(PREPEND(churchify(first))(churchify(rest)))

def bare_churchify(obj):
    return churchandtypify(obj, bare_churchify_recurs)[1]

def churchify(obj):
    typnum, churchval = churchandtypify(obj, churchify_recurs)
    return BARE_MAKE_TYPEDVAR_MAKER(bare_churchify(typnum))(churchval)

def extract_type_and_val(tval):
    return bare_numerify(BARE_TYPEOF(tval)), BARE_VALUEOF(tval)

class ChurchError(Exception):
    pass

class ChurchTypeError(ChurchError):
    pass

class ChurchIndexError(ChurchError):
    pass

errors = {
    1: ChurchTypeError,
    2: ChurchIndexError,
}

def dechurchify(tval):
    t, val = extract_type_and_val(tval)
    if t == num_void_id:
        return None
    elif t == num_bool_id:
        return bare_boolify(val)
    if t == num_pos_int_id:
        return bare_numerify(val)
    elif t == num_neg_int_id:
        return -bare_numerify(val)
    elif t == num_list_id:
        return map(dechurchify, bare_listify(val))
    elif t == num_pair_id:
        return map(dechurchify, bare_unpairify(val))
    elif t == num_resultpair_id:
        resultval, errnum = bare_unpairify(val)
        errnum = bare_numerify(errnum)
        if errnum:
            return errors[errnum]
        return dechurchify(resultval)
    elif t == num_char_id:
        return chr(bare_numerify(val))
    elif t == num_string_id:
        return ''.join([chr(bare_numerify(c)) for c in bare_listify(val)])
    elif t == num_error_id:
        return errors[bare_numerify(val)]
