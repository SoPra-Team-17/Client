import cppyy

def init_cppyy():
    cppyy.add_library_path("/usr/local/lib")

    cppyy.load_library("SopraClient")
    cppyy.load_library("SopraCommon")
    cppyy.load_library("SopraNetwork")
