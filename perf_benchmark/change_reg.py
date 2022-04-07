#!/usr/bin/python3
import sys



def errorExit(error = ""):
    print(f"Error {error} happened")
    exit(-1)

if len(sys.argv) != 3:
    errorExit()

swapLookup = {'x' : 'r',
        'r' : 'x'}
f = open(sys.argv[1],"r+")

contents = f.read()
back_buf = []
for substr in contents.split(" ")[1:]:
    if sys.argv[2] in substr:
        back_buf.append(substr.replace(sys.argv[2],swapLookup[sys.argv[2]]))
    else:
        back_buf.append(substr)


f.truncate(0)
fin_str = " ".join(back_buf)
print(back_buf)
f.write(fin_str)
f.close()

