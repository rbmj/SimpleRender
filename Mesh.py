from OpenGL.GL import *

class Vertex(object):
	def __init__(self):
		self._x = 0.0
		self._y = 0.0
		self._z = 0.0
		self._nx = 0.0
		self._ny = 0.0
		self._nz = 0.0
		self._s = 0.0
		self._t = 0.0
		self._hasCoords = False
		self._hasNormals = False
		self._hasST = False
	def setX(self, x):
		self._hasCoords = True
		self._x = x
	def setY(self, y):
		self._hasCoords = True
		self._y = y
	def setZ(self, z):
		self._hasCoords = True
		self._z = z
	def coords(self):
		return (self._x, self._y, self._z)
	def setNX(self, nx):
		self._hasNormal = True
		self._nx = nx
	def setNY(self, ny):
		self._hasNormal = True
		self._ny = ny
	def setNZ(self, nz):
		self._hasNormal = True
		self._nz = nz
	def normal(self):
		return (self._nx, self._ny, self._nz)
	def setS(self, s):
		self._hasST = True
		self._s = s
	def setT(self, t):
		self._hasST = True
		self._t = t
	def stcoords(self):
		return (self._s, self._t)
	def hasCoords(self):
		return self._hasCoords
	def hasNormal(self):
		return self._hasNormal
	def hasST(self):
		return self._hasST
		
class Face(object):
	def __init__(self):
		self._vertices = []
	def set(self, l):
		self._vertices = l
	def vertices(self):
		return self._vertices
		
class Mesh(object):
	def __init__(self):
		self.vertices = []
		self.faces = []
	def addVertex(self, v):
		self.vertices.append(v)
	def getVertex(self, vi):
		return self.vertices[vi]
	def addFace(self, f):
		self.faces.append(f)
	def draw(self):
		mode = None
		for face in self.faces:
			numvertices = len(face.vertices())
			if numvertices == 3 and mode != GL_TRIANGLES:
				if mode:
					glEnd()
				glBegin(GL_TRIANGLES)
				mode = GL_TRIANGLES
			elif numvertices == 4 and mode != GL_QUADS:
				if mode:
					glEnd()
				glBegin(GL_QUADS)
				mode = GL_QUADS
			elif numvertices > 4:
				if mode:
					glEnd()
				glBegin(GL_POLYGON)
				mode = GL_POLYGON
			elif numvertices < 3:
				raise RuntimeError('Face has <3 vertices')
			for vertex in [self.getVertex(i) for i in face.vertices()]:
				if vertex.hasNormal():
					glNormal3f(*(vertex.normal()))
				glVertex3f(*(vertex.coords()))
			if mode == GL_POLYGON:
				glEnd()
				mode = None
		if mode:
			glEnd()