try:
	from Qt import QtCore, QtWidgets
except ModuleNotFoundError:
	from PySide2 import QtCore, QtWidgets

import shiboken2

from maya import OpenMayaUI, OpenMaya, OpenMayaAnim, cmds
import maya.api.OpenMaya as OpenMaya2


#
#
# GUI
#
#

def getMayaWindow():
	try:
		ptr     = OpenMayaUI.MQtUtil.mainWindow()
		return shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)
	except :
		return None


class RbfRetargeterGUI( QtWidgets.QMainWindow ):

	def __init__(self, parent=getMayaWindow() ):
		#super(DeformationToSkinningGUI, self).__init__(parent)
		QtWidgets.QMainWindow.__init__(  self, parent )

		self.setWindowTitle("RBF Retargeter")

		# UI elements
		central_Widget		= QtWidgets.QWidget() ;self.setCentralWidget( central_Widget )
		central_Layout		= QtWidgets.QVBoxLayout( central_Widget )


		gb3 	= QtWidgets.QGroupBox()  ;central_Layout.addWidget( gb3 )
		gb3.setTitle('Source')
		v3		= QtWidgets.QVBoxLayout( gb3 )
		v3_h1	= QtWidgets.QHBoxLayout( )  ;v3.addLayout( v3_h1 )
		self.src_LE 	= QtWidgets.QLineEdit()    ;v3_h1.addWidget( self.src_LE )
		self.src_PB     = QtWidgets.QPushButton()  ;v3_h1.addWidget( self.src_PB )
		self.src_PB.setText('<<')

		gb2 	= QtWidgets.QGroupBox()  ;central_Layout.addWidget( gb2 )
		gb2.setTitle('Source Shapes')
		v2		= QtWidgets.QVBoxLayout( gb2 )
		v2_h1	= QtWidgets.QHBoxLayout( )  ;v2.addLayout( v2_h1 )
		self.srcShapes_LW   = QtWidgets.QListWidget()  ;v2_h1.addWidget( self.srcShapes_LW )
		self.srcShapes_PB   = QtWidgets.QPushButton()  ;v2_h1.addWidget( self.srcShapes_PB )
		self.srcShapes_PB.setText('<<')

		gb4 	= QtWidgets.QGroupBox()  ;central_Layout.addWidget( gb4 )
		gb4.setTitle('Target')
		v4		= QtWidgets.QVBoxLayout( gb4 )
		v4_h1	= QtWidgets.QHBoxLayout( )  ;v4.addLayout( v4_h1 )
		self.tgts_LW   = QtWidgets.QListWidget()  ;v4_h1.addWidget( self.tgts_LW )
		self.tgts_PB   = QtWidgets.QPushButton()  ;v4_h1.addWidget( self.tgts_PB )
		self.tgts_PB.setText('<<')

		gb1 	= QtWidgets.QGroupBox()  ;central_Layout.addWidget( gb1 )
		gb1.setTitle('Other')
		v1		= QtWidgets.QVBoxLayout( gb1 )

		v1_h1	= QtWidgets.QHBoxLayout( )  ;v1.addLayout( v1_h1 )
		label1 		    = QtWidgets.QLabel() ;v1_h1.addWidget(label1)
		label1.setText('Shader From')
		self.shader_CB  = QtWidgets.QComboBox()  ;v1_h1.addWidget( self.shader_CB )
		self.shader_CB.addItem( 'Target' )
		self.shader_CB.addItem( 'Shapes' )
		self.shader_CB.setCurrentIndex( 0 )

		v1_h2	= QtWidgets.QHBoxLayout( )  ;v1.addLayout( v1_h2 )
		self.sphere_CB  = QtWidgets.QCheckBox() ;v1_h2.addWidget(self.sphere_CB)
		self.sphere_CB.setText( 'Volumic Sphere' )
		self.sphere_CB.setChecked(True)

		v1_h3	= QtWidgets.QHBoxLayout( )  ;v1.addLayout( v1_h3 )
		self.fromVertexIds_LE 	= QtWidgets.QLineEdit() ;v1_h3.addWidget( self.fromVertexIds_LE )
		self.fromVertexIds_LE.setEnabled( False )
		self.fromGetIds_PB     = QtWidgets.QPushButton()  ;v1_h3.addWidget( self.fromGetIds_PB )
		self.fromGetIds_PB.setText( '<<' )

		self.build_PB  = QtWidgets.QPushButton()  ;central_Layout.addWidget( self.build_PB )
		self.build_PB.setText( 'Build Shapes' )
		self.build_PB.setStyleSheet( 'background-color: rgb(60,60,60);border: 2px solid rgb(0,0,0);border-radius: 3px;font: 13pt courier;color : rgb(255,77,133);' )

		# aesthetic
		central_Layout.setContentsMargins( 9,8,9,5 )
		v3.setContentsMargins( 0,0,0,0 )
		v3_h1.setContentsMargins( 0,0,0,0 )
		v2.setContentsMargins( 0,0,0,0 )
		v2_h1.setContentsMargins( 0,0,0,0 )
		v4.setContentsMargins( 0,0,0,0 )
		v4_h1.setContentsMargins( 0,0,0,0 )
		v1.setContentsMargins(10,5,0,0 )
		v1_h1.setContentsMargins( 0,0,0,0 )
		v1_h2.setContentsMargins( 0,0,0,0 )
		v1_h3.setContentsMargins( 0,0,0,0 )
		v3.setSpacing( 0 )
		v3_h1.setSpacing( 0 )
		v2.setSpacing( 0 )
		v2_h1.setSpacing( 0 )
		v4.setSpacing( 0 )
		v4_h1.setSpacing( 0 )
		v1.setSpacing( 5 )
		v1_h1.setSpacing( 0 )
		v1_h2.setSpacing( 0 )
		v1_h3.setSpacing( 0 )

		# functions
		self.src_PB.clicked.connect( self.set_source )
		self.srcShapes_PB.clicked.connect( self.set_sourceShapes )
		self.tgts_PB.clicked.connect( self.set_targets )
		self.build_PB.clicked.connect( self.buildShapes )
		self.fromGetIds_PB.clicked.connect( self.set_src_vertexIds )

		# empty all   because  Qline_edits are stored  with the  self.loadSettings()
		# but NOT the  QlistWidget   so I prefer to have all empty
		self.src_LE.setText('')
		self.tgts_LW.clear()
		self.srcShapes_LW.clear()

		self.fromVertexIds_LE.setText('Solver Vertices')

		self.setGeometry( QtCore.QRect(579, 749, 199, 515) )

	def mesh_from_transform(self, item ):

		if cmds.nodeType(item)=='mesh':
			return item
		# else
		mesh    = cmds.listRelatives(item, s=True, pa=True, type="mesh"  ) # f=fullPath

		if mesh :
			return mesh[0]
		else:
			return None

	def set_source(self):

		sel = cmds.ls(sl=True, type=('transform','mesh') )
		if not sel :
			self.src_LE.setText('')
			OpenMaya2.MGlobal.displayInfo('Please select a mesh')
		else :
			mesh   = self.mesh_from_transform( sel[0] )

			if not mesh :
				self.src_LE.setText('')
				OpenMaya2.MGlobal.displayInfo('Please select a mesh')
			else :
				self.src_LE.setText(mesh)

	def set_targets(self):

		sel = cmds.ls(sl=True, type=('transform','mesh') )

		if sel :
			meshes  = []
			for item in sel :
				mesh   = self.mesh_from_transform( item )
				if not mesh :
					self.tgts_LW.clear()
					OpenMaya2.MGlobal.displayInfo('Please select meshes')
					return
				meshes.append( mesh )

			self.tgts_LW.clear()
			self.tgts_LW.addItems( meshes  )
		else :
			self.tgts_LW.clear()

	def set_sourceShapes(self):

		sel = cmds.ls(sl=True, type=('transform','mesh') )

		if sel :
			meshes  = []

			for item in sel :
				mesh   = self.mesh_from_transform( item )

				if not mesh :
					self.srcShapes_LW.clear()
					OpenMaya2.MGlobal.displayInfo('Please select meshes')
					return
				meshes.append( mesh )

			self.srcShapes_LW.clear()
			self.srcShapes_LW.addItems( meshes  )
		else :
			self.srcShapes_LW.clear()

	def set_src_vertexIds(self):

		sel = cmds.ls( "*.vtx[*]", sl=True, fl=True)

		if not sel :
			self.fromVertexIds_LE.setText('Solver Vertices')
			return

		# else
		vIds_str    = ''

		for i,item in enumerate(sel) :
			tmp         = item.split('[') [-1]
			vIds_str    += tmp.split(']') [0]

			if i!=len(sel)-1:
				vIds_str    += ', '

		self.fromVertexIds_LE.setText(vIds_str)

	def get_srcVertexIds(self ):

		ids_str     = self.fromVertexIds_LE.text()

		if ids_str == 'Solver Vertices':
			return []


		input_ids   = eval( '['+ids_str+']' )
		if len(input_ids)==0 :
			return []

		return input_ids

	def buildShapes(self):

		cmds.undoInfo(openChunk=True)

		# get
		source          = self.src_LE.text()
		targets         = [self.tgts_LW.item(i).text() for i in range(self.tgts_LW.count())]
		sourceShapes    = [self.srcShapes_LW.item(i).text() for i in range(self.srcShapes_LW.count())]

		if (not source) or (not targets) or (not sourceShapes):
			OpenMaya2.MGlobal.displayInfo('Please fill all inputs : source mesh, source shape(s), target(s) mesh')
			return

		if source in sourceShapes:
			OpenMaya2.MGlobal.displayInfo("Source can't be a SourceShape at the same time !")
			return
		for target in targets :
			if target in sourceShapes :
				OpenMaya2.MGlobal.displayInfo("Target can't be a SourceShape at the same time !")
				return
			if source==target :
				OpenMaya2.MGlobal.displayInfo("Source can't be a Target at the same time !")
				return

		# build or not  the Volumic/Static Sphere  +  get vertexIds used in the command
		useSphere   = self.sphere_CB.isChecked()
		from_ids    = self.get_srcVertexIds(  )

		if 0< len(from_ids) <3 :
			OpenMaya2.MGlobal.displayInfo('Solver Vertices minimum is 3')
			return

		# launch custom command for each target
		# cmds.loadPlugin( "rbfRetargeter", quiet=True )

		for target in targets :

			newTRs      = cmds.retargetShapes( source, sourceShapes, target, useSphere, from_ids )
			newShapes   = [cmds.listRelatives(item, s=True)[0]  for item in newTRs]

			# copy shaders from target or shapes
			shaderMode  = self.shader_CB.currentIndex()
			if shaderMode==0 :      transfer_to_multiple( target, newShapes )
			elif shaderMode==1 :    transfer_one_to_one( sourceShapes, newShapes )

		cmds.undoInfo(closeChunk=True)


def showUI():
	win     = RbfRetargeterGUI()
	win.show()
	return win

#
#
# Utilities
#
#


def get_shadingEngines( item ):
	'''from a shader or a shape '''

	outputs    = cmds.listConnections( item, s=False, d=True, type="shadingEngine" )

	if outputs :
		return list( frozenset(outputs))
	else :
		#OpenMaya2.MGlobal.displayInfo('No ShadingEngine connected to '+item)
		return []

def assigned_from_shadingEngine( shadingEngine ):
	'''get shapes and compounds assigned by this shading engine'''

	assigned	= cmds.sets( shadingEngine, q=True)
	# assigned	= cmds.ls( assigned, fl=True )

	return assigned

def assignedList_from_shape( shape  ):
	'''get shapes and compounds assigned on this shape'''

	shEngines	    = get_shadingEngines( shape )
	assigned_list, assigned_engines   = [], []

	transform = cmds.listRelatives(shape, p=True)[0]
	for shEngine in shEngines:
		allObjs = assigned_from_shadingEngine( shEngine )
		objs = [obj for obj in allObjs if obj.partition('.')[0] in [shape, transform]]
		if not objs:
			continue

		assigned_list.append( objs )
		assigned_engines.append( shEngine )

	return assigned_list, assigned_engines

def assign( onThat, shEngine ):
	'''onThat is a list of shapes and compounds
	This command can
	- assign onThat  and  create a new shader with shaderName and shaderType
	- or just assign  using existing shaderName  ( so ignoring shaderType )'''

	"""
	if cmds.objExists( shaderName ):
		shaderNode      = shaderName
		shEngine        = get_shadingEngines( shaderNode )[0]

	else :
		# createNew
		# connection for Maya shaders
		cmds.connectAttr( shaderNode+'.outColor', shEngine+'.surfaceShader')

		# for mentalRay shaders
		#...
	"""
	# assign
	#for item in onThat :
	#	cmds.sets( item, fe=shEngine  )
	cmds.sets( onThat, fe=shEngine  )

def transfer_multiple( assigned_list, shEngines ):

	for onThat, shEngine in zip(assigned_list, shEngines) :

		assign( onThat, shEngine )


def compress( componentList, vertex=False, edge=False, face=False ):
	'''Invert ls(fl=True) effect,  return ['mesh.f[0:1]', 'mesh.f[3]'] '''

	if vertex :
		return cmds.polyListComponentConversion( componentList, fv=True, tv=True )
	elif edge :
		return cmds.polyListComponentConversion( componentList, fe=True, te=True )
	elif face :
		return cmds.polyListComponentConversion( componentList, ff=True, tf=True )
	else :
		cmds.warning('No flag specified ! vertex ? edge ? face ?')
		return

def uncompress( componentList ):
	return cmds.ls( componentList, fl=True )

def get_node( plug ):

	return plug.split('.')[0]

def get_shape_from_component( component ):
	'''Because a component can be transform.f[0] or shape.f[0] I need a function to deal with that '''

	shape   = get_node( component )

	if cmds.nodeType(shape) in ('transform','joint'):
		shape   = cmds.listRelatives(shape, s=True, path=True )[0]  # -path give fullPath only if doubleNamed

	return str(shape)

def get_componentId( component ):
	'''component 'pSphere3.vtx[184]' or 'nurbsSphere1.cv[32][11]'  etc... so return a list of ids'''

	component_dim   = component.count('[')

	ids     = [int( component.split('[')[1+ii].split(']')[0] )  for ii in range(component_dim) ]

	return ids

def shape_componentList_to_dict( componentList ):
	'''from []   return {'pSphereShape3': [[0], [1], [2]], 'nurbs1:[[0,0],[0,1],[0,2]]' } '''


	ids_per_shape   = {}


	for component in componentList :

		#
		shape   = get_shape_from_component( component )

		if shape not in ids_per_shape :
			ids_per_shape[shape]    = []

		#
		vId     = get_componentId( component )

		ids_per_shape[shape].append( vId )


	return ids_per_shape

def componentList_to_dict(  componentList  ):
	'''Use same function than lib.shape,
	Ignore component type.
	return {shape1:[0,5,3,2], shape2:[10,11], ...}'''

	componentList 	= uncompress( componentList )

	ids_per_shape   = shape_componentList_to_dict( componentList )


	# libShape function return n-dimension component
	# mesh components are 1-dim
	ids_per_mesh    = {}

	for mesh in ids_per_shape.keys() :

		mesh_nIds   = ids_per_shape[mesh]
		mesh_1Ids   = [nId[0] for nId in mesh_nIds]

		ids_per_mesh[mesh]  = mesh_1Ids

	return ids_per_mesh

def dict_to_componentList( dic, vertex=False, edge=False, face=False ):

	cType 	= 0
	if edge :cType=1
	if face :cType=2
	str 	= ['vtx','e','f'][cType]

	componentList 	= []
	for key in dic.keys():
		for value in dic[key]:
			componentList.append( key+'.%s[%s]'%(str,value) )

	return componentList



def transfer_to( fromShape, toShape, cloneNum=0,  verbose=False):
	'''must have same topo.
	If cloneNum = >=2  force assign to faces*cloneNum even if the faces dont exist.
	if cloneNum == -1  try to assign to the exact number of clone.
	if cloneNum == 0 or 1  dont do anything.
	'''

	# secu
	if (not cmds.nodeType(fromShape)=='mesh') or (not cmds.nodeType(toShape)=='mesh'):
		OpenMaya2.MGlobal.displayError('Inputs must be mesh shapes : '+fromShape+' '+toShape)
		return None


	#
	fromTr      = cmds.listRelatives( fromShape, p=True )[0]

	assigned_list, shEngines    = assignedList_from_shape( fromShape )

	# replace the name of fromShape by toShape
	newAssign_list  = []

	for i,assigned in enumerate(assigned_list) :

		newAssign   = []

		for j,item in enumerate(assigned) :


			# the shape
			if assigned_list[i][j] == fromShape :

				newAssign.append( toShape )


			# a face
			elif ".f[" in assigned_list[i][j] :

				if fromTr in assigned_list[i][j] :
					newAssign.append(  assigned_list[i][j].replace( fromTr, toShape ) )

				elif fromShape in assigned_list[i][j] :
					newAssign.append(  assigned_list[i][j].replace( fromShape, toShape ) )
			'''
				else :
					print "ignored : "+assigned_list[i][j]
			else :
				print "ignored : "+assigned_list[i][j]
			'''

		newAssign_list.append( newAssign )


	# assign to cloned geometry (currently used in cloneToQuad function )
	numShader   = len( shEngines )

	if (numShader>1)   and   (cloneNum not in (0,1)) :   # can be -1

		fromShape_F 	= libMesh.get_numFace( fromShape )
		if cloneNum==-1 :   toShape_F = libMesh.get_numFace( toShape )
		else :              toShape_F = fromShape_F * cloneNum

		if toShape_F % fromShape_F != 0 :
			OpenMaya2.MGlobal.displayWarning('ToShape is not a clean clonedMesh, assign anyway.')

		for aa,assigned in enumerate(newAssign_list) :
			comp_dict 	= componentList_to_dict(  assigned  )
			key         = comp_dict.keys()[0]
			fIds        = comp_dict.values()[0]
			new_fIds    = list(fIds)
			for ff in range( 1, toShape_F ):
				for fId in fIds :
					new_fIds.append( fromShape_F * ff + fId )
			new_dict    = {key:new_fIds }
			newAssign_list[aa]  = dict_to_componentList( new_dict, face=True  )
			newAssign_list[aa]  = compress( newAssign_list[aa], face=True )


	# assign
	transfer_multiple( newAssign_list, shEngines )
	if verbose:
		OpenMaya2.MGlobal.displayInfo('Shading.transfer_to OK from '+fromShape+' to '+toShape)


def transfer_to_multiple( fromShape, toShapes ):

	for toShape in  toShapes :

		transfer_to( fromShape, toShape)


def transfer_one_to_one( fromShapes, toShapes ):

	for fromShape,toShape in zip(fromShapes, toShapes) :

		transfer_to( fromShape, toShape)
