======================
Simple OpenGL Renderer
======================

This is a very basic OpenGL renderer written in Python.

It currently requires PyOpenGL and Python 2.7+.  It should
be Python 3 compatible, but PyOpenGL currently does not work
with Python 3 so Python 2 is required.

Usage
======================

Current usage is as follows:
$ python draw.py test.ply

Once the OpenGL window has appeared, the controls for the window are:
 - +/- zooms in/out
 - Arrow keys rotates
 - Shift+Arrow keys translates

The only supported file format right now is the Stanford Polygon Format.
The file's extension must be .ply.  It must contain two element types,
'vertex' and 'face'.  vertex must at minimum have properties 'x', 'y',
and 'z', and face must have a 'vertex_indices' property of type list.
This matches the nomenclature used by blender's ply export script.

Extension
======================

Adding support for new file formats is relatively easy.  Add a file
in the filetypes directory.  This must contain a special function
called 'register' taking one argument.  Its argument will be a
dictionary mapping file extensions to parsing functions.  These
parsing functions take a file name (string) as an argument and
return a Mesh object.  As an example:

.. code:: python
	
	import Mesh
	
	def parse_myformat(fname):
		m = Mesh()
		for line in open(fname, 'r'):
			pass #parse file
		return m
	
	# The name of this function must be 'register':
	def register(handlers):
		handlers['myformat_extension'] = parse_myformat

The Mesh class has two significant methods.  addVertex() adds a vertex
to the Mesh (see the Vertex class - it's fairly simple).  addFace() adds
a face to the Mesh (see the Face class - again, simple).  Note that faces'
vertex members are currently indices into the array of vertices stored by
the Mesh object.  So a face (0, 1, 2, 3) is a quad defined by the first
four vertices added to the mesh.

TODO
======================

The code has practically no error handling.  Everything works if the
filename exists and parses correctly.  However, it does not fail
gracefully.

The Mesh object should create a vertex buffer (at least of quads and
tris) in order to optimize drawing the object.  This is unimplemented
right now because it's a performance improvement, not a correctness
improvement.

Lighting should be configurable.

The ply parser is not currently robust at dealing with attribute names
that are not the same as those expected (i.e. those output by blender's
export script).  This should be easy to deal with, but one needs to know
what other commonly-used attribute names are 'out there' in the wild.
If the parser encounters unknown attributes, it should give the user
the opportunity to define which slots these correspond with at runtime.

It would be nice to have a nice wxPython GUI, while preserving the ability
to render from the command line.  Perhaps the command-line could become
a non-interactive renderer?