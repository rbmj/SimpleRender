#!/usr/bin/env python

import math

# Compares two values to see if they are equal within an acceptable error
def equals(a, b):
	DELTA = .001
	if(abs(a-b)<DELTA):
		return True
	return False

class Vector4d:
	def __init__(self, x, y, z, w):
		self.val = [x, y, z, w]

	def __getitem__(self, i):
		return self.val[i]

	def __str__(self):
		return "<%7.3f, %7.3f, %7.3f, %7.3f>" % (self[0], self[1], self[2], self[3])

	def __setitem__(self, i, x):
		self.val[i] = x
		
	def list(self):
		return self.val
	
	def magnitude(self):
		return math.sqrt(self[0]*self[0] + self[1]*self[1] + self[2]*self[2] + self[3]*self[3])

	def scale(self, factor):
		for i in range(4):
			self.val[i] = self.val[i]*factor

	def makeUnit(self):
		if not self.isZero():
			m = self.magnitude()
			for i in range(4):
				self.val[i] /= m

	def isZero(self):
		for i in range(4):
			if not equals(self.val[i], 0.0):
				return False
		return True

	def __mul__(self, m):
		# this is wrong - matrix should be on the left...
		m = m.transpose()
		return Vector4d(*[ dot(m[i], self) for i in range(4) ])

	def __add__(self, v):
		return Vector4d(*[ self[i] + v[i] for i in range(4) ])

	def __iadd__(self, v):
		for i in range(4):
			self[i] += v[i]
		return self

	def __sub__(self, v):
		return Vector4d(*[ self[i] - v[i] for i in range(4) ])
	
	def __isub__(self, v):
		for i in range(4):
			self[i] -= v[i]
		return self

	def __eq__(self, v):
		for i in range(4):
			if not equals(self[i], v[i]):
				return False
		return True

	def __ne__(self, v):
		return not (self == v)
	
	def __len__(self):
		return 4



def dot(u, v):
	if len(u) != len(v):
		raise RuntimeError('Vectors do not have same dimension')
	return sum([u[i]*v[i] for i in range(len(u))])

def proj(u, v):
	return v.scale(dot(u, v)/dot(v, v))
	
class Matrix4x4:
	def __init__(self, *args):
		if len(args) == 4:
			self._createFromColumns(*args)
		if len(args) == 16:
			self._createFromElements(*args)

	def _createFromElements(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p):
		self.val = [ Vector4d(a, e, i, m),
					 Vector4d(b, f, j, n),
					 Vector4d(c, g, k, o),
					 Vector4d(d, h, l, p) ]

	def _createFromColumns(self, a, b, c, d):
		self.val = [a, b, c, d]

	def __getitem__(self, i):
		return self.val[i]

	def __setitem__(self, i, x):
		self.val[i] = x

	def __str__(self):
		s = ""
		for i in range(4):
			s += "|%7.3f, %7.3f, %7.3f, %7.3f|\n" % (self[0][i],
											         self[1][i],
											         self[2][i],
											         self[3][i])
		return s

	def __eq__(self, m):
		for i in range(4):
			if self[i] != m[i]:
				return False
		return True

	def __ne__(self, m):
		return not (self == m)
	
	def scale(self, s):
		for i in range(4):
			self[i].scale(s)
		
	def transpose(self):
		return Matrix4x4(*[ self[i][j]
							for i in range(4) for j in range(4) ])

	def copy(self):
		return Matrix4x4(*[ self[j][i]
							for i in range(4) for j in range(4) ])

	# def det(self):
		# return ( self[0][0]*self[1][1]*self[2][2] -
				 # self[0][0]*self[1][2]*self[2][1] +
				 # self[1][0]*self[0][1]*self[2][2] -
				 # self[1][0]*self[0][2]*self[2][1] +
				 # self[2][0]*self[0][1]*self[1][2] -
				 # self[2][0]*self[0][2]*self[1][1] )
			
	def __mul__(self, n):
		m = self.transpose()
		return Matrix4x4(*[ dot(m[i], n[j])
							for i in range(4) for j in range(4) ])

	def orthogonalize(self):
		m = self.copy()
		for i in range(4):
			for j in range(i):
				m[i] -= proj(m[i], m[j])
		return m

	def orthonormalize(self):
		m = self.orthogonalize()
		for i in range(4):
			m[i].makeUnit()
		return m

	def isOrthogonal(self):
		return (self * self.transpose()) == getIdentity4x4()

def getIdentity4x4():
	return Matrix4x4(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)

def rotateX(theta):
	s = math.sin(theta)
	c = math.cos(theta)
	return Matrix4x4(1, 0, 0, 0,
					 0, c,-s, 0,
					 0, s, c, 0,
					 0, 0, 0, 1)

def rotateY(theta):
	s = math.sin(theta)
	c = math.cos(theta)
	return Matrix4x4(c , 0, s, 0,
				     0 , 1, 0, 0,
					 -s, 0, c, 0,
					 0 , 0, 0, 1)

def rotateZ(theta):
	s = math.sin(theta)
	c = math.cos(theta)
	return Matrix4x4(c,-s, 0, 0,
					 s, c, 0, 0,
					 0, 0, 1, 0,
					 0, 0, 0, 1)

def translate(x, y, z):
	return Matrix4x4(1, 0, 0, x,
					 0, 1, 0, y,
					 0, 0, 1, z,
					 0, 0, 0, 1)

def scale(x, y, z):
	return Matrix4x4(x, 0, 0, 0,
					 0, y, 0, 0,
					 0, 0, z, 0,
					 0, 0, 0, 1)
					   
def printBreak():
	print ("-------------------")
