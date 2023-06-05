# test_diffhelper.py = test <diffhelper.py>

from ulib import lintest

from ulib.butil import pr, prn, dpr

import diffhelper as dh


#---------------------------------------------------------------------

#---------------------------------------------------------------------

class T_misc(lintest.TestCase):

    def test_makeDiffLines(self):
        oData = [
            "alpha",
            "beta",
            "gamma",
            "delta",
            "epsilon",
            "fff ff",
            "gg ggg",
            "h hh hhh",
        ]
        nData = [
            "alpha",
            "beta",
            "gamma",
            "different",
            "epsilon",
            "fff ff",
            "gg ggg",
            "h hh hhh",
        ]
        r = dh.makeDiffLines(oData, nData, "old", "new")
        dpr("r=%r", r)

#---------------------------------------------------------------------

class T_readGroupIntro(lintest.TestCase):
    """ the readGroupIntro() function """

    def test_getPositiveInts(self):
        r = dh.getPositiveInts("")
        self.assertSame(r, [], "no ints")

        r = dh.getPositiveInts("34xxxx67zzz9")
        self.assertSame(r, [34,67,9])

        r = dh.getPositiveInts("34xxxx067zzz9")
        self.assertSame(r, [34,67,9])

        r = dh.getPositiveInts("34xxxx0067zzz9")
        self.assertSame(r, [34,67,9])

        r = dh.getPositiveInts("@@ -8,7 +9,6 @@")
        self.assertSame(r, [8, 7, 9, 6])

    def test_normal(self):
        r = dh.readGroupIntro("@@ -8,7 +9,6 @@")
        self.assertSame(r, (8,9))


#---------------------------------------------------------------------

group = lintest.TestGroup()
group.add(T_misc)
group.add(T_readGroupIntro)

if __name__=='__main__': group.run()

#end



#end
