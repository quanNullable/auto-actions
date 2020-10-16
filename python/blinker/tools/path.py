import sys,os

def addParentDir():
  parentDir=os.path.abspath(os.path.dirname(sys.path[0])+os.path.sep+".")
  sys.path.append(parentDir)