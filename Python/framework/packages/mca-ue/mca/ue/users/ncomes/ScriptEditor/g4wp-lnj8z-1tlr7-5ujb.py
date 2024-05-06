import unreal
from mca.ue import pyunreal as pue

class AssetDefinitions:
	def __init__(self, *args, **kwargs):
		self._dict = {unreal.SkeletalMesh: pue.PySkelMesh}
	
	def __getattr__(self, name):
		def func(*args, **kwargs):
			resp = {unreal.SkeletalMesh: pue.PySkelMesh}[args[0]]    # Decide which responder to use (example)
			return kwargs.get(name, None)         # Call the function on the responder
		return func


df = AssetDefinitions()

jkl = df.getattr(unreal.SkeletalMesh)
print(jkl)

defi = AssetDefinitions()

get_attr = defi.func(unreal.SkeletalMesh)




_dict = {unreal.SkeletalMesh: pue.PySkelMesh}


print(_dict.get(unreal.SkeletalMesh))


class RandomResponder(object):
    choices = [A, B, C]

    @classmethod
    def which(cls):
        return random.choice(cls.choices)

    def __getattr__(self, attr):
        return getattr(self.which(), attr)

import random

class RandomResponder(object):
	choices = [unreal.SkeletalMesh]
	
	@classmethod
	def which(cls):
		return random.choice(cls.choices)

	def __getattr__(self, attr):
        # we define a function that actually gets called
        # which takes up the first positional argument,
        # the rest are left to args and kwargs
		def doCall(which, *args, **kwargs):
            # get the attribute of the appropriate one, call with passed args
			return getattr(self.choices[which], attr)(*args, **kwargs)
		return doCall

df = RandomResponder.which()
print(df)

