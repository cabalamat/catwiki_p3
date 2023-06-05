# diffhelper.py = make <difflib> easier to use


import difflib
from typing import List, Literal, Tuple
from enum import Enum

from ulib import butil
from ulib.butil import pr, prn, form, dpr, dpvars, printargs

#---------------------------------------------------------------------

DiffLineType = Literal[
    'OLD_TITLE',
    'NEW_TITLE',
    'GROUP_INTRO',
    'ADD_LINE',
    'REMOVE_LINE',
    'UNCHANGED_LINE',
]

DiffLineState = Literal[
    'AT_START',
    'IN_GROUP',
]

class DiffInfo:
    diffItems: 'DiffItem' = []
    oln: int = -1 # line number in old file
    nln: int = -1 # line number in new file

    def __init__(
        self,
        oldData: List[str],
        newData: List[str],
        oldDesc: str,
        newDesc: str):
        """ Build diff information for oldData/newData
        oldData = the old file contents
        newData = the new file contents
        oldDesc = a description of the old file, e.g. a filename
        newDesc = a description of the new file, e.g. a filename
        """
        self.diffItems = [] # result
        dpvars("self.diffItems")
        dr = difflib.unified_diff(oldData, newData, oldDesc, newDesc)

        ldr = list(dr)
        dpr("ldr=%r::%s", ldr, type(ldr))
        for s in ldr:
            prn("[%s]", s)

        state = 'AT_START'
        dpvars("state")
        for line in ldr:
            di = DiffItem(self)
            di.readLine(state, line)
            state = di.state
            dpvars("di")
            dpvars("state")
            self.diffItems.append(di)
        #//for



class DiffItem:
    """ one line of a diff """
    info: DiffInfo # the DiffInfo we're part of
    lineStr: str # the line input
    state: DiffLineState # state of this line
    lineType: DiffLineType # type of this line
    strippedLineStr: str # this line minus unnecessay stuff
    oldLineNum: int = -1
    newLineNum: int = -1

    def __init__(self, diffInfo: DiffInfo):
        self.info = diffInfo

    def __repr__(self) -> str:
        r = form("<DiffItem lineStr=%r state=%r lineType=%r oLN=%r nLN=%r>",
            self.lineStr,
            self.state, self.lineType,
            self.oldLineNum, self.newLineNum)
        return r

    def readLine(self, state: DiffLineState, line: str) -> DiffLineState:
        dpvars("state line")
        self.lineStr = line
        self.state = state

        if state == 'AT_START' and line.startswith("--- "):
            self.strippedLineStr = line[4:].strip()
            self.lineType = 'OLD_TITLE'
            return

        if state == 'AT_START' and line.startswith("+++ "):
            self.strippedLineStr = line[4:].strip()
            self.lineType = 'NEW_TITLE'
            return

        if line.startswith("@"):
            self.lineType = 'GROUP_INTRO'
            self.state = 'IN_GROUP'
            self.oldLineNum, self.newLineNum = readGroupIntro(line)
            return

        ata: int = 1 # amount to add
        if self.prev().lineType == 'GROUP_INTRO':
            ata = 0

        if state == 'IN_GROUP' and line.startswith("+"):
            self.lineType = 'ADD_LINE'
            self.strippedLineStr = line[1:].rstrip()
            self.oldLineNum = self.prev().oldLineNum
            self.newLineNum = self.prev().newLineNum + ata

        if state == 'IN_GROUP' and line.startswith("-"):
            self.lineType = 'REMOVE_LINE'
            self.strippedLineStr = line[1:].rstrip()
            self.oldLineNum = self.prev().oldLineNum + ata
            self.newLineNum = self.prev().newLineNum

        if state == 'IN_GROUP' and line.startswith(" "):
            self.lineType = 'UNCHANGED_LINE'
            self.strippedLineStr = line[1:].rstrip()
            self.oldLineNum = self.prev().oldLineNum + ata
            self.newLineNum = self.prev().newLineNum + ata

    def prev(self) -> 'DiffItem':
        """ return the previous DiffItem """
        prevDI = self.info.diffItems[-1]
        return prevDI


@printargs
def readGroupIntro(line: str) -> Tuple[int, int]:
    """ a group intro is a string like '@@ -8,7 +9,7 @@'
    where the 1st number (8 in the example) is the start line
    number in the old file, and the 3rd (9 in example) is the
    start line number in the new file.

    Return those numbers.
    """
    _, afterMinus = line.split("-", 1)
    oldStr, afterPlus = afterMinus.split("+", 1)
    ii = getPositiveInts(oldStr)
    if len(ii)>=1:
        oldNum = ii[0]
    else:
        oldNum = 0
    jj = getPositiveInts(afterPlus)
    if len(jj)>=1:
        newNum = jj[0]
    else:
        newNum = 0
    return (oldNum, newNum)

def getPositiveInts(s: str) -> List[int]:
    """ find positive integers in a string.
    Every chars not in [0-9] is converted to a space.
    Then the integers are found and returned.
    E.g. getPositiveInts(" 3xxx7-8+91zzz") => [3,7,8,91]
    """
    s2 = ""
    for ch in s:
        if ch in "0123456789":
            s2 += ch
        else:
            s2 += " "
    groups = s2.split()
    r = []
    for g in groups:
        try:
            i = int(g)
        except ValueError:
            continue
        r.append(i)
    #//for
    return r




#---------------------------------------------------------------------

def makeDiffLines(
    oldData: List[str], newData: List[str],
    oldDesc: str, newDesc: str
    ) -> DiffInfo:
    """ Build diff information for oldData/newData
    oldData = the old file contents
    newData = the new file contents
    oldDesc = a description of the old file, e.g. a filename
    newDesc = a description of the new file, e.g. a filename

    """
    diffInfo = DiffInfo(oldData, newData, oldDesc, newDesc)
    return diffInfo





#end
