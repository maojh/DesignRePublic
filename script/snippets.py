import sys

try:
    print "trying"
    for i in range(1,4):
        if i==2:
            raise ValueError("dfga",i)
        if i==3:
            raise Exception
        print i
except ValueError as err:
    print "exception", err.args[1]
except Exception:
    print "new exception"


def method(a):
    pass        #pass ignore an incomplete block

print "In loop handling"
b = []
jump = 0
for h in range(0,6):
#    print h
    try:
        b.append(5./h)
#        print "", b[h-jump]
    except IndexError:
        print "IndexError"
    except:
        print sys.exc_info()[0]
        jump = jump + 1

print "failed to compute", jump, "times"


#For loop implementation(iterators)

# create an iterator object from that iterable
iter_obj = iter(b)
# infinite loop
while True:
    try:
        # get the next item
        element = next(iter_obj)
#        print element
    except StopIteration:
        # if StopIteration is raised, break from loop
        print "Reached last Item in Iterator"
        break

print "PowTwo"

class PowTwo:
    """Class to implement an iterator
    of powers of two"""

    def __init__(self, max = 0):
        self.max = max

    def __iter__(self):
        self.n = 0
        return self

    def next(self):
        if self.n <= self.max:
            result = 2 ** self.n
            self.n += 1
            return result
        else:
            raise StopIteration

for i in PowTwo(5):
    print i




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print bcolors.HEADER + "Warning" + bcolors.ENDC
print bcolors.OKBLUE + "Warning" + bcolors.ENDC
print bcolors.OKGREEN + "Warning" + bcolors.ENDC
print bcolors.WARNING + "Warning" + bcolors.ENDC
print bcolors.FAIL + "Warning" + bcolors.ENDC
print bcolors.ENDC + "Warning" + bcolors.ENDC
print bcolors.BOLD + "Warning" + bcolors.ENDC
print bcolors.UNDERLINE + "Warning" + bcolors.ENDC
