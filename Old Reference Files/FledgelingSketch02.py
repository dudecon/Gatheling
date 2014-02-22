# Fledgeling sketch
DEFAULT_NAME = "mana"
TREE_TYPES = ("person", "idea", "time", "place", "goal")

def MakeType(node, treeType):
    assert treeType in TREE_TYPES , "invalid tree type"
    assert isinstance(node, flNode)
    if treeType in node.types: return
    exec("node.{0}Parent = None".format(treeType))
    exec("node.{0}Children = []".format(treeType))
    node.types += [treeType]

def UnMakeType(node, treeType):
    assert isinstance(node, flNode)
    if treeType not in node.types: return
    # remove all associated children links
    for child in eval("self.{0}Children".format(treeType)):
        ChangeParent(child, treeType, None)
    # remove parent link
    ChangeParent(node, treeType, None)
    # delete the associated properties
    exec("del node.{0}Parent".format(treeType))
    exec("del node.{0}Children".format(treeType))
    # remove the type from the types listing
    node.types.remove(treeType)

def ChangeParent(node, treeType, newParent):
    assert treeType in TREE_TYPES , "invalid tree type"
    assert isinstance(node, flNode)
    assert treeType in node.types
    #print("changing", (node, ), "parent to", (newParent, ))
    oldParent = eval("node.{0}Parent".format(treeType))
    #print("Old parent is",(oldParent, ))
    # remove self from the current parent's "child" list
    if oldParent is not None and eval("node in oldParent.{0}Children".format(treeType)):
        #print("removing", (node, ), "from child list of", (oldParent,))
        exec("oldParent.{0}Children.remove(node)".format(treeType))
    # add self to the new parent's "child" list
    if newParent is not None:
        #print("adding", (node, ), "to child list of", (newParent,))
        exec("newParent.{0}Children += [node]".format(treeType))
    # change the node's internal pointer to its new parent
    #print("updating", (node, ), "Parent pointer to indicate", (newParent, ))
    exec("node.{0}Parent = newParent".format(treeType))
    #print("new parent is", (eval("node.{0}Parent".format(treeType)), ))
    # if node's new parent is also it's child, make the old parent
    # the new parent's parent
    # ...
    # to prevent orphaning and looping child parent relationships
    # you can still get this with three step parent chains, but at least
    # it's harder to do accidentally during parenthood inversions
    if eval("newParent in node.{0}Children".format(treeType)):
        #print("inverting paranthood of: ", newParent, oldParent, "around", node)
        ChangeParent(newParent, treeType, oldParent)
    #print("done changing parent")

class flNode(object):        
    def __init__(self, names = None, kind = None):
        # set the names
        if names == None:
            self.names = [DEFAULT_NAME]
        elif isinstance(names, str):
            self.names = [names]
        else:
            assert isinstance(names, (list, tuple))
            for name in names:
                assert isinstance(name, str) , "names must be strings"
            self.names = [i for i in names]

        # set the types
        self.types = []
        # using no kind of thing
        if kind == None:
            pass
        # using another node
        # assume this other node is the parent in all of these properties
        elif isinstance(kind, flNode):
            # set the types of the node to the types of its prototype
            for t in kind.types:
                MakeType(self, t)
                ChangeParent(self, t, kind)
        # using a list of tree types
        elif isinstance(kind, (list, tuple)):
            for t in kind:
                MakeType(self, t)
        # make a value, for debugging mostly
        self.value = 0

    def __del__(self):
        # remove hierarchy links
        for treeType in self.types:
            UnMakeType(self, treeType)        
                
    def __str__(self):
        result = ""
        result += self.names[0] + " "
        result += "types are:"
        for i in self.types:
            result += " " + i
        result += " value = "
        result += str(self.value)
        return result

    def __repr__(self):
        result = self.names[0]
        return result

    #numeric stuff
    def __int__(self): return int(self.value)
    def __float__(self): return float(self.value)
    def __round__(self, n=0): return round(self.value, n)
    def __neg__(self): return -self.value
    def __pos__(self): return +self.value
    def __abs__(self): return abs(self.value)
    def __invert__(self): return ~self.value
    # operator pairs for numeric emulation
    operator_pairs = (('add',"+"),('sub',"-"),('mul',"*"),
                      ('truediv',"/"),('floordiv',"//"),('mod',"%"),
                      ('pow',"**"))
    # declare all the left numeric methods
    for pair in operator_pairs:
        exec("def __{0}__(self, other): return self.value {1} other".format(pair[0],pair[1]))
    # declare all the right numeric methods
    for pair in operator_pairs:
        exec("def __r{0}__(self, other): return other {1} self.value".format(pair[0],pair[1]))
        

#----------------------------------------------------
# some test code below
#----------------------------------------------------

bob = flNode("bob", ("place", "person"))
square = flNode("town square", ("place",))
town = flNode("the town", ("place",))
ChangeParent(square, "place", town)
ChangeParent(bob, "place", square)
print("bob's children: ", bob.placeChildren)
print("square's children: ", square.placeChildren)
print("town's children: ", town.placeChildren)
print("invert parenthood between Bob and Square")
ChangeParent(square, "place", bob)
print("bob's children: ", bob.placeChildren)
print("square's children: ", square.placeChildren)
print("town's children: ", town.placeChildren)
# note, bug!
# looping paranthood! Why?
