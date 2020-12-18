class animal ():
	legs = 4;                       """Private DataMember """
	_ears = 2;			 """Private DataMember """
	def get_legs (self):
		return self.legs
	def set_legs (self, a):
		self.legs = a
	def get_ears (self):
		return self.ears
	def set_ears (self, a):
		self.ears = a
class animal_extension (animal):
	_nose = 1;			 """Private DataMember """
	def get_nose (self):
		return self.nose;
	def set_nose (self, a):
		self.nose = a;
dog = animal_extension ()			
mouse = animal_extension ()
cow = animal_extension ()
buffalo = animal_extension ()
cat = animal_extension ()
elephant = animal_extension ()
lion = animal_extension ()
tiger = animal_extension ()
goat = animal_extension ()
giraffe = animal_extension ()
print ("Dog	", dog.get_legs())
print ("Mouse	", mouse.get_legs())
print ("Cow	", cow.get_legs())
print ("Buffalo	", buffalo.get_legs())
print ("Cat	", cat.get_legs())
print ("Elephant", elephant.get_legs())
print ("Lion	", lion.get_legs())
print ("Tiger	", tiger.get_legs())
print ("Goat	", goat.get_legs())
print ("Giraffe	", giraffe.get_legs())

"""While abstracting only the Public members are get abstracted and Private members are not """
