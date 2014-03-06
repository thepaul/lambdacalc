import unittest
from church import *
from using_church import *

class TestChurch(unittest.TestCase):
    def assertBareBool(self, b, expected=True):
        self.assertIs(bare_boolify(b), bool(expected))

    def assertBareNum(self, n, expected):
        num = bare_numerify(n)
        self.assertEqual(num, expected)

    def assertChurch(self, chrch, val=True, msg=None):
        self.assertEqual(dechurchify(chrch), val, msg=msg)

    def test_basic(self):
        def fail(*_):
            raise Exception('fail called')

        self.assertEqual(BARE_VOID('foo'), 'foo')
        self.assertEqual(BARE_ZERO(fail)(0), 0)

        self.assertEqual(BARE_IF(BARE_TRUE)(lambda _: 1)(fail), 1)
        self.assertEqual(BARE_IF(BARE_FALSE)(fail)(lambda _: 2), 2)

    def test_bare_bools(self):
        self.assertBareBool(BARE_TRUE)
        self.assertBareBool(BARE_FALSE, False)

    def test_bare_nums(self):
        self.assertBareNum(BARE_ONE, 1)
        self.assertBareNum(BARE_TWO, 2)
        self.assertBareNum(BARE_THREE, 3)
        self.assertBareNum(BARE_FOUR, 4)
        self.assertBareNum(BARE_TEN, 10)

    def test_bare_add(self):
        self.assertBareNum(BARE_ADD(BARE_TEN)(BARE_TEN), 20)
        self.assertBareNum(BARE_ADD(BARE_TEN)(BARE_ZERO), 10)
        self.assertBareNum(BARE_ADD(BARE_ZERO)(BARE_TEN), 10)
        self.assertBareNum(BARE_ADD(BARE_ZERO)(BARE_ZERO), 0)

    def test_bare_mult(self):
        self.assertBareNum(BARE_MULT(BARE_TEN)(BARE_TEN), 100)
        self.assertBareNum(BARE_MULT(BARE_TEN)(BARE_ZERO), 0)
        self.assertBareNum(BARE_MULT(BARE_ZERO)(BARE_ZERO), 0)
        self.assertBareNum(BARE_MULT(BARE_ZERO)(BARE_TEN), 0)

    def test_bare_sub(self):
        self.assertBareNum(BARE_SUB(BARE_ZERO)(BARE_ZERO), 0)
        self.assertBareNum(BARE_SUB(BARE_TEN)(BARE_ZERO), 10)
        self.assertBareNum(BARE_SUB(BARE_TEN)(BARE_FIVE), 5)

    def test_bare_is_zero(self):
        self.assertBareBool(BARE_IS_ZERO(BARE_ZERO))
        self.assertBareBool(BARE_IS_ZERO(BARE_ONE), False)

    def test_bare_not(self):
        self.assertBareBool(BARE_NOT(BARE_TRUE), False)
        self.assertBareBool(BARE_NOT(BARE_FALSE))
        self.assertBareBool(BARE_NOT(BARE_NOT(BARE_FALSE)), False)

    def test_bare_or(self):
        self.assertBareBool(BARE_OR(BARE_FALSE)(BARE_FALSE), False)
        self.assertBareBool(BARE_OR(BARE_FALSE)(BARE_TRUE))
        self.assertBareBool(BARE_OR(BARE_TRUE)(BARE_FALSE))
        self.assertBareBool(BARE_OR(BARE_TRUE)(BARE_TRUE))

    def test_bare_and(self):
        self.assertBareBool(BARE_AND(BARE_FALSE)(BARE_FALSE), False)
        self.assertBareBool(BARE_AND(BARE_FALSE)(BARE_TRUE), False)
        self.assertBareBool(BARE_AND(BARE_TRUE)(BARE_FALSE), False)
        self.assertBareBool(BARE_AND(BARE_TRUE)(BARE_TRUE))

    def test_bare_xor(self):
        self.assertBareBool(BARE_XOR(BARE_FALSE)(BARE_FALSE), False)
        self.assertBareBool(BARE_XOR(BARE_FALSE)(BARE_TRUE))
        self.assertBareBool(BARE_XOR(BARE_TRUE)(BARE_FALSE))
        self.assertBareBool(BARE_XOR(BARE_TRUE)(BARE_TRUE), False)

    def test_bare_logic(self):
        self.assertBareBool(BARE_AND(BARE_OR(BARE_TRUE)(BARE_FALSE))
                                    (BARE_NOT(BARE_XOR(BARE_TRUE)(BARE_TRUE))))

    def test_bare_equalp(self):
        self.assertBareBool(BARE_EQUALP(BARE_TEN)(BARE_TEN))
        self.assertBareBool(BARE_EQUALP(BARE_TEN)(BARE_NINE), False)
        self.assertBareBool(BARE_EQUALP(BARE_NINE)(BARE_TEN), False)
        self.assertBareBool(BARE_EQUALP(BARE_ZERO)(BARE_ONE), False)
        self.assertBareBool(BARE_EQUALP(BARE_ZERO)(BARE_ZERO))

    def test_bare_leq(self):
        self.assertBareBool(BARE_LEQ(BARE_TEN)(BARE_TEN))
        self.assertBareBool(BARE_LEQ(BARE_ZERO)(BARE_TEN))
        self.assertBareBool(BARE_LEQ(BARE_TEN)(BARE_ZERO), False)
        self.assertBareBool(BARE_LEQ(BARE_ZERO)(BARE_ZERO))

    def test_bare_geq(self):
        self.assertBareBool(BARE_GEQ(BARE_TEN)(BARE_TEN))
        self.assertBareBool(BARE_GEQ(BARE_ZERO)(BARE_TEN), False)
        self.assertBareBool(BARE_GEQ(BARE_TEN)(BARE_ZERO))
        self.assertBareBool(BARE_GEQ(BARE_ZERO)(BARE_ZERO))

    def test_bare_lt(self):
        self.assertBareBool(BARE_LT(BARE_TEN)(BARE_TEN), False)
        self.assertBareBool(BARE_LT(BARE_ZERO)(BARE_TEN))
        self.assertBareBool(BARE_LT(BARE_TEN)(BARE_ZERO), False)
        self.assertBareBool(BARE_LT(BARE_ZERO)(BARE_ZERO), False)

    def test_bare_gt(self):
        self.assertBareBool(BARE_GT(BARE_TEN)(BARE_TEN), False)
        self.assertBareBool(BARE_GT(BARE_ZERO)(BARE_TEN), False)
        self.assertBareBool(BARE_GT(BARE_TEN)(BARE_ZERO))
        self.assertBareBool(BARE_GT(BARE_ZERO)(BARE_ZERO), False)

    def test_bare_lists(self):
        self.assertEqual(bare_listify(BARE_NIL), [])
        barelist = BARE_PREPEND(BARE_ONE)(BARE_PREPEND(BARE_TWO)(BARE_NIL))
        self.assertListEqual(map(bare_numerify, bare_listify(barelist)), [1, 2])
        self.assertBareNum(BARE_LEN(barelist), 2)
        self.assertBareNum(BARE_LEN(bare_churchify([6] * 200)), 200)
        self.assertBareNum(BARE_CONSHEAD(BARE_CONSTAIL(barelist)), 2)
        self.assertBareBool(BARE_IS_NIL(barelist), False)
        self.assertBareBool(BARE_IS_NIL(BARE_NIL))
        self.assertBareBool(BARE_IS_NIL(BARE_CONSTAIL(BARE_CONSTAIL(barelist))))
        barelist2 = BARE_APPEND(barelist)(BARE_EIGHT)
        self.assertListEqual(map(bare_numerify, bare_listify(barelist2)), [1, 2, 8])
        one_element = BARE_APPEND(BARE_NIL)(BARE_NIL)
        self.assertBareNum(BARE_LEN(one_element), 1)
        respair = BARE_ELT(barelist2)(BARE_TWO)

    def test_type_tests(self):
        self.assertChurch(IS_VOID(VOID))
        self.assertChurch(IS_BOOL(FALSE))
        self.assertChurch(IS_BOOL(TRUE))
        self.assertChurch(IS_BOOL(VOID), False)
        self.assertChurch(IS_LIST(TYPE_ERROR), False)
        self.assertChurch(IS_ERROR(TYPE_ERROR))
        self.assertChurch(IS_INT(ZERO))

        typedlist = MK_LIST(BARE_PREPEND(BARE_ONE)(BARE_PREPEND(BARE_NINE)(BARE_NIL)))
        self.assertChurch(IS_INT(typedlist), False)
        self.assertChurch(IS_LIST(typedlist))
        self.assertChurch(IS_LIST(MK_LIST(BARE_NIL)))

    def test_list_len(self):
        typedlist = MK_LIST(BARE_PREPEND(BARE_TEN)(BARE_NIL))
        self.assertChurch(LEN(typedlist), 1)
        self.assertChurch(LEN(VOID), ChurchTypeError)
        self.assertChurch(IS_EMPTY(MK_LIST(BARE_NIL)))
        self.assertChurch(IS_EMPTY(typedlist), False)
        self.assertChurch(IS_EMPTY(VOID), ChurchTypeError)

    def assert_op(self, opname, a, b, result):
        op = globals()[opname]
        for n1 in ((0, neg_zero) if a == 0 else (a,)):
            for n2 in ((0, neg_zero) if b == 0 else (b,)):
                self.assertChurch(op(churchify(n1))(churchify(n2)), result,
                                  '%s(%r, %r) != %r' % (opname, n1, n2, result))

    assert_add = lambda self, a, b, c: self.assert_op('ADD', a, b, c)
    assert_sub = lambda self, a, b, c: self.assert_op('SUB', a, b, c)
    assert_mult = lambda self, a, b, c: self.assert_op('MULT', a, b, c)
    assert_equalp = lambda self, a, b, c: self.assert_op('EQUALP', a, b, c)

    def test_add(self):
        self.assert_add(23, 12, 35)
        self.assert_add(23, -12, 11)
        self.assert_add(-23, 12, -11)
        self.assert_add(-23, -12, -35)
        self.assert_add(0, 0, 0)
        self.assert_add(0, -1, -1)
        self.assertChurch(ADD(TRUE)(churchify(3)), ChurchTypeError)
        self.assertChurch(ADD(ZERO)(MK_LIST(BARE_NIL)), ChurchTypeError)

    def test_sub(self):
        self.assert_sub(23, 73, -50)
        self.assert_sub(23, -73, 96)
        self.assert_sub(-23, 73, -96)
        self.assert_sub(-23, -73, 50)

    def test_mult(self):
        self.assert_mult(0, 0, 0)
        self.assert_mult(0, 1, 0)
        self.assert_mult(1, 0, 0)
        self.assert_mult(1, 1, 1)
        self.assert_mult(2, 2, 4)
        self.assert_mult(-2, 2, -4)
        self.assert_mult(2, -2, -4)
        self.assert_mult(-2, -2, 4)
        self.assert_mult(-3, 0, 0)
        self.assert_mult(0, -1, 0)

    def test_equalp(self):
        self.assert_equalp(0, 0, True)
        self.assert_equalp(0, 1, False)
        self.assert_equalp(0, -1, False)
        self.assert_equalp(1, 0, False)
        self.assert_equalp(1, 1, True)
        self.assert_equalp(1, -1, False)
        self.assert_equalp(-1, 0, False)
        self.assert_equalp(-1, 1, False)
        self.assert_equalp(-1, -1, True)

    def test_neg(self):
        self.assertChurch(NEG(ZERO), 0)
        self.assertChurch(NEG(churchify(12)), -12)
        self.assertChurch(NEG(churchify(-24)), 24)

    def test_elt(self):
        list1 = churchify([1, 2, 9])
        self.assertChurch(list1, [1, 2, 9])
        self.assertChurch(ELT(list1)(churchify(2)), 9)
        self.assertChurch(ELT(list1)(churchify(0)), 1)
        self.assertChurch(ELT(list1)(churchify(3)), ChurchIndexError)
        self.assertChurch(ELT(list1)(churchify(23)), ChurchIndexError)

    def test_append(self):
        list1 = churchify([1, 2, 3])
        list2 = APPEND(list1)(churchify([4, 5, 6]))
        self.assertChurch(LEN(list2), 4)  # last element is a list
        self.assertChurch(IS_LIST(list2))
        self.assertChurch(ON_RESULT(ELT(list2)(churchify(3)))
                            (lambda onsucc: IS_LIST(onsucc))
                            (lambda onfail: onfail))
        self.assertChurch(ON_RESULT(ELT(list1)(churchify(3)))
                            (lambda onsucc: IS_LIST(onsucc))
                            (lambda onfail: onfail),
                          ChurchIndexError)
        self.assertChurch(list2, [1, 2, 3, [4, 5, 6]])

    def test_strs(self):
        x = churchify('hi')
        self.assertChurch(IS_STRING(x))
        self.assertChurch(churchify('foobar baz'), 'foobar baz')
        self.assertChurch(STRLEN(churchify('blah')), 4)
        self.assertChurch(STRLEN(churchify('')), 0)
        self.assertChurch(STRCAT(churchify("abcd"))(churchify("efg")), "abcdefg")
        self.assertChurch(STRCHR(churchify("Mal Reynolds"))(churchify(0)), 'M')
        self.assertChurch(STRCHR(churchify("Mal Reynolds"))(churchify(3)), ' ')
        self.assertChurch(STRCHR(churchify("Mal Reynolds"))(churchify(33)), ChurchIndexError)
