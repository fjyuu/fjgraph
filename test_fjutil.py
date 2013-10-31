import unittest
import fjutil


class UtilTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_str2float(self):
        f = fjutil.str2float("1.1")
        self.assertEqual(f, 1.1)

        f1, f2 = fjutil.str2float("1.1", "1.2")
        self.assertEqual(f1, 1.1)
        self.assertEqual(f2, 1.2)

    def test_str2float_e(self):
        f = fjutil.str2float("2e2")
        self.assertEqual(f, 2.0 * (10 ** 2))

        f = fjutil.str2float("2e")
        self.assertEqual(f, 2.0)

        f = fjutil.str2float("2e-1")
        self.assertEqual(f, 2.0 * (10 ** -1))
