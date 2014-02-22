# Fledgeling sketch

# need to make a way for ideas to have more than one "structural parent"

class Node(object):
    def change_parent(self, new_parent):
        assert isinstance(new_parent, Node), "target parent is not a Node"
        # record the current parent
        old_parent = self.parent
        # remove self from the current parent's "child" list
        if self in old_parent.children: old_parent.children.pop(self)
        # add self to the new parent's "child" list
        # unless this is its own parent, in which case parenthood is a one-way relationship
        if new_parent is not self: new_parent.children += [self]
        # change our internal pointer to the new parent
        self.parent = new_parent
        # and we're done here

    def add_attribute(self, attribute, target_value = 0):
        assert isinstance(attribute, Node), "Attribute is not a Node. That won't work!"
        # make a new instance, a child of the attribute
        new_attribute = Node(value = target_value, parent = attribute)
        # get the type of the attribute
        attribute_type = attribute.type
        # make this new attribute have a subordinate type to its ideal
        new_attribute.type = attribute_type + "_inst"
        # make a new variable for the attribute
        exec("self.{0} = new_attribute".format(attribute_type))
        # NOTE:
        # A node may have only one attribute of each type at any time.
        
    def __init__(self, name = None, attributes = None, value = 0, parent = None, children = None):
        
        # set the type
        if name == None:
            if parent == None:
                raise Exception("No name AND no parent! What do you want from me?")
            else:
                # we don't have a name, but we do have a parent,
                # Use the parent's name and add "junior"
                self.name = parent.name + " Jr."
        else:
            # use the specified name
            assert isinstance(name, str), "name must be a string"
            self.name = name
        #initialize the object hierarchy
        if children == None:
            self.children = []
        else:
            self.children = children
        self.parent = self
        # if there is no parent, make yourself the parent
        if parent == None: parent = self
        self.change_parent(parent)
        #If attributes are not specified, use the parent's attributes
        if attributes == None:
            if self.parent is self:
                # Node is its own parent,
                # and has no explicit attributes
                # in which case there will be no attributes
                self.attributes = []
            else:
                # Node inherits the parent's attributes
                self.attributes = self.parent.attributes
        else:
            #use a specified set of attributes
            self.attributes = attributes
            #Make the attributes real
            for val in self.attributes:
                self.add_attribute(val)
        # set the value
        self.value = value
                
    def __str__(self):
        result = ""
        result += self.type + " = "
        result += str(self.value)
        return result

    def __repr__(self):
        result = ""
        result += self.type + ", "
        result += str(self.value) + " value, "
        result += str(len(self.attributes)) + " attributes, "
        result += str(len(self.children)) + " children"
        result = '<' + result + '>'
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

mass = Node("mass")
happiness = Node("happiness")
Eubellience = Node("bubblyness")

bob = Node("person", [happiness, mass])
Nick = Node("person", [happiness], parent = bob)
NickSon = Node("person", [mass, Eubellience], parent = Nick)
print(bob)
print(bob.children)
print(bob.attributes)
print(Nick)
print(Nick.children)
print(Nick.attributes)
print(NickSon)
print(NickSon.children)
print(NickSon.attributes)
