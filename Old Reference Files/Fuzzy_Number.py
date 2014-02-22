# a "number" class with fuzzy values

class FuzzNum(object):
    # a floating point number with a fuzzy value
    def __init__(self, median = 0., variance = 0.):
        self.med = median
        # radius must be zero or positive
        self.var = max(variance,0)

    def __str__(self):
        return "{0} +- {1}".format(self.med, self.var)

    # operator pairs for numeric emulation
    numeric_operator_pairs = (('add',"+"),('sub',"-"),('mul',"*"),
                      ('truediv',"/"),('floordiv',"//"),('mod',"%"),
                      ('pow',"**"))
    # declare all the left numeric methods
    for pair in numeric_operator_pairs:
        exec("def __{0}__(self, other): return FuzzNum(self.med {1} other.med,\
             self.var {1} other.var)".format(pair[0],pair[1]))
    # declare all the right numeric methods
    for pair in numeric_operator_pairs:
        exec("def __r{0}__(self, other): return FuzzNum(other.med {1} self.med,\
             other.var {1} self.var)".format(pair[0],pair[1]))
    
    # declare all the comparison overloads
    def __eq__(self, other):
        diff = abs(self.med - other.med)
        slop = self.var + other.var
        return diff <= slop
    def __ne__(self, other):
        return not self == other
    # operator pairs for comparison overloads
    comparison_operator_pairs_simple = (('lt','<'),('gt','>'))
    for pair in comparison_operator_pairs_simple:
        exec("def __{0}__(self, other): return self.med {1} other.med".format(pair[0],pair[1]))
    # declare the compound comparison overloads
    def __le__(self, other): return self == other or self < other
    def __ge__(self, other): return self == other or self > other

#----------------------------------------------------
# some test code below
#----------------------------------------------------

test_stuff = ("a","b","a == b","a < b","a >= b","a > b","a + b",
              "a - b","b - a","a - a","a / b","a // b","a * b",
              "b / a","b // a")
a = FuzzNum(3,2.5)
b = FuzzNum(7.1,3)
for stuff in test_stuff:
    exec('print("{0}:",{0})'.format(stuff))
