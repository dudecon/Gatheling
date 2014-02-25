#!/usr/bin/python3

'''
Created on Apr 26, 2013

@author: andy
'''

__all__ = ['Component', 'ModularType', 'Modular', 'Node']

from sys import modules
from collections import OrderedDict

def MergeDicts(*dicts):
	r = {}
	for d in dicts:
		for k, v in d.items():
			if k not in r:
				r[k] = v
			elif isinstance(r[k], dict) and isinstance(v, dict):
				r[k] = MergeDicts(r[k], v)
			else: r[k] += v
	
	return r

class ModularType(type):
	subclasses = {}
	DerivedValues = {}
	filter = {}
	@classmethod
	def __prepare__(mcls, name, bases):
		return {'__classname__': name}
	
	def __new__(cls, name, bases, classDict):
		newClass = type.__new__(cls, name, bases, classDict)
		if 'moduleDepends' in classDict:
			for module in classDict['moduleDepends']:
				if module not in cls.DerivedValues:
					cls.DerivedValues[module] = {}
				cls.DerivedValues[module] = MergeDicts(cls.DerivedValues[module], {newClass: classDict['moduleDepends']})
		if 'filter' in classDict:
			cls.filter = MergeDicts(cls.filter, classDict['filter'])
		if name not in cls.subclasses:
			cls.subclasses[name] = newClass
		_all = modules[newClass.__module__].__dict__.setdefault('__all__', [])
		if name not in _all:
			_all.append(name)
		return newClass
	
	@classmethod
	def getSubclass(cls, idx):
		if idx in cls.subclasses:
			return cls.subclasses[idx]
		raise KeyError("{0}: No such ModularType class.".format(repr(idx)))

class Modular(metaclass=ModularType):
	def __init__(self):
		self._components = OrderedDict()
	
	def addComponent(self, comp):
		if isinstance(comp, Modular):
			o = comp
		elif isinstance(comp, type):
			o = comp()
		else:
			raise TypeError("Got '{0}', expected Component object or class.".format(comp.__class__.__name__))
		component_name = o.__class__.__name__
		if component_name in self._components:
			return self._components[component_name]
		
		self._components[component_name] = o
		o._container = self
		
		if o.__class__ in self.__class__.DerivedValues:
			for mod, depends in self.__class__.DerivedValues[o.__class__].items():
				dependsMet = True
				for depend in depends:
					if depend.__name__ not in self._components:
						dependsMet = False
						break
				if dependsMet:
					c = mod()
					if isinstance(c, mod):
						self.addComponent(mod)
		
		return o
			
	
	def getComponent(self):
		return self
	
	def __getattribute__(self, *args):
		ex = True
		rval = None
		try:
			rval = object.__getattribute__(self, *args)
			ex = False
		except AttributeError as e:
			for component in self._components.values():
				try:
					rval = object.__getattribute__(component, *args)
					ex = False
				except AttributeError:
					pass
				except Exception as f:
					e = f
			if ex:
				raise e
		
		return rval

class Node(Modular):
	id_count = 0
	@classmethod
	def next_id(cls):
		cls.id_count += 1
		return cls.id_count
	
	def __new__(cls, *args, **kwargs):
		o = super().__new__(cls)
		o._ID = cls.next_id()
		
		return o
	
	def __init__(self):
		super().__init__()
		self.__setattr__("get{0}Node".format(self.__class__.__name__), self.getComponent)
		self._Parent = None
		self._Children = {}
	
	@classmethod
	def _ChangeParent(cls, nod, new_parent):
		if nod._Parent is not None:
			nod._Parent._RemoveChildByIndex(nod)
		new_parent._AddChildByIndex(nod)
	
	def _AddChildByIndex(self, child, idx=None):
		if idx is not None:
			index = idx
		else:
			index = child._ID
		if child._ID in self._Children:
			return False
		if child._Parent is not None:
			child._Parent._RemoveChildByIndex(idx)
		child._Parent = self
		self._Children[index] = child
		
		return True
	
	def _RemoveChildByIndex(self, Idx):
		if Idx in self._Children:
			child = self._Children[Idx]
			child._Parent = None
			del self._Children[Idx]
			return child
		return False

class Component(Node):
	HumanName = "ComponentName"
	HumanUnits = "units"
	def __init__(self):
		super().__init__()
		self._identifier = self.__classname__
		self._value = 0
	
	def getTareValue(self):
		return self._value
	
	def setValue(self, value):
		self._value = value
	
	def getValue(self):
		s = self._value
		for child in self._container._Children.values():
			if self.__class__.__name__ in child._components:
				childCompNode = child._components[self.__class__.__name__]
				s += childCompNode.getValue()
		return s
	
	def __str__(self):
		_val = self.getValue()
		try:
			_val = "{0:.6g}".format(_val)
		except:
			pass
		return "{0}: {1} {2}".format(self.HumanName, _val, self.HumanUnits)

class MultiValueComponent(Component):
	def __init__(self):
		super().__init__()
		self._value = {}
	
	def getValueByKey(self, key):
		return self._value[key]
	
	def getValue(self):
		s = self._value
		for child in self._container._Children.values():
			if self.__classname__ in child._components:
				s = MergeDicts(s, child._components[self.__classname__].getValue())
		return s
	
	def __str__(self):
		s = []
		for key, value in self.getValue().items():
			try:
				value = "{0:.6g}".format(value)
			except:
				pass
			units = self.HumanUnits
			if key in self.keyNames:
				key = self.keyNames[key]
			if key in self.keyUnits:
				units = self.keyUnits[key]
			s.append("{0} ({1}): {2} {3}".format(self.HumanName, key, value, units))
		return "\n{0: <{w}}".format('', w=self._container._depth * 4).join(s)
	
	keyNames = {}
	keyUnits = {}

