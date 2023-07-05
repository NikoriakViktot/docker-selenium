from pymetdecoder import synop as s

c = 'AAXX 01061 29328 81498 82504 10133 20112 39956 40088 52009 78082 88900'
synop = "AAXX 01000 33658 42984 03101 10261 20122 39805 40082 57003 555 1/044 ="
output = s.SYNOP()
# print(output.handle_not_implemented(synop))
# print(s.RADIATION_TYPES)
# print(output.decode(synop))
print(output.decode(c))