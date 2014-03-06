# lambda calculus in python
#
# this does make one concession beyond the strictest formulation of the lambda
# calculus: use of the assignment operator (=) at the top level. it should be
# understood as a shorthand for expressing this whole thing as a single lambda
# expression which takes all of the variable names as arguments, all parts of
# which are then applied (starting at the innermost) with the corresponding
# expressions as arguments.
#
# for example, if this module was
#
# VOID = lambda x: x
# TRUE = lambda ontrue: lambda onfalse: ontrue(VOID)
# FALSE = lambda ontrue: lambda onfalse: onfalse(VOID)
# NOT = lambda b: lambda ontrue: lambda onfalse: b(onfalse)(ontrue)
# WHATEVER = NOT(TRUE)(VOID)(lambda x: x(x))
# WHATEVER(TRUE)
#
# then the transformation would be
#
# ((lambda VOID:
#      (lambda TRUE:
#          (lambda FALSE:
#              (lambda NOT:
#                  (lambda WHATEVER:
#                      WHATEVER(TRUE))
#                   (NOT(TRUE)(VOID)(lambda x: x(x))))
#               (lambda b: lambda ontrue: lambda onfalse: b(onfalse)(ontrue)))
#           (lambda ontrue: lambda onfalse: onfalse(VOID)))
#       (lambda ontrue: lambda onfalse: ontrue(VOID)))
#   (lambda x: x))
#
# Obviously, references to toplevel variables which are defined later in the
# module are not allowed.

# bare void is the identity function
BARE_VOID = lambda x: x

# bare booleans: functions which take (ontrue, onfalse) and invoke the
# appropriate one
BARE_TRUE = lambda ontrue: lambda onfalse: ontrue(BARE_VOID)
BARE_FALSE = lambda ontrue: lambda onfalse: onfalse(BARE_VOID)

BARE_IF = lambda test: lambda ontrue: lambda onfalse: test(ontrue)(onfalse)

# numbers: functions which take a function f and a zero element z,
# and iterate calls of z = f(z), n times
BARE_ZERO = lambda f: lambda z: z

BARE_SUCC = lambda n: lambda f: lambda z: f(n(f)(z))

BARE_ONE   = BARE_SUCC(BARE_ZERO)
BARE_TWO   = BARE_SUCC(BARE_ONE)
BARE_THREE = BARE_SUCC(BARE_TWO)
BARE_FOUR  = BARE_SUCC(BARE_THREE)
BARE_FIVE  = BARE_SUCC(BARE_FOUR)
BARE_SIX   = BARE_SUCC(BARE_FIVE)
BARE_SEVEN = BARE_SUCC(BARE_SIX)
BARE_EIGHT = BARE_SUCC(BARE_SEVEN)
BARE_NINE  = BARE_SUCC(BARE_EIGHT)
BARE_TEN   = BARE_SUCC(BARE_NINE)

NO_ERROR_id = BARE_ZERO
TYPE_ERROR_id = BARE_ONE
INDEX_ERROR_id = BARE_TWO

BARE_ADD = lambda n: lambda m: lambda f: lambda z: n(f)(m(f)(z))
BARE_MULT = lambda n: lambda m: lambda f: lambda z: n(m(f))(z)

_PRED = lambda n: lambda f: lambda z: (n(lambda g: (lambda h: h(g(f)))))(lambda u: z)(lambda u: u)
BARE_SUB = lambda n: lambda m: m(_PRED)(n)

BARE_IS_ZERO = lambda n: n(lambda _: BARE_FALSE)(BARE_TRUE)

BARE_NOT = lambda b: lambda ontrue: lambda onfalse: b(onfalse)(ontrue)
BARE_AND = lambda b1: lambda b2: b1(lambda _: b2)(lambda _: BARE_FALSE)
BARE_OR  = lambda b1: lambda b2: b1(lambda _: BARE_TRUE)(lambda _: b2)
BARE_XOR = lambda b1: lambda b2: b1(lambda _: BARE_NOT(b2))(lambda _: b2)
BARE_EQUALP = lambda n1: lambda n2: (BARE_AND(BARE_IS_ZERO(BARE_SUB(n1)(n2)))
                                             (BARE_IS_ZERO(BARE_SUB(n2)(n1))))

BARE_LEQ = lambda n1: lambda n2: BARE_IS_ZERO(BARE_SUB(n1)(n2))
BARE_GEQ = lambda n1: lambda n2: BARE_IS_ZERO(BARE_SUB(n2)(n1))
BARE_LT = lambda n1: lambda n2: BARE_NOT(BARE_GEQ(n1)(n2))
BARE_GT = lambda n1: lambda n2: BARE_NOT(BARE_LEQ(n1)(n2))

# recursion combinator
Y = ((lambda f: lambda F: F(lambda x: f(f)(F)(x)))
     (lambda f: lambda F: F(lambda x: f(f)(F)(x))))

# bare pairs: functions which take a function f and call it with f(head, tail)
BARE_PAIR = lambda head: lambda tail: lambda f: f(head)(tail)
BARE_PAIRHEAD = lambda pair: pair(lambda head: lambda tail: head)
BARE_PAIRTAIL = lambda pair: pair(lambda head: lambda tail: tail)

# conses: conceptually, are either NIL or a bare pair. they are functions which
# take argument functions (onempty, onpair) and, when called, either invoke
# onempty(VOID) or onpair(head, tail)
BARE_NIL = lambda onempty: lambda onpair: onempty(BARE_VOID)
BARE_CONS = lambda head: lambda tail: lambda onempty: lambda onpair: onpair(head)(tail)
BARE_CONSHEAD = lambda cons: cons(BARE_VOID)(lambda head: lambda tail: head)
BARE_CONSTAIL = lambda cons: cons(BARE_VOID)(lambda head: lambda tail: tail)
BARE_IS_NIL = lambda cons: cons(lambda _: BARE_TRUE)(lambda _: lambda _: BARE_FALSE)

# bare lists: either NIL, or a cons where the tail is a bare list
BARE_APPEND = Y(lambda APPEND_r:
                  lambda lst: lambda newval:
                    lst(lambda _: BARE_CONS(newval)(BARE_NIL))
                       (lambda head: lambda tail: BARE_CONS(head)(APPEND_r(tail)(newval))))
BARE_PREPEND = BARE_CONS

BARE_CONCAT = Y(lambda CONCAT_r:
                  lambda lst1: lambda lst2:
                    lst1(lambda _: lst2)
                        (lambda head: lambda tail: BARE_CONS(head)(CONCAT_r(tail)(lst2))))

BARE_LEN = Y(lambda LEN_r:
                 lambda cons:
                     cons(lambda _: BARE_ZERO)
                         (lambda head: lambda tail: BARE_SUCC(LEN_r(tail))))

# resultpairs: these are bare pairs (something, errnum) indicating the result
# of an operation where a successful result could be anything. errnum is
# a bare number: NO_ERROR_id if no error occurred, or some other error ID
# otherwise. If an error occurred, 'something' is undefined.
BARE_RESULTPAIR = BARE_PAIR
BARE_RESULT_VAL = BARE_PAIRHEAD
BARE_RESULT_ERRVAL = BARE_PAIRTAIL
BARE_RESULT_WAS_ERR = lambda brp: BARE_IS_ZERO(BARE_RESULT_ERRVAL(brp))

BARE_ON_RESULT = lambda brp: lambda onsuccess: lambda onfail: \
        brp(lambda rhead: lambda errid:
               BARE_IF(BARE_IS_ZERO(errid))
                      (lambda _: onsuccess(rhead))
                      (lambda _: onfail(errid)))

# these return resultpairs
BARE_NEXT = lambda rpair: BARE_ON_RESULT(rpair) \
              (lambda lst: lst(lambda _: BARE_RESULTPAIR(BARE_VOID)(INDEX_ERROR_id))
                              (lambda head: lambda tail: BARE_RESULTPAIR(tail)(NO_ERROR_id))) \
              (lambda errnum: rpair)
BARE_NTHCONS = lambda lst: lambda n: n(BARE_NEXT)(BARE_RESULTPAIR(lst)(NO_ERROR_id))
BARE_ELT = lambda lst: lambda n: \
        (lambda rpair: BARE_ON_RESULT(rpair)
           (lambda cons: cons(lambda _: BARE_RESULTPAIR(BARE_VOID)(INDEX_ERROR_id))
                             (lambda head: lambda tail: BARE_RESULTPAIR(head)(NO_ERROR_id)))
           (lambda errnum: rpair)) \
          (BARE_NTHCONS(lst)(n))

# typed objects are pairs where the head is a bare ordinal indicating type,
# and the tail is the bare value.
BARE_TYPEOF = BARE_PAIRHEAD
BARE_VALUEOF = BARE_PAIRTAIL

TYPE_OF = lambda tval: MK_POS_INT(BARE_TYPEOF(tval))

# a VOID-typed object
VOID_id = BARE_ONE
BOOL_id = BARE_TWO
POS_INT_id = BARE_THREE
NEG_INT_id = BARE_FOUR
LIST_id = BARE_FIVE
PAIR_id = BARE_SIX
RESULTPAIR_id = BARE_SEVEN
CHAR_id = BARE_EIGHT
STRING_id = BARE_NINE
ERROR_id = BARE_TEN

_TYPECOMPARER = lambda typenum: lambda typedx: BARE_EQUALP(BARE_TYPEOF(typedx))(typenum)

BARE_IS_VOID = _TYPECOMPARER(VOID_id)
BARE_IS_BOOL = _TYPECOMPARER(BOOL_id)
BARE_IS_POS_INT = _TYPECOMPARER(POS_INT_id)
BARE_IS_NEG_INT = _TYPECOMPARER(NEG_INT_id)
BARE_IS_LIST = _TYPECOMPARER(LIST_id)
BARE_IS_PAIR = _TYPECOMPARER(PAIR_id)
BARE_IS_RESULTPAIR = _TYPECOMPARER(RESULTPAIR_id)
BARE_IS_CHAR = _TYPECOMPARER(CHAR_id)
BARE_IS_STRING = _TYPECOMPARER(STRING_id)
BARE_IS_ERROR = _TYPECOMPARER(ERROR_id)
BARE_IS_INT = lambda typedx: (BARE_OR(BARE_IS_POS_INT(typedx))
                                     (BARE_IS_NEG_INT(typedx)))

BARE_MAKE_TYPEDVAR_MAKER = lambda typnum: lambda val: BARE_PAIR(typnum)(val)

MK_VOID = BARE_MAKE_TYPEDVAR_MAKER(VOID_id)
MK_BOOL = BARE_MAKE_TYPEDVAR_MAKER(BOOL_id)
MK_POS_INT = BARE_MAKE_TYPEDVAR_MAKER(POS_INT_id)
MK_NEG_INT = BARE_MAKE_TYPEDVAR_MAKER(NEG_INT_id)
MK_LIST = BARE_MAKE_TYPEDVAR_MAKER(LIST_id)
MK_PAIR = BARE_MAKE_TYPEDVAR_MAKER(PAIR_id)
MK_RESULTPAIR = BARE_MAKE_TYPEDVAR_MAKER(RESULTPAIR_id)
MK_CHAR = BARE_MAKE_TYPEDVAR_MAKER(CHAR_id)
MK_STRING = BARE_MAKE_TYPEDVAR_MAKER(STRING_id)
MK_ERROR = BARE_MAKE_TYPEDVAR_MAKER(ERROR_id)

MK_RESULTPAIR_FROM = lambda val: lambda errnum: MK_RESULTPAIR(BARE_RESULTPAIR(val)(errnum))

VOID = MK_VOID(BARE_VOID)
TRUE = MK_BOOL(BARE_TRUE)
FALSE = MK_BOOL(BARE_FALSE)
ZERO = MK_POS_INT(BARE_ZERO)

_TYPED_TYPECOMPARER = lambda comparer: lambda tval: MK_BOOL(comparer(tval))

IS_VOID = _TYPED_TYPECOMPARER(BARE_IS_VOID)
IS_BOOL = _TYPED_TYPECOMPARER(BARE_IS_BOOL)
IS_POS_INT = _TYPED_TYPECOMPARER(BARE_IS_POS_INT)
IS_NEG_INT = _TYPED_TYPECOMPARER(BARE_IS_NEG_INT)
IS_INT = _TYPED_TYPECOMPARER(BARE_IS_INT)
IS_LIST = _TYPED_TYPECOMPARER(BARE_IS_LIST)
IS_PAIR = _TYPED_TYPECOMPARER(BARE_IS_PAIR)
IS_RESULTPAIR = _TYPED_TYPECOMPARER(BARE_IS_RESULTPAIR)
IS_CHAR = _TYPED_TYPECOMPARER(BARE_IS_CHAR)
IS_STRING = _TYPED_TYPECOMPARER(BARE_IS_STRING)
IS_ERROR = _TYPED_TYPECOMPARER(BARE_IS_ERROR)

NO_ERROR    = MK_ERROR(NO_ERROR_id)
TYPE_ERROR  = MK_ERROR(TYPE_ERROR_id)
INDEX_ERROR = MK_ERROR(INDEX_ERROR_id)

RETURN_TYPE_ERROR = lambda _: TYPE_ERROR
RETURN_INDEX_ERROR = lambda _: INDEX_ERROR

ON_RESULT = lambda tval: lambda onsuccess: lambda onfail: \
        BARE_IF(BARE_IS_RESULTPAIR(tval)) \
               (lambda _: BARE_ON_RESULT(BARE_VALUEOF(tval))
                            (onsuccess)
                            (lambda errnum: onfail(MK_ERROR(errnum)))) \
               (RETURN_TYPE_ERROR)

OR = lambda tb1: lambda tb2: \
        BARE_IF(BARE_AND(BARE_IS_BOOL(tb1))(BARE_IS_BOOL(tb2))) \
               (lambda _: MK_BOOL(BARE_OR(BARE_VALUEOF(tb1))(BARE_VALUEOF(tb2)))) \
               (RETURN_TYPE_ERROR)
AND = lambda tb1: lambda tb2: \
        BARE_IF(BARE_AND(BARE_IS_BOOL(tb1))(BARE_IS_BOOL(tb2))) \
               (lambda _: MK_BOOL(BARE_AND(BARE_VALUEOF(tb1))(BARE_VALUEOF(tb2)))) \
               (RETURN_TYPE_ERROR)
IF = lambda test: lambda ontrue: lambda onfalse: \
        BARE_IF(BARE_IS_BOOL(test)) \
               (lambda _: BARE_VALUEOF(test)(ontrue)(onfalse)) \
               (RETURN_TYPE_ERROR)

IS_ZERO = lambda tnum: BARE_IF(BARE_IS_INT(tnum)) \
                              (lambda _: MK_BOOL(BARE_IS_ZERO(BARE_VALUEOF(tnum)))) \
                              (RETURN_TYPE_ERROR)

ADD = lambda tn1: lambda tn2: \
        BARE_IF(BARE_AND(BARE_IS_POS_INT(tn1))
                        (BARE_IS_POS_INT(tn2))) \
         (lambda _: MK_POS_INT(BARE_ADD(BARE_VALUEOF(tn1))(BARE_VALUEOF(tn2)))) \
         (lambda _: BARE_IF(BARE_AND(BARE_IS_POS_INT(tn1))
                                    (BARE_IS_NEG_INT(tn2)))
                     (lambda _: BARE_IF(BARE_LEQ(BARE_VALUEOF(tn2))(BARE_VALUEOF(tn1)))
                                 (lambda _: MK_POS_INT(BARE_SUB(BARE_VALUEOF(tn1))
                                                               (BARE_VALUEOF(tn2))))
                                 (lambda _: MK_NEG_INT(BARE_SUB(BARE_VALUEOF(tn2))
                                                               (BARE_VALUEOF(tn1)))))
                     (lambda _: BARE_IF(BARE_AND(BARE_IS_NEG_INT(tn1))
                                                (BARE_IS_POS_INT(tn2)))
                                 (lambda _: BARE_IF(BARE_LEQ(BARE_VALUEOF(tn1))(BARE_VALUEOF(tn2)))
                                             (lambda _: MK_POS_INT(BARE_SUB(BARE_VALUEOF(tn2))
                                                                           (BARE_VALUEOF(tn1))))
                                             (lambda _: MK_NEG_INT(BARE_SUB(BARE_VALUEOF(tn1))
                                                                           (BARE_VALUEOF(tn2)))))
                                 (lambda _: BARE_IF(BARE_AND(BARE_IS_NEG_INT(tn1))
                                                            (BARE_IS_NEG_INT(tn2)))
                                             (lambda _: MK_NEG_INT(BARE_ADD(BARE_VALUEOF(tn1))
                                                                           (BARE_VALUEOF(tn2))))
                                             (RETURN_TYPE_ERROR))))

MULT = lambda tn1: lambda tn2: \
        BARE_IF(BARE_OR(BARE_AND(BARE_IS_POS_INT(tn1))
                                (BARE_IS_POS_INT(tn2)))
                       (BARE_AND(BARE_IS_NEG_INT(tn1))
                                (BARE_IS_NEG_INT(tn2)))) \
         (lambda _: MK_POS_INT(BARE_MULT(BARE_VALUEOF(tn1))(BARE_VALUEOF(tn2)))) \
         (lambda _: BARE_IF(BARE_OR(BARE_AND(BARE_IS_POS_INT(tn1))
                                            (BARE_IS_NEG_INT(tn2)))
                                   (BARE_AND(BARE_IS_NEG_INT(tn1))
                                            (BARE_IS_POS_INT(tn2))))
                     (lambda _: MK_NEG_INT(BARE_MULT(BARE_VALUEOF(tn1))(BARE_VALUEOF(tn2))))
                     (RETURN_TYPE_ERROR))

NEG = lambda tn: BARE_IF(BARE_IS_POS_INT(tn)) \
                        (lambda _: MK_NEG_INT(BARE_VALUEOF(tn))) \
                        (lambda _: BARE_IF(BARE_IS_NEG_INT(tn))
                                          (lambda _: MK_POS_INT(BARE_VALUEOF(tn)))
                                          (RETURN_TYPE_ERROR))

SUB = lambda tn1: lambda tn2: ADD(tn1)(NEG(tn2))

EQUALP = lambda tn1: lambda tn2: \
        BARE_IF(BARE_OR(BARE_AND(BARE_IS_POS_INT(tn1))
                                (BARE_IS_POS_INT(tn2)))
                       (BARE_AND(BARE_IS_NEG_INT(tn1))
                                (BARE_IS_NEG_INT(tn2)))) \
         (lambda _: MK_BOOL(BARE_EQUALP(BARE_VALUEOF(tn1))(BARE_VALUEOF(tn2)))) \
         (lambda _: BARE_IF(BARE_AND(BARE_IS_INT(tn1))
                                    (BARE_IS_INT(tn2)))
                     (lambda _: MK_BOOL(BARE_AND(BARE_IS_ZERO(BARE_VALUEOF(tn1)))
                                                (BARE_IS_ZERO(BARE_VALUEOF(tn2)))))
                     (RETURN_TYPE_ERROR))

IS_EMPTY = lambda tlst: BARE_IF(BARE_IS_LIST(tlst)) \
                               (lambda _: MK_BOOL(BARE_IS_NIL(BARE_VALUEOF(tlst)))) \
                               (RETURN_TYPE_ERROR)

HEAD = lambda tlst: BARE_IF(BARE_IS_LIST(tlst)) \
                           (lambda _: BARE_VALUEOF(tlst)(RETURN_INDEX_ERROR)
                                                     (lambda head: lambda tail: head)) \
                           (RETURN_TYPE_ERROR)
TAIL = lambda tlst: BARE_IF(BARE_IS_LIST(tlst)) \
                           (lambda _: BARE_VALUEOF(tlst)(RETURN_INDEX_ERROR)
                                                     (lambda head: lambda tail: MK_LIST(tail))) \
                           (RETURN_TYPE_ERROR)
LEN = lambda tlst: BARE_IF(BARE_IS_LIST(tlst)) \
                          (lambda _: MK_POS_INT(BARE_LEN(BARE_VALUEOF(tlst)))) \
                          (RETURN_TYPE_ERROR)

ELT = lambda tlst: lambda n: \
        BARE_IF(BARE_AND(BARE_IS_LIST(tlst))
                        (BARE_IS_POS_INT(n))) \
               (lambda _: MK_RESULTPAIR(BARE_ELT(BARE_VALUEOF(tlst))(BARE_VALUEOF(n)))) \
               (lambda _: MK_RESULTPAIR_FROM(VOID)(TYPE_ERROR_id))

PREPEND = lambda tval: lambda tlst: \
        BARE_IF(BARE_IS_LIST(tlst)) \
               (lambda _: MK_LIST(BARE_PREPEND(tval)(BARE_VALUEOF(tlst)))) \
               (RETURN_TYPE_ERROR)

APPEND = lambda tlst: lambda tval: \
        BARE_IF(BARE_IS_LIST(tlst)) \
               (lambda _: MK_LIST(BARE_APPEND(BARE_VALUEOF(tlst))(tval))) \
               (RETURN_TYPE_ERROR)

CONCAT = lambda lst1: lambda lst2: \
        BARE_IF(BARE_AND(BARE_IS_LIST(lst1))
                        (BARE_IS_LIST(lst2))) \
               (lambda _: MK_LIST(BARE_CONCAT(BARE_VALUEOF(lst1))(BARE_VALUEOF(lst2)))) \
               (RETURN_TYPE_ERROR)

STRLEN = lambda tstr: BARE_IF(BARE_IS_STRING(tstr)) \
                             (lambda _: MK_POS_INT(BARE_LEN(BARE_VALUEOF(tstr)))) \
                             (RETURN_TYPE_ERROR)

STRCAT = lambda str1: lambda str2: \
        BARE_IF(BARE_AND(BARE_IS_STRING(str1))
                        (BARE_IS_STRING(str2))) \
               (lambda _: MK_STRING(BARE_CONCAT(BARE_VALUEOF(str1))(BARE_VALUEOF(str2)))) \
               (RETURN_TYPE_ERROR)

STRCHR = lambda tstr: lambda n: \
        BARE_IF(BARE_AND(BARE_IS_STRING(tstr))
                        (BARE_IS_POS_INT(n))) \
               (lambda _: BARE_ON_RESULT(BARE_ELT(BARE_VALUEOF(tstr))(BARE_VALUEOF(n)))
                            (lambda succ: MK_RESULTPAIR_FROM(MK_CHAR(succ))(NO_ERROR_id))
                            (lambda errnum: MK_RESULTPAIR_FROM(VOID)(errnum))) \
               (lambda _: MK_RESULTPAIR_FROM(VOID)(TYPE_ERROR_id))
