# test_diffhelper.py = test <diffhelper.py>

from ulib import lintest

from ulib.butil import pr, prn, dpr

import diffhelper as dh


#---------------------------------------------------------------------

#---------------------------------------------------------------------

class T_misc(lintest.TestCase):

    def test_1(self):
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

group = lintest.TestGroup()
group.add(T_misc)

if __name__=='__main__': group.run()

#end



#end
