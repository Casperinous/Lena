class Dummy:

	@staticmethod
	def dum():
		return 3*4

class A(object):

	def __init__(self, val):

		self.test1 = val
		self.callback = Dummy.dum



class B(A):

	def __init__(self):

		A.__init__(self,3)
		self.test2 = 2
		print self.test1



class C(B):

	def __init__(self):

		B.__init__(self)
		print self.test1
		print self.callback()



c = C()
