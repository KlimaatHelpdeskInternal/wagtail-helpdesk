import unittest



class SampleTestCase(unittest.TestCase):

    def teststring(self):
        a= 'some'
        b= 'some'
        self.assertEqual(a, b)
    def testint(self):
        a= 4
        b= 4
        self.assertEqual(a, b)
