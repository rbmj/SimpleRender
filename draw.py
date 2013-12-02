import sys
import os
import importlib
import matrices

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

import filetypes
handlers = {}
for m in filetypes.__all__:
	importlib.import_module('filetypes.'+m).register(handlers)

import Mesh
global mesh
mesh = None

scaleFactor = 1.05
rotateFactor = 0.05

# Gets called by glutMainLoop() many times per second
def doIdle():    
	pass    # Remove if we actually use this function
	
def doKeyboard(*args):
	global cameraMatrix
	if args[0] == '+':
		cameraMatrix.scale(1/scaleFactor)
	elif args[0] == '-':
		cameraMatrix.scale(scaleFactor)
	else:
		return
	doRedraw()
	
def doSpecial(*args):
	global cameraMatrix
	if args[0] == GLUT_KEY_UP:
		cameraMatrix = cameraMatrix*matrices.rotateX(-rotateFactor) #up
	if args[0] == GLUT_KEY_DOWN:
		cameraMatrix = cameraMatrix*matrices.rotateX(rotateFactor) #down
	if args[0] == GLUT_KEY_LEFT:
		cameraMatrix = cameraMatrix*matrices.rotateY(-rotateFactor) #left
	if args[0] == GLUT_KEY_RIGHT:
		cameraMatrix = matrices.rotateY(rotateFactor)*cameraMatrix #right
	doRedraw()

# Called by glutMainLoop() when window is resized
def doReshape(width, height):
	global cameraMatrix
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glViewport(0,0,width,height)
	gluPerspective(45.0, ((float)(width))/height, .1, 200)
	
	doCamera()

def doCamera():
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	pos = matrices.Vector4d(0, 3, 10, 1)*cameraMatrix
	lookAt = matrices.Vector4d(0, 0, 0, 1)*cameraMatrix
	direction = matrices.Vector4d(0, 1, 0, 1)*cameraMatrix
	direction.makeUnit()

	gluLookAt(*(pos.list()[:-1] + lookAt.list()[:-1] + direction.list()[:-1]))

# Called by glutMainLoop() when screen needs to be redrawn
def doRedraw():
	doCamera()
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (.25, .25, .25, 1.0))
	glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, .5))
	glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, (128.0, ))
	glMatrixMode(GL_MODELVIEW)
	
	mesh.draw()
	
	glutSwapBuffers()  # Draws the new image to the screen if using double buffers

if __name__ == '__main__':
	global cameraMatrix
	cameraMatrix = matrices.getIdentity4x4()
	mesh = handlers[os.path.splitext(sys.argv[1])[1][1:]](sys.argv[1])
	
	# Basic initialization - the same for most apps
	glutInit([])
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(640,480)
	glutCreateWindow("Simple OpenGL Renderer")
	glEnable(GL_DEPTH_TEST)      # Ensure farthest polygons render first
	glEnable(GL_NORMALIZE)       # Prevents scale from affecting color
	glClearColor(0.1, 0.1, 0.2, 0.0) # Color to apply for glClear()

	# Set up two lights
	glEnable(GL_LIGHTING)
	BRIGHT4f = (1.0, 1.0, 1.0, 1.0)  # Color for Bright light
	DIM4f = (.2, .2, .2, 1.0)        # Color for Dim light
	glLightfv(GL_LIGHT0, GL_AMBIENT, BRIGHT4f)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, BRIGHT4f)
	glLightfv(GL_LIGHT0, GL_POSITION, (10, 10, 10, 0))
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT1, GL_AMBIENT, DIM4f)
	glLightfv(GL_LIGHT1, GL_DIFFUSE, DIM4f)
	glLightfv(GL_LIGHT1, GL_POSITION, (-10, 10, -10, 0))
	glEnable(GL_LIGHT1)

	# Callback functions for loop
	glutDisplayFunc(doRedraw)        # Runs when the screen must be redrawn
	glutIdleFunc(doIdle)             # Runs in a loop when the screen is not redrawn
	glutReshapeFunc(doReshape)       # Runs when the window is resized
	glutSpecialFunc(doSpecial)       # Runs when directional key is pressed
	glutKeyboardFunc(doKeyboard)     # Runs when key is pressed

	# Runs the GUI - never exits
	# Repeatedly calls doRedraw(), doIdle(), & doReshape()
	glutMainLoop()

