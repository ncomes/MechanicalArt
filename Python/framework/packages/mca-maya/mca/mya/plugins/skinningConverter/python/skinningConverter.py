import random, math

try:
    from Qt import QtCore, QtWidgets, QtGui
except ModuleNotFoundError:
    from PySide2 import QtCore, QtWidgets, QtGui

import shiboken2

from maya import OpenMayaUI, OpenMaya, OpenMayaAnim, cmds, mel


epsilon     = 1e-7

#
#
# GUI
#
#

def get_maya_window():
    """
    Returns the QWidget of mayas main_window
    """
    ptr     = OpenMayaUI.MQtUtil.mainWindow()
    #return QtCompat.wrapInstance(long(ptr), QtWidgets.QWidget)
    return shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)


class DeformationToSkinningGUI( QtWidgets.QMainWindow ):
    
    def __init__(self, parent=get_maya_window() ):
        QtWidgets.QMainWindow.__init__(  self, parent )
    
        self.setWindowTitle("Deformation to Skinning")
        
        central_Widget        = QtWidgets.QWidget() ;self.setCentralWidget( central_Widget )
        central_Layout        = QtWidgets.QVBoxLayout( central_Widget )
        
        # 4 things, 3 groupBox + 1 button
        # groupBox 1
        gb1         = QtWidgets.QGroupBox()  ;central_Layout.addWidget( gb1 )
        
        gb1_v1        = QtWidgets.QVBoxLayout( gb1 )
        gb1_h1        = QtWidgets.QHBoxLayout( )  ;gb1_v1.addLayout( gb1_h1 )
        
        gb1_h1_left = QtWidgets.QVBoxLayout()  ;gb1_h1.addLayout( gb1_h1_left )
        
        label1         = QtWidgets.QLabel() ;gb1_h1_left.addWidget(label1)
        label1.setText('Max Influence')
        label2         = QtWidgets.QLabel() ;gb1_h1_left.addWidget(label2)
        label2.setText('Frame Range')
        
        
        gb1_h1_right    = QtWidgets.QVBoxLayout()  ;gb1_h1.addLayout( gb1_h1_right )
        
        self.maxInf_SB     = QtWidgets.QSpinBox()  ;gb1_h1_right.addWidget( self.maxInf_SB )
        
        gb1_h1_right_h        = QtWidgets.QHBoxLayout()  ;gb1_h1_right.addLayout( gb1_h1_right_h )
        self.startFrame_LE     = QtWidgets.QLineEdit() ;gb1_h1_right_h.addWidget( self.startFrame_LE )
        self.endFrame_LE     = QtWidgets.QLineEdit() ;gb1_h1_right_h.addWidget( self.endFrame_LE )
        
        self.selectedJoints_CB    = QtWidgets.QCheckBox()  ;gb1_v1.addWidget( self.selectedJoints_CB )
        self.selectedJoints_CB.setText( 'Selected Joints' )
        
        # groupBox 2
        self.gb2         = QtWidgets.QGroupBox()  ;central_Layout.addWidget( self.gb2 )
        
        gb2_v1        = QtWidgets.QVBoxLayout( self.gb2 )
        gb2_h1        = QtWidgets.QHBoxLayout( )  ;gb2_v1.addLayout( gb2_h1 )
        
        gb2_h1_left = QtWidgets.QVBoxLayout()  ;gb2_h1.addLayout( gb2_h1_left )
        
        label3         = QtWidgets.QLabel() ;gb2_h1_left.addWidget(label3)
        label3.setText('Num Joint')
        label4         = QtWidgets.QLabel() ;gb2_h1_left.addWidget(label4)
        label4.setText('Joint Type')
        
        gb2_h1_right    = QtWidgets.QVBoxLayout()  ;gb2_h1.addLayout( gb2_h1_right )
        
        self.numJoint_SB     = QtWidgets.QSpinBox()  ;gb2_h1_right.addWidget( self.numJoint_SB )
        self.rigid_CB       = QtWidgets.QComboBox()  ;gb2_h1_right.addWidget( self.rigid_CB )
        
        self.makeRoot_CB    = QtWidgets.QCheckBox()  ;gb2_v1.addWidget( self.makeRoot_CB )
        self.makeRoot_CB.setText( 'Root' )
        
        # groupBox 3
        self.gb3         = QtWidgets.QGroupBox()  ;central_Layout.addWidget( self.gb3 )
        
        gb3_v1        = QtWidgets.QVBoxLayout( self.gb3 )
        gb3_h1        = QtWidgets.QHBoxLayout( )  ;gb3_v1.addLayout( gb3_h1 )
        
        gb3_h1_left = QtWidgets.QVBoxLayout()  ;gb3_h1.addLayout( gb3_h1_left )
        
        label5         = QtWidgets.QLabel() ;gb3_h1_left.addWidget(label5)
        label5.setText('MaxIteration')
        self.stopAt_CB  = QtWidgets.QCheckBox() ;gb3_h1_left.addWidget(self.stopAt_CB)
        self.stopAt_CB.setText( 'Break %' )
        label6         = QtWidgets.QLabel() ;gb3_h1_left.addWidget(label6)
        label6.setText('Matching , Iter')
        
        gb3_h1_right    = QtWidgets.QVBoxLayout()  ;gb3_h1.addLayout( gb3_h1_right )
        
        self.maxIter_SB     = QtWidgets.QSpinBox()  ;gb3_h1_right.addWidget( self.maxIter_SB )
        self.errorPercentBreak_DSB     = QtWidgets.QDoubleSpinBox()  ;gb3_h1_right.addWidget( self.errorPercentBreak_DSB )
        
        gb3_h1_right_h        = QtWidgets.QHBoxLayout()  ;gb3_h1_right.addLayout( gb3_h1_right_h )
        self.error_LE         = QtWidgets.QLineEdit() ;gb3_h1_right_h.addWidget( self.error_LE )
        self.iterDone_LE     = QtWidgets.QLineEdit() ;gb3_h1_right_h.addWidget( self.iterDone_LE )
        
        
        # Final Button
        self.convert_PB     = QtWidgets.QPushButton()  ;central_Layout.addWidget( self.convert_PB )
        self.convert_PB.setText( 'Convert' )
        
        
        #
        # Size, Margins (left top right bottom), shape
        #
        self.setGeometry( QtCore.QRect(1173, 713, 197, 262) )
        central_Layout.setContentsMargins( 4,5,4,5 )
        
        gb1_v1.setContentsMargins( 8,4,8,5 )
        gb2_v1.setContentsMargins( 8,4,8,5 )
        gb3_v1.setContentsMargins( 8,4,8,5 )
        
        for layout in ( gb1_h1, gb1_h1_left, gb1_h1_right, gb1_h1_right_h,
                        gb2_h1, gb2_h1_left, gb2_h1_right,
                        gb3_h1, gb3_h1_left, gb3_h1_right, gb3_h1_right_h ):
            layout.setContentsMargins( 0,0,0,0 )
        
        for layout in ( central_Layout,
                        gb1_v1, gb1_h1, gb1_h1_left, gb1_h1_right, gb1_h1_right_h,
                        gb2_v1, gb2_h1, gb2_h1_left, gb2_h1_right,
                        gb3_v1, gb3_h1, gb3_h1_left, gb3_h1_right, gb3_h1_right_h ):
            layout.setSpacing( 0 )
        
        self.gb2.setEnabled( True )
        self.gb3.setEnabled( True )
        label6.setEnabled( False )
        self.error_LE.setEnabled( False )
        self.iterDone_LE.setEnabled( False )
        self.convert_PB.setStyleSheet('background-color: rgb(60,60,60);\nborder: 2px solid rgb(30,30,30);\nborder-radius: 3px;\nfont:  13pt courier;\ncolor : rgb(100,255,180);')
        self.errorPercentBreak_DSB.setEnabled( False )
        
        for item in (self.maxInf_SB, self.startFrame_LE, self.endFrame_LE, self.numJoint_SB,
                    self.errorPercentBreak_DSB, self.maxIter_SB, self.error_LE, self.iterDone_LE ):
            item.setAlignment( QtCore.Qt.AlignCenter )
        
        
        #
        # Default values
        #
        self.maxInf_SB.setValue( 8 )
        self.maxInf_SB.setMaximum( 200 )
        
        int_Validator   = QtGui.QIntValidator()
        self.startFrame_LE.setValidator(  int_Validator  )
        self.startFrame_LE.setText( '0' )
        self.endFrame_LE.setValidator( int_Validator  )
        self.endFrame_LE.setText( '30' )
        
        self.selectedJoints_CB.setChecked( False )
        
        self.numJoint_SB.setValue( 50 )
        self.numJoint_SB.setSingleStep( 10 )
        self.numJoint_SB.setMaximum( 10000 )
        self.rigid_CB.addItem( 'Rigid' )
        self.rigid_CB.addItem( 'Flexible' )
        self.rigid_CB.setCurrentIndex( 0 )
        
        self.makeRoot_CB.setChecked( False )
        
        self.stopAt_CB.setChecked( False )
        self.maxIter_SB.setValue( 10 )
        self.maxIter_SB.setMaximum( 10000 )
        self.errorPercentBreak_DSB.setValue( 1.0 )
        self.errorPercentBreak_DSB.setSingleStep( .1 )
        
        self.error_LE.setText( '.0' )
        self.iterDone_LE.setText( '0' )
        
        
        #
        # FUNCTIONS
        #
        self.selectedJoints_CB.stateChanged.connect( self.selectedJoints_changed )
        self.stopAt_CB.stateChanged.connect( self.stopAt_changed )
        self.convert_PB.clicked.connect( self.convert_selection0 )
    
    
    def selectedJoints_changed(self):
        
        state   = self.selectedJoints_CB.isChecked()
        
        if state==True:
            self.gb2.setEnabled(False)
            self.gb3.setEnabled(False)
        else :
            self.gb2.setEnabled(True)
            self.gb3.setEnabled(True)
    
    def stopAt_changed(self):
        
        state   = self.stopAt_CB.isChecked()
        
        if state==True:
            self.errorPercentBreak_DSB.setEnabled(True)
        else :
            self.errorPercentBreak_DSB.setEnabled(False)
    
    def get_errorPercentBreak(self):
        state   = self.stopAt_CB.isChecked()
        
        if state==True :
            return self.errorPercentBreak_DSB.value()
        else :
            return -1.0
    
    def get_meshes(self):
        
        meshes  = get_selected_meshes( noIntermediate=True )
        
        if not meshes :
            return None
            
        return meshes
    
    def are_animated(self, meshes):
        
        for item in meshes :
            if not is_animated_mesh(item) :
                return False
        
        return True
    
    def convert_selection0(self):
        
        meshes          = self.get_meshes()
        if not meshes :
            cmds.warning( 'Please select an Animated Mesh' )
            return
        
        are_animated    = self.are_animated( meshes )
        if not are_animated :
            cmds.warning( 'Meshes must be animated' )
            return
        
        
        # create or use selected joints
        useSelectedJoints   = self.selectedJoints_CB.isChecked()
        
        if useSelectedJoints :
            existingJoints  = cmds.ls(sl=True, type='joint')
            numJoint        = len(existingJoints)
            makeRoot        = None
            maxIteration    = 1  # no joint iteration
        else :
            existingJoints  = None
            numJoint        = self.numJoint_SB.value()
            makeRoot        = self.makeRoot_CB.isChecked()
            maxIteration    = self.maxIter_SB.value()
            
        
        #
        if numJoint < 1:
            cmds.warning( "numJoint can't be < 1" )
            return
        
        maxInf      = self.maxInf_SB.value()
        
        if maxInf > numJoint :
            cmds.warning( "MaxInfluence can't be > numJoint" )
            return
        
        
        # endFrame is included
        startFrame  = int( self.startFrame_LE.text() )
        endFrame    = int( self.endFrame_LE.text() )
        
        if startFrame >= endFrame:
            cmds.warning( 'startFrame must be < endFrame' ) 
            return
        
        frames      = [ float(item) for item in range(startFrame, endFrame+1) ]
        
        if len(frames) < 2 :
            cmds.warning( 'Need at least 2 frames ( here frames are %s )' %frames ) 
            return
        
        
        # doit
        errorPercentBreak   = self.get_errorPercentBreak() # usused if -1.0
        rigidMatrices       = bool( 1 - self.rigid_CB.currentIndex())
        
        cmds.undoInfo(openChunk=True)
        cmds.refresh(suspend=True)
        res  = from_scratch( meshes, existingJoints, numJoint, maxInf, frames, maxIteration,
                               errorPercentBreak   = errorPercentBreak,
                               deleteInitJoints    = True,
                               rigidMatrices       = rigidMatrices,
                               makeRoot            = makeRoot, )
        cmds.refresh(suspend=False)
        cmds.undoInfo(closeChunk=True)
        
        # show error in UI
        self.set_matching( res['error'], res['iterationDone'] )
        


    def set_matching(self, err, iterDone ):
        
        matching    = get_matching_percent( err )
        
        self.error_LE.setText( '%.3f' %matching )
        
        self.iterDone_LE.setText( str(iterDone ) )

def showUI():
    win     = DeformationToSkinningGUI()
    win.show()
    return win

#
#
# Utilities
#
#

def filter_meshes( items, noIntermediate=True ):
    '''Return meshes, useful for selection'''
    
    items2  = cmds.ls( items, type=('transform','mesh'))
    meshes  = []
    
    for item in items2 :
        nodeType    = cmds.nodeType(item)
        
        if nodeType == 'mesh':
            meshes.append( item )
            
        elif nodeType == 'transform':
            
            shapes = cmds.listRelatives(item, s=True, path=True, noIntermediate=noIntermediate )  # -path give fullPath only if doubleNamed
            
            for shape in shapes :
                if cmds.nodeType(shape)=='mesh':
                    meshes.append( shape )    
    return meshes

def get_selected_meshes( noIntermediate=True ):
    sel     = cmds.ls(sl=True, type=('transform','mesh'))
    return filter_meshes( sel, noIntermediate=noIntermediate )

def is_animated_mesh( mesh ):
    # simply check if there is a connection in .inMesh attribute
    
    inputs  = cmds.listConnections( mesh+'.inMesh', s=True, d=False)
    if not inputs :
        return False
    
    # excude polyPrimitive
    heritance   = cmds.nodeType(inputs[0], inherited=True)
    if 'polyPrimitive' in heritance :
        return False
    
    return True

def combine( meshes, createMesh=True, deleteHistory=True):
    
    polyUnite   = cmds.createNode( 'polyUnite', ss=True )
    for ii,mesh in enumerate(meshes):
        cmds.connectAttr( mesh+'.outMesh', polyUnite+'inputPoly[%s]'%ii )
        cmds.connectAttr( mesh+'.worldMatrix', polyUnite+'inputMat[%s]'%ii )
    
    if not createMesh :
        return polyUnite, None, None
    
    #
    newTr       = cmds.createNode('transform', ss=True)
    newMesh     = cmds.createNode( 'mesh', parent=newTr, ss=True )
    cmds.connectAttr( polyUnite+'.output' , newMesh+'.inMesh' )
    
    #
    if deleteHistory :
        cmds.delete( newMesh, ch=True )
        return None, newTr, newMesh
    
    return polyUnite, newTr, newMesh

def get_shapePosition( shape ):
    """Get the positionId of this shape under its transform"""
    tr          = cmds.listRelatives(shape, p=True, pa=True )[0]  # -path give fullPath only if doubleNamed
    allShapes   = cmds.listRelatives( tr, shapes=True, path=True) 
    posId       = allShapes.index( shape )
    return posId

def duplicate_shape( shape, onTR = None, ):
    # duplicate under a tmp transform then delete it
    # because the magic function exists only with Pymel
    shapeTR     = cmds.listRelatives(shape, p=True)[0]
    posId       = get_shapePosition( shape )
    
    dupTR       = cmds.duplicate( shape, rc=True ) [0]
    dup         = cmds.listRelatives( dupTR, shapes=True) [ posId ]
    
    if onTR and onTR != shapeTR :
        cmds.parent( dup, onTR, s=True, r=True )
    else :
        cmds.parent( dup, shapeTR, s=True, r=True )
    
    cmds.delete( dupTR )
    return dup

def duplicate_with_transform( shape, restorePivot=False ):
    '''
    shapeTR     = cmds.listRelatives(shape, p=True, pa=True)[0] # -path give fullPath only if doubleNamed
    newTR       = create_on( shapeTR, nodeType='transform', t=True, r=True, s=True, pivot=False)
    newShape    = duplicate_shape( shape, onTR=newTR  )
    
    if restorePivot :
        rPivot  = cmds.getAttr(shapeTR+'.rotatePivot')[0]
        sPivot  = cmds.getAttr(shapeTR+'.scalePivot')[0]
        cmds.setAttr( newTR+'.rotatePivot', rPivot[0],rPivot[1],rPivot[2] )
        cmds.setAttr( newTR+'.scalePivot', sPivot[0],sPivot[1],sPivot[2] )
    '''
    
    newTR       = cmds.duplicate( shape, rc=True ) [0]
    newShapes   = cmds.listRelatives( newTR, shapes=True)
    finalShape  = None
    
    posId       = get_shapePosition( shape )
    for id,newShape in enumerate(newShapes) :
        if id==posId:
            finalShape  = newShape
        else:
            cmds.delete(newShape)
    
    return newTR, finalShape


def get_meshFn( meshName  ):
    sList       = OpenMaya.MSelectionList()
    sList.add(meshName)
    dagPath     = OpenMaya.MDagPath()
    sList.getDagPath(0, dagPath)
    return OpenMaya.MFnMesh( dagPath )

def get_points( mesh, space=OpenMaya.MSpace.kWorld ):
    fn      = get_meshFn( mesh  )
    pnts    = OpenMaya.MFloatPointArray()
    fn.getPoints( pnts, space )
    return pnts

def get_points_as_tuples( mesh, space=OpenMaya.MSpace.kWorld ):
    pnts    = get_points( mesh, space=space )
    pnts2   = []
    for ii in range(pnts.length()):
        pnts2.append(  (pnts[ii].x, pnts[ii].y, pnts[ii].z)  )
    return pnts2


class Cluster(object):
    id = 0
    def __init__(self, center):
        self.id         = Cluster.id
        Cluster.id        += 1
        self.center        = center
        self.prevCenter = None
        self.points        = [] 
        self.pointIds   = []
        
    def clear_points(self):
        self.points        = [] 
        self.pointIds   = [] 
        
    def add_point(self, pntId,pnt):
        self.points.append( pnt )
        self.pointIds.append( pntId ) # id of this pnt in the input points list
        
    def compute_error(self, get_distance):
        error   = .0
        for pnt in self.points:
            error   += get_distance(self.center, pnt)
        return error
    
    def get_center(self):
        return self.center
    
    def update_center(self, get_centroid):
        self.prevCenter = self.center
        self.center     = get_centroid(self.points)
        
    def center_changed(self, get_distance):
        if self.prevCenter == None:
            return True
        return get_distance(self.prevCenter, self.center) > epsilon

def get_clusters(points, numMeans, maxIterations=None):
    '''K-Means Clustering 
    points: List of points to cluster. 
    numMeans: Number of clusters desired.
    maxIterations: Optional parameter used to constrain the number of iterations the alorithm can run for.
    '''
    
    if numMeans < 1 :
        return [[], .0, 0] 
    
    
    clusters        = init_clusters(points, numMeans)
    iterations        = 0
    hasConverged    = False
    
    while not hasConverged and (iterations < maxIterations or maxIterations == None):
        iterations += 1
        
        # cluster assignment step
        for cluster in clusters:
            cluster.clear_points()
            
        for pntId,pnt in enumerate(points):
            closestCluster = get_closest_cluster(pnt, clusters)
            closestCluster.add_point( pntId, pnt )
            
        # update cluster centers 
        for cluster in clusters:
            cluster.update_center(get_centroid)
        hasConverged = not clusters_were_updated(clusters, get_distance)
    
    totalError = .0
    for cluster in clusters:
        totalError += cluster.compute_error(get_distance)
    
    return [clusters, totalError, iterations]    

def init_clusters( points, numMeans ):
    
    clusters    = []
    numPoints   = len(points)
    
    # the initial k clusters are some random input points
    # it improves how fast is the convergence
    # cant use the same point twice, so choose an id then remover it from the id-list
    ids     = range( numPoints )
    
    for kk in range(numMeans):
        randomId     = random.choice( ids )
        ids.remove( randomId )
        
        clusters.append( Cluster(points[randomId]) )
        
    return clusters 

def clusters_were_updated(clusters, get_distance):
    
    wereUpdated     = False
    
    for cluster in clusters:
        wereUpdated |= cluster.center_changed(get_distance)
        
    return wereUpdated

def get_closest_cluster( pnt, clusters):
    closestDist        = float("inf") 
    closestCluster  = None
    
    for cluster in clusters:
        distance = get_distance( pnt, cluster.center)
        if distance < closestDist:
            closestDist        = distance
            closestCluster  = cluster 
    
    return closestCluster

def get_closest_pnt( pnts, pnt):
    closestDist        = float("inf") 
    closest_pos     = None
    
    for ii,pp in enumerate(pnts):
        distance = get_distance( pnt, pp)
        if distance < closestDist:
            closestDist        = distance
            closest_pos     = ii 
    
    return closest_pos

def get_distance(x, y):
    return sum([(a-b)**2 for a,b in zip(x,y)])

def get_centroid(items):
    
    arrangeByDimensions = zip(*map(lambda x: x, items))
    averageLocation = []
    
    for dimVals in arrangeByDimensions:
        averageLocation.append(sum(dimVals) / len(dimVals))
    
    return tuple(averageLocation)


def fix_points_duplicates( mesh, pnts ):
    '''Kmeans does not like pnts duplicates, offset them with a small random value'''
    
    diag        = get_diagonalLength( mesh, world=False )
    offsetLen   = .0001 * diag
    
    if len(frozenset(pnts)) != len(pnts):
        
        # enumerate duplicates
        pnts_dict = {}
        
        for id,item in enumerate(pnts) :
            if item not in pnts_dict :
                pnts_dict[item] = [id]
            else :
                pnts_dict[item].append( id )
        
        # edit only those > 1
        for vIds in pnts_dict.values() :
            
            if len(vIds) > 1 :
                # randomize different small values
                for vId in vIds :
                    
                    offsetVec   = []
                    for kk in range(3):
                        val     = .0
                        while val==.0 :val = random.uniform(-offsetLen,offsetLen)
                        offsetVec.append(val)
                        
                    pnts[vId]     = ( pnts[vId][0]+offsetVec[0], pnts[vId][1]+offsetVec[1], pnts[vId][2]+offsetVec[2] )
    return pnts

def get_from_kmeans( mesh, k, maxIter=None ):
    '''Each cluster contains its centroid value, the points used, and the pointIds in the concatened_points list'''
    pnts    = get_points_as_tuples( mesh ) # kWorld by default
    pnts    = fix_points_duplicates( mesh, pnts )
    [clusters, error, numIter] = get_clusters( pnts, k, maxIterations=maxIter)
    return clusters 

def get_MItMeshVertex( meshName  ):
    sList       = OpenMaya.MSelectionList()
    sList.add(meshName)
    dagPath     = OpenMaya.MDagPath()
    sList.getDagPath(0, dagPath)
    return OpenMaya.MItMeshVertex( dagPath )

def get_vertexUVs( mesh ):
    meshItVertex    = get_MItMeshVertex( mesh  )
    numVertex       = meshItVertex.count()
    uvs             = {}
    for ii in range(numVertex):
        vId         = meshItVertex.index()
        util        = OpenMaya.MScriptUtil()
        ptr         = util.asFloat2Ptr()
        meshItVertex.getUV( ptr )
        u   = util.getFloat2ArrayItem(ptr, 0, 0)
        v   = util.getFloat2ArrayItem(ptr, 0, 1)
        uvs[vId]    = (u,v)
        meshItVertex.next()
    return uvs

def attach_joints( trs, mesh , vIds ):
    uvs     = get_vertexUVs( mesh )
    mshTr   = cmds.listRelatives( mesh, parent=True )[0]
    conss   = []
    for vId,tr in zip(vIds, trs):
        u,v     = uvs[vId]
        cons    = cmds.pointOnPolyConstraint( mesh+'.vtx[%s]'%vId, tr )[0]
        cmds.setAttr( cons+'.'+mshTr+'U0', u )
        cmds.setAttr( cons+'.'+mshTr+'V0', v )
        conss.append( cons )
    return conss

def build_joints( mesh, k, maxIter = None, nodeType = 'joint' ):
    
    clusters    = get_from_kmeans( mesh, k, maxIter=maxIter )
    trs         = []
    vIds        = []
    
    for kk in range(k):
        tr  = cmds.createNode( nodeType, n=nodeType+str(kk), ss=True)
        t   = clusters[kk].center
        
        cmds.setAttr( tr+'.t', t[0],t[1],t[2] )
        
        #
        # build on averaged vId
        # get centroid
        #centroid   = get_centroid( clusters[kk].points ) # clusters[kk].pointIds
        centroid        = clusters[kk].center
        closest_pos     = get_closest_pnt( clusters[kk].points, centroid )
        closest_vId     = clusters[kk].pointIds [closest_pos]
        #closestPnt      = clusters[kk].points   [closest_pos]
        
        # build rivet on this vId
        trs.append( tr )
        vIds.append( closest_vId )
        
    return trs, vIds


def getMObject(node ):
    sList = OpenMaya.MSelectionList()
    sList.add(node)
    oNode = OpenMaya.MObject()
    sList.getDependNode(0, oNode)
    return oNode

def get_center_at_frames( shape, frames, world=True ):
    centers     = []
    for frame in frames :
        cmds.currentTime( frame )
        centers.append( get_center( shape, world=world ) )
    return centers

def get_center( shape, world=False ):
    centerp     = get_MBoundingBox( shape, world=world ).center()
    return (centerp.x,centerp.y,centerp.z)

def get_as( node, attr, apiType ):
    values   = cmds.getAttr(node+'.'+attr)
    if apiType=='MFloatVector':
        return OpenMaya.MFloatVector(values[0][0],values[0][1],values[0][2]) # pymel is better with that
    elif apiType=='MVector':
        return OpenMaya.MVector(values[0][0],values[0][1],values[0][2])
    elif apiType=='MFloatMatrix':
        fm    = OpenMaya.MFloatMatrix()
        OpenMaya.MScriptUtil.createFloatMatrixFromList( values , fm )
        return fm
    elif apiType=='MMatrix':
        mm    = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList( values , mm )
        return mm
    
def get_MBoundingBox( shape, world=False ):
    dag     = OpenMaya.MFnDagNode( getMObject(shape) )
    bb      = dag.boundingBox()
    if world :
        tr      = cmds.listRelatives(shape, parent=True)[0]
        mm      = get_as( tr, 'wm[0]', apiType='MMatrix' )
        bb.transformUsing(mm)
    return bb

def get_diagonalLength( shape, world=False ):
    bb      = get_MBoundingBox( shape, world=world )
    minp    = bb.min()
    maxp    = bb.max()
    diag    = (maxp-minp).length()
    return diag

def create_animCurve_on( node, attr, data={} ):
    
    plug    = getMPlug( node, attr )
    unit    = OpenMaya.MTime.uiUnit()
    
    animCurve_fn    = OpenMayaAnim.MFnAnimCurve()
    animCurve_Obj   = animCurve_fn.create( plug )
    animCurve_name  = animCurve_fn.name()
    
    if data :
        times       = data['times']
        values      = data['values']
        for kk in range(len(times)) :
            animCurve_fn.addKey( OpenMaya.MTime(times[kk], unit), values[kk] )
        # tangents
        #
    return animCurve_name

def create_anims( nodes, attrs, datas ):
    animCurves  = []
    for node in nodes :
        for ii,attr in enumerate(attrs) :
            animCurves.append( create_animCurve_on( node, attr, data=datas[ii] ) )
    return animCurves


def get_skinCluster( shape ):
    '''get the first skinCLuster found'''
    skinNode    = mel.eval("findRelatedSkinCluster %s;"%shape)
    if skinNode :
        return skinNode
    return None

def is_skinned( shape ):
    
    if get_skinCluster( shape ):
        return True
    else : 
        return False

def build_skin( shape, joints, maxInf ):
    
    skinNode    = cmds.skinCluster( shape, joints, 
                        mi    = maxInf,
                        omi    = True,
                        nw    = 0,
                        sm    = 0,
                        tsb    = True  ) [0]
    
    # normalize now, to avoid crappy warnings when I set the weights
    cmds.skinCluster( skinNode, forceNormalizeWeights=True, edit=True )
    cmds.setAttr(  skinNode+'.normalizeWeights', 1  ) # interactive
    #
    return skinNode

def remove_unusedInfluence( skinCluster ):
    infs        = cmds.skinCluster(skinCluster, q=True, influence=True)
    wgted_infs    = cmds.skinCluster(skinCluster, q=True, weightedInfluence=True)
    unuseds        = tuple( frozenset(infs)-frozenset(wgted_infs) )
    if unuseds :
        cmds.skinCluster(skinCluster, e=True, removeInfluence=unuseds)
    return unuseds

def copy_skin( fromShape, toShapes,
                removeUnused    = False,
                surfAssociation ="closestPoint",
                infAssociation  =("oneToOne","closestJoint","label")):
    '''Copy skin from a shape to anothers, building news'''
    
    skinNode        = get_skinCluster( fromShape )
    jnts            = cmds.skinCluster( skinNode, q=True, inf=True )
    maxInf          = cmds.skinCluster( skinNode, q=True, mi=True)
    
    cmds.delete( toShapes, ch=True )
    newSkinNodes    = []
    
    for toShape in toShapes :
        newSkinNode     = build_skin( toShape, jnts, maxInf  )
        newSkinNodes.append( newSkinNode )
        
        cmds.copySkinWeights( fromShape, toShape, noMirror=True, sa=surfAssociation, ia=infAssociation  )
        
        if removeUnused:
            remove_unusedInfluence( newSkinNode )
    
    return newSkinNodes


def group( trs, nodeType='transform' ):
    grp     = cmds.createNode( nodeType, ss=True )
    cmds.parent( trs, grp  )
    return grp

def set_color( node, colorId ):
    cmds.setAttr( node+'.overrideEnabled' , True)
    cmds.setAttr( node+'.overrideColor' , colorId)


def get_hierarchy( tr, reverse=False ):
    allParents  = []
    parent      = cmds.listRelatives(tr, p=True)
    
    while parent :
        allParents.append( parent[0] )
        parent  = cmds.listRelatives(parent[0], p=True)
    
    #
    if reverse:
        allParents.reverse()
    
    return allParents

def relist_by_hierarchy( trs ):
    newList = []
    for tr in trs :
        if len(newList)==0:
            newList.append(tr )
            continue
        #
        hierarchy   = get_hierarchy( tr, reverse=False)
        if not hierarchy :
            newList.insert( 0, tr )
            continue
        #
        done = False
        for hier in hierarchy :
            if hier in newList :
                pos = newList.index(hier) +1
                newList.insert(pos, tr)
                done = True
            if done :
                break
        if done :
            continue
        newList.insert( 0, tr )
    return newList

def get_targetTranslate( targetTr, useTargetPivot=True, space='world' ):
    t    = None
    if space=='world':
        if useTargetPivot :
            t   = cmds.xform(targetTr, q=True, rp=True, ws=True)
        else :
            wm  = get_as( targetTr, 'wm', 'MMatrix')
            t   = [wm(3,0), wm(3,1), wm(3,2)]
    elif space=='object':
        t       = cmds.getAttr(targetTr+'.t')[0]
        if useTargetPivot :
            # add him   rotatePivotTranslate  and  rotatePivot
            rpt = cmds.getAttr(targetTr+'.rotatePivotTranslate')[0]
            rp  = cmds.getAttr(targetTr+'.rotatePivot')[0]
            t   = [ t[ii]+rpt[ii]+rp[ii] for ii in range(3)]
    return t

def substract_drivenPivot( drivenTr, targetTranslate  ):
    
    rotPivot_FV    = ( get_as( drivenTr, 'rotatePivotTranslate', 'MVector')
                  + get_as( drivenTr, 'rotatePivot', 'MVector')  )
    
    rotPivot_FV = rotPivot_FV * get_as( drivenTr, 'pim', 'MMatrix')
    rotPivot    = (rotPivot_FV.x,rotPivot_FV.y,rotPivot_FV.z)
    
    new_targetTranslate        = [item1-item2 for item1,item2 in zip(targetTranslate, rotPivot)]
    return new_targetTranslate

def snap_on( tr, onTr, t=False, r=False, s=False, useDrivenPivot=True ):
    """Snap world pos"""
    if t :
        targetTranslate     = get_targetTranslate( onTr, space='world', useTargetPivot=useDrivenPivot  )
        if useDrivenPivot :
            targetTranslate     = substract_drivenPivot( tr, targetTranslate  )
        cmds.xform( tr, t=targetTranslate, ws=True )
    
    if r :
        wm          = get_as( onTr, 'wm', 'MMatrix') # xform -q -ws -ro  fails sometimes
        euler       = mEuler_from_MMatrix( wm, rotOrder=cmds.getAttr(tr+'.ro') )
        new_wRot    = degrees_from_mEuler( euler )
        cmds.xform( tr, ro=new_wRot, ws=True )
    
    if s :
        # too complex in world because need Shearing and I dont want that
        s3      = cmds.getAttr(onTr+'.scale')[0]
        cmds.setAttr(tr+'.scale', s3[0], s3[1], s3[2] )
        
def create_on( onTr,
               nodeType='transform',
               t=True, r=True, s=False,
               pivot=True, ):

    # create and snap
    newTr   = cmds.createNode( nodeType, ss=True )
    snap_on( newTr, onTr, t=t, r=r, s=s, useDrivenPivot=pivot  )
    
    return newTr

def copy_rotateOrder( fromJnts, toJnts ):
    """Change the rotateOrders from fromJnts to toJnts without moving """
    for fromJnt,toJnt in zip(fromJnts, toJnts):
        from_ro    = cmds.getAttr(fromJnt+'.ro')
        to_ro      = cmds.getAttr(toJnt+'.ro')
        if from_ro != to_ro :
            reorder( toJnt, from_ro  )

def radians_from_degrees( degrees ):
    return [ degree*math.pi/180.0 for degree in degrees ]

def degrees_from_mEuler( euler ) :
    return [ radi*180.0/ math.pi for radi in (euler[0], euler[1], euler[2]) ]

def mEuler_from_degrees( degrees, ro_int=0  ) :
    rad     = radians_from_degrees( degrees  )
    return OpenMaya.MEulerRotation( rad[0], rad[1], rad[2], ro_int )
    
def reorder( jnt, new_rotOrder  ):
    """Change rotateOrder without moving,
    Dont use matrix because the order just affects .rotate  not .ra  and .jo """
    
    degrees     = cmds.getAttr(jnt+'.rotate') [0] # because cmds return list of tuple
    ro          = cmds.getAttr(jnt+'.ro')
    
    euler        = mEuler_from_degrees( degrees, ro_int=ro )
    euler.reorderIt( new_rotOrder )
    
    new_degrees = degrees_from_mEuler(    euler )
    
    cmds.setAttr(jnt+'.ro', new_rotOrder)
    cmds.setAttr(jnt+'.rotate', new_degrees[0], new_degrees[1], new_degrees[2])

def parent_no_mediator( child, parent ):
    wm      = cmds.getAttr(child+'.wm')
    cmds.parent( child, parent, r=True )
    cmds.xform( child, m=wm, ws=True)
    
def mEuler_from_MMatrix( mm, rotOrder=0) :
    """Build a MEulerRotation from MFloatMatrix"""
    mEuler        = OpenMaya.MEulerRotation.decompose( mm, 0)
    if rotOrder !=0:
        # I prefer to reorder after creation  because I am not sure  this works fine every time
        mEuler.reorderIt( rotOrder )
    return mEuler

def clean_rotation( jnts, rotationTo='r'):
    """Bake rotations in only one rotation attribute """
    
    for jnt in jnts :
        
        # do nothing if all the rotation attrs are not free (settable)
        if not (cmds.getAttr(jnt+'.r', settable=True)  and
                cmds.getAttr(jnt+'.jo', settable=True)  and
                cmds.getAttr(jnt+'.ra', settable=True)  ):
            continue
        
        # store and set 0 0 0
        fm  = get_as( jnt, 'm', 'MMatrix')
        ro    = cmds.getAttr(jnt+'.ro')
        
        cmds.setAttr(jnt+'.rotate',0,0,0)
        cmds.setAttr(jnt+'.jo', 0,0,0)
        cmds.setAttr(jnt+'.ra', 0,0,0)
        
        # convert matrix in the good euler
        euler        = mEuler_from_MMatrix( fm, rotOrder=ro  )
        
        if not rotationTo in ('r','rotate'):
            # convert to kXYZ because .jo and .ra are always in kXYZ
            euler.reorderIt( 0 )
        
        new_rot     = degrees_from_mEuler(  euler )
        
        # set this rotation in only one attr
        cmds.setAttr( jnt+'.'+rotationTo, new_rot[0], new_rot[1], new_rot[2])

def segmentScale_( parent, child, connect=True, value=True):
    """Do a segment scale connection"""
    if connect!=None :
        alreadyConnected    = cmds.isConnected( parent+'.scale', child+'.inverseScale' )
        
        if connect and not alreadyConnected:
            cmds.connectAttr( parent+'.scale', child+'.inverseScale')
        elif not connect and alreadyConnected :
            cmds.disconnectAttr( parent+'.scale', child+'.inverseScale')
    
    if value != None:
        cmds.setAttr( child+'.segmentScaleCompensate', value)
        
def parent_( trs, parent, relative=False,  rotationTo='r', segmentScale=True ):
    '''Smart and clean parent, with joint options included'''
    
    for tr in trs :
        if relative :
            cmds.parent( tr, parent, r=True)
        else :
            parent_no_mediator( tr, parent )
        
        # if joint  apply a rotationTo and segmentScale setting
        if cmds.nodeType(tr)=='joint':
            clean_rotation( (tr,), rotationTo=rotationTo )
            segmentScale_( parent, tr, connect=segmentScale, value=segmentScale)

def copy_hierarchy( fromTrs, toTrs, parentToClosest=False, elseParent=None, rotationTo='r' ):
    
    for i in range( len(fromTrs) ):
        # find the new parent to use if it is in fromTrs
        if parentToClosest :    parents = get_hierarchy(fromTrs[i], reverse=True)
        else :                  parents = cmds.listRelatives(fromTrs[i], p=True)
        
        if parents:
            for p in parents :
                if p in fromTrs :
                    new_p    = toTrs[ fromTrs.index( p ) ]
                    parent_( [toTrs[i]], new_p ,  rotationTo=rotationTo, segmentScale=False )
        
        elif elseParent :
            parent_( [toTrs[i]], elseParent ,  rotationTo=rotationTo, segmentScale=False )
            
        else :
            # dont parent
            pass

def duplicate_trs( trs, hierarchy=False, parentToClosest=True, elseParent=None, nodeType='transform' ):
    
    newTrs     = [ create_on( tr, nodeType=nodeType) for tr in trs ]
    
    copy_rotateOrder( trs, newTrs )
    
    if hierarchy :
        copy_hierarchy( trs, newTrs, parentToClosest=parentToClosest, elseParent=elseParent, rotationTo='r')
    
    return newTrs


def getMPlug(node, attr):
    try :
        sList = OpenMaya.MSelectionList()
        sList.add('%s.%s'%(node, attr))
        mPlug = OpenMaya.MPlug()
        sList.getPlug(0, mPlug)
    except :
        # .rotatePivot fails in the default method ...
        mPlug     = OpenMaya.MFnDependencyNode(getMObject(node)).findPlug( attr )
    
    return mPlug

def get_usedArrayIds( node, attr ):
    """Return the used ids of this array attr """
    plug        = api.getMPlug( node, attr )
    intArray    = OpenMaya.MIntArray()
    plug.getExistingArrayAttributeIndices( intArray )
    return intArray

def get_joints( skinCluster ):
    '''Get joints as a dict, keys are matrixIds, values are jointNames '''
    matrixIds   = get_usedArrayIds( skinCluster, 'matrix' )
    jnts        = {}
    for idx in matrixIds :
        inputs  = cmds.listConnections( skinCluster+'.matrix[%s]'%idx, s=True, d=False )
        if inputs :
            jnts[idx]   = str(inputs[0])
        else :
            jnts[idx]   = None
    return jnts

def MM_to_float16( m ):
    return [m(ii,jj) for ii in range(4) for jj in range(4)]

def MMatrix_setAttr( plug, MM_or_FM=None, float16=None ):
    if MM_or_FM :
        cmds.setAttr( plug, MM_to_float16( MM_or_FM ), type='matrix' )
    elif float16 :
        cmds.setAttr( plug, float16, type='matrix' )

def reset_skin( skinNode ):
    '''Simply reset the new bindingMatrices without killing anything '''
    
    jnts_data    = get_joints( skinNode )
    
    for jId, joint in jnts_data.items() :
        MMatrix_setAttr( skinNode+'.bindPreMatrix[%s]'%jId, get_as( joint,'wim','MMatrix') )
    

def get_numVertex( mesh ):
    return cmds.polyEvaluate( mesh, v=True )

def get_vertexIds( mesh ):
    return range( get_numVertex( mesh ) )


def node_add_dict( node, dic, parent=None ):
    for attr, attrType in dic.items() :
        add_( node, attr, attrType,  parent=parent  )
    
def add_( node, attr, attrType, multi=False, parent=None  ):
    '''Need to use a eval( cmd ) because -parent flag canNOT be set to NONE, fuck.
    toDo : Find a way to allow attribute order '''

    # list = multi
    if isinstance( attrType, list  ):
        add_( node, attr, attrType[0], multi=True, parent=parent  )
        return


    #** dict = compound
    numChildren     = None

    if isinstance( attrType, dict  ):
        numChildren     = len( attrType )


    # DT or AT ?
    cmd     = 'cmds.addAttr( "%s", ln="%s", ' %(node, attr)


    if numChildren:
        cmd     += 'at="compound", '

    elif attrType in ( 'matrix', 'long', 'double', 'bool' ):
        cmd     += 'at="%s", ' %attrType

    elif attrType in ('Int32Array', 'doubleArray', 'stringArray', 'string' ):
        cmd     += 'dt="%s", ' %attrType

    

    #**
    if numChildren:
        cmd     += 'nc=%s, ' %numChildren

    if parent :
        cmd     += 'p="%s", ' %parent


    #
    cmd    += 'm=%s, )' %multi
    eval( cmd )


    #**
    if numChildren :
        add_dict( node, attrType, parent=attr )

def node_set_dict(node, dico):
    for attrName,value in dico.items():
        set_( node, attrName, value )
        
def set_( node, attr, val ):
    """An intelligent setAttr working on all attrs, even compound and arrays"""

    if val is None :
        return


    # use plug because the attributeQuery is a big shit
    # with pymel all this code should be done in 3 lines
    plug        = getMPlug(node, attr)

    isArray     = plug.isArray()
    isCompound  = plug.isCompound()



    if (isinstance(val, str)
    and ('.' in val)
    and (cmds.objExists(val))
    ):
        cmds.connectAttr( val, node+'.'+attr )



    elif isArray :
        if isinstance( val, dict ):
            set_array( node, attr, val  )
        else :
            cmds.error('Array attribute, val must be a DICT')


    elif isCompound  :
        if isinstance( val, dict ):
            set_compound( node, attr, val )

        elif len(val)==3:
            #***** it is a vector or float3 *****
            cmds.setAttr(node+'.'+attr, val[0], val[1], val[2])

        else :
            cmds.error('Compound attribute, val must be a DICT or list[3]')


    else :
        #  set
        # ****** tuple mean arrayAttribute ( not multi )
        # ****** list means vector or matrix


        if isinstance( val, tuple ):

            #****** type of item[0]   define if   intArray, doubleArray, stringArray ...  

            if isinstance( val[0], int):
                cmds.setAttr( node+'.'+attr, val, type='Int32Array'  )

            elif isinstance( val[0], float ):
                cmds.setAttr( node+'.'+attr, val, type='doubleArray'  )

            elif isinstance( val[0], str ):
                cmds.setAttr( node+'.'+attr, len(val), type='stringArray', *val  )



        elif isinstance( val, list ):
            len_    = len(val)

            # ***** len defines vector/float3 or matrix

            if len_==3 :
                cmds.setAttr(node+'.'+attr, val[0], val[1], val[2])

            elif len_==16:
                cmds.setAttr(node+'.'+attr, val, type='matrix' )



        elif isinstance( val, str ):
            cmds.setAttr(node+'.'+attr, val, type='string')

        else :
            # classic
            cmds.setAttr(node+'.'+attr, val)

def create_node( nodeType,
                add_dict    = None,
                set_dict    = None,
                parent      = None, ):
    
    # load some plugins 
    if nodeType in ('decomposeMatrix', 'composeMatrix', 'inverseMatrix', 'transposeMatrix'):
        cmds.loadPlugin('matrixNodes', qt=True)
    
    if parent :
        node    = cmds.createNode(nodeType , ss=True, p=parent)
    else :
        node    = cmds.createNode(nodeType , ss=True)
    
    # add + set
    if add_dict :
        node_add_dict( node, add_dict )
    if set_dict :
        node_set_dict( node, set_dict )
    
    return node

def set_skin_weights( skinNode, weights):
    for vertexId, infs in weights.items():
        
        # reset this default crap !!! otherwise it's keeping the values made at creation time !
        cmds.removeMultiInstance( skinNode+'.weightList[%d]'%vertexId )
        
        for infId, infWgt  in  infs.items():
            cmds.setAttr(skinNode+".weightList[%d].weights[%d]"%(vertexId,infId), infWgt )


#
#
# Skinning conversion
#
#

def from_scratch( animatedMeshes,  existingJoints, numJoint,  maxInf, frames, maxIteration,
                    errorPercentBreak  = 1.0,
                    rigidMatrices      = True,
                    deleteInitJoints   = True,
                    makeRoot           = False,):
    '''
    Combine the meshes, launch SSD only once, copy resulting skinning to a copy of input meshes.
    
    if existingJoints is None, create joints using numJoint and makeRoot.
    if existingJoints, they MUST be animated by your own way.
    '''
    
    
    #*** need to go to frame0 to make  kmeans and duplicate_shapes  working well
    cmds.currentTime( frames[0] )
    
    
    #** combine them into one mesh, because it is easier than managing kmeans and ssd through multiple meshes, their codes would become unsupportable
    numMesh     = len(animatedMeshes)
    
    if numMesh > 1:
        polyUnite, tr, mesh  = combine( animatedMeshes, createMesh=True, deleteHistory=False )
        dupMeshes   = [duplicate_with_transform(item,restorePivot=True)[1]  for item in animatedMeshes]
    else :
        mesh, tr    = animatedMeshes[0], None
        dupMeshes   = []
    
    
    #
    if existingJoints :
        # They MUST be animated
        initJnts        = existingJoints
        duplicateJoints = False
        setMatrices     = False
        root            = None
        
    else :
        # initialize joints using kmeans algorithm, let the maxIter unlimited
        initJnts, vIds  = build_joints( mesh, numJoint, maxIter=None, nodeType='joint'  )
        initConss       = attach_joints( initJnts, mesh, vIds )
        
        #
        duplicateJoints = True
        setMatrices     = True
        
        #
        root            = None
        if makeRoot :
            root        = cmds.createNode('joint', ss=True )
            centers     = get_center_at_frames( mesh, frames=frames, world=True )
            create_anims( [root], ('tx','ty','tz'), ({'times':frames,'values':zip(*centers)[0]}, {'times':frames,'values':zip(*centers)[1]}, {'times':frames,'values':zip(*centers)[2]}) )
        
        
    #*** SSD, run skinningSolver, then bonesSolver  ...  * iteration
    #
    cmds.currentTime( frames[0] )
    
    ssd_res     = perform(  mesh,
                            initJnts,
                            frames,
                            maxInf,
                            maxIteration         = maxIteration,
                            iterationFullSolver = 1,
                            errorPercentBreak   = errorPercentBreak,
                            updateRestMatrices     = False,
                            rigidMatrices       = rigidMatrices,
                            
                            duplicateShape         = True,
                             duplicateJoints        = duplicateJoints,
                            setMatrices         = setMatrices,
                             root                = root,  )
    
    #** copy the final big skin to the piecewise meshes
    if numMesh > 1:
        skinMeshes  = dupMeshes
        copy_skin( [ssd_res['newShape']], skinMeshes, removeUnused=True )
        
        newTr       = cmds.listRelatives(ssd_res['newShape'], p=True)[0]
        cmds.delete( tr, newTr )
    else :
        skinMeshes  = [ssd_res['newShape']]
    
    
    
    # Groups
    jntType_str     = ['flexible','rigid'][rigidMatrices]
    skinTrs         = [cmds.listRelatives(item, p=True)[0] for item in skinMeshes]
    mesh_grp        = group( skinTrs  )
    anim_jnts_grp   = None
    init_jnts_grp   = None
    
    if not existingJoints :
        anim_jnts_grp       = group(  [ssd_res['targetJoints'],[root]][makeRoot==True]  )
        init_jnts_grp       = group(  initJnts   )
        if deleteInitJoints :
            cmds.delete( init_jnts_grp )
            initJnts        = []
            init_jnts_grp   = None
        
        
    # Naming, Colors
    mesh_grp    = cmds.rename( mesh_grp, 'meshes_j%s_mi%s_%s'%(numJoint,maxInf,jntType_str) )
    for ii in range(len(skinTrs)) :
        skinTrs[ii]     = cmds.rename(skinTrs[ii], 'mesh#')
    if anim_jnts_grp :
        anim_jnts_grp   = cmds.rename( anim_jnts_grp, 'joints_j%s_mi%s_%s'%(numJoint,maxInf, jntType_str) )
        set_color( anim_jnts_grp, 27 )
    if not existingJoints:
        for ii in range(len(ssd_res['targetJoints'])) :
            ssd_res['targetJoints'][ii]     = cmds.rename(ssd_res['targetJoints'][ii], 'jnt#')
    if init_jnts_grp :
        init_jnts_grp   = cmds.rename( init_jnts_grp, 'init_j%s'%numJoint )
    if makeRoot :
        cmds.setAttr(root+'.radius', 0)
    
    # End
    res     = {'skinMeshes':    skinMeshes,
               'newJoints':     ssd_res['targetJoints'],
               'initJnts':      initJnts,
               'error':         ssd_res['error'],
               'iterationDone': ssd_res['iterationDone'],
               'root':          root,
               'meshGrp':       mesh_grp, }
    return res


def perform( animatedShape,
             animatedJoints,
             frames,
             maxInf,
             
             maxIteration           = 1,
             iterationFullSolver    = 1,
             errorPercentBreak      = 1.0,
             updateRestMatrices     = False,
             rigidMatrices          = True,
             
             duplicateShape         = True,
             duplicateJoints        = True,
             setMatrices            = True,
             hierarchy              = True,
             root                   = True,
             
             existingSkinCluster    = None,
             maxCPU                 = -1, ):
    '''
    IMPORTANT : setMatrices is NOT undoable, so it is better to duplicateJoints=True  or  setMatrices=False
    
    iteration   = 1     compute  skinning,   does not affect bones
    iteration   > 1     compute  skinning, matrices, skinning, ...  iteratively,  so update bones.
    
    iterationFullSolver = ignored if iteration==1,  "launching the full joints solving" count.
    errorPercentBreak   = ignored if iteration==1.
    updateRestMatrices  = ignored if iteration==1.
    rigidMatrices       = ignored if iteration==1.
    
    duplicateJoints = True      duplicate and set matrices on them
    duplicateJoints = False     set matrices on animatedJoints
    setMatrices     = False     Don't set matrices, so don't animate the duplicatedJoints or don't edit/break the animatedJoints.
    
    hierarchy   allows to maintain same joint hierarchy when they are duplicated, so ignored if duplicateJoints=False.
    
    existingSkinCluster : if a skinCluster node is specified, animatedJoints are ignored and I use the influences of that skinCluster.
    The speed of the process is also increased a lot, because I use only the existing influence per vertex instead of all the joints.
    '''
    
    
    #** do it here, othewise sometimes it's bad
    cmds.currentTime( frames[0] )
    
    # override animatedJoints by the influences of this skinCluster
    # obviously, they must also be animated
    if existingSkinCluster :
        animatedJoints  = cmds.skinCluster(existingSkinCluster, q=True, inf=True)
    
    
    # new order by hierarchy allow to set the local matrices in the c++ command
    # the c++ command will then set all the good keys
    animatedJoints   = relist_by_hierarchy( animatedJoints )
    
    if setMatrices :
        if duplicateJoints :    targetJoints    = duplicate_trs( animatedJoints, hierarchy=hierarchy, nodeType='joint', elseParent=root )
        else :                  targetJoints    = list( animatedJoints )
    else : #unused
        targetJoints    = None
    
    
    # compute weights 
    weights, error, iterationDone     = run_cpp(    animatedShape,
                                                    animatedJoints,
                                                    frames,
                                                    maxInf,
                                                    maxIteration        = maxIteration,
                                                    iterationFullSolver = iterationFullSolver,
                                                    errorPercentBreak   = errorPercentBreak,
                                                    updateRestMatrices  = updateRestMatrices,
                                                    rigidMatrices       = rigidMatrices,
                                                    setMatrices         = setMatrices,
                                                    targetJoints        = targetJoints,
                                                    existingSkinCluster = existingSkinCluster,
                                                    maxCPU              = maxCPU,)
    
    
    if (maxIteration>1) and (not duplicateJoints) and (is_skinned(animatedShape)) :
        # animatedJoints have been moved by the c++ cmd, so the original shape CAN be bad now,  reset skin !
        reset_skin( animatedShape  )
    
    
    
    # create skin + set weights  to newShape
    if duplicateShape : newShape        = duplicate_with_transform( animatedShape  )[1]
    else :              newShape        = animatedShape
    
    if targetJoints :   skinJoints      = targetJoints
    else :              skinJoints      = animatedJoints
    
    skinNode    = skin( newShape, skinJoints, weights, maxInf  )
    
    
    
    #**
    cmds.currentTime( frames[0] )
    
    res     = {'skinNode':      skinNode,
               'newShape':      newShape,
               'targetJoints':  targetJoints,
               'error':         error,
               'iterationDone': iterationDone, }
    
    return res


def run_cpp(    animatedShape,
                animatedJoints,
                frames,
                maxInf,
                maxIteration        = 1,
                iterationFullSolver = 1,
                errorPercentBreak   = 1.0,
                updateRestMatrices  = False,
                rigidMatrices       = True,
                setMatrices         = True,
                targetJoints        = None,
                vertexIds           = None,
                existingSkinCluster = None,
                maxCPU              = -1, ):


    from mca.mya.plugins import loader
    loader.load_skinning_converter_plugin()
    
    if not vertexIds :
        vertexIds   = get_vertexIds( animatedShape )
        
    vertexIds       = tuple( vertexIds )
    animatedJoints  = tuple( animatedJoints )
    frames          = tuple( [float(item) for item in frames] )
    
    
    if setMatrices and targetJoints :
        # if setMatrices is False, targetJoints are unused
        targetJoints    = tuple( targetJoints )
    
    
    numJnts         = len(animatedJoints)
    if maxInf > numJnts :
        maxInf      = numJnts
    
    
    #
    add_dict    = { 'shape':                'string',
                    'vertexIds':            'Int32Array',
                    'sourceJoints':         'stringArray',
                    'targetJoints':         'stringArray',
                    'setMatrices':          'bool',
                    'frames':               'doubleArray',
                    'maxInfluence':         'long',
                    'maxIteration':         'long',
                    'iterationFullSolver':  'long',
                    'updateRestMatrices':   'bool',
                    'rigidMatrices':        'bool',
                    'errorPercentBreak':    'double',
                    'lagragian':            'double',
                    'existingSkinCluster':  'string',
                    'maxCPU':               'long',
                    
                    # outputs
                    'weightIds':            ['Int32Array'],
                    'weights':              ['doubleArray'],
                    'error':                'double',
                    'iterationDone':        'long', }
    
    set_dict     = {'shape':                animatedShape,
                    'vertexIds':            vertexIds,
                    'sourceJoints':         animatedJoints,
                    'targetJoints':         targetJoints,
                    'setMatrices':          setMatrices,
                    'frames':               frames,
                    'maxInfluence':         maxInf,
                    'maxIteration':         maxIteration,
                    'iterationFullSolver':  iterationFullSolver,
                    'updateRestMatrices':   updateRestMatrices,
                    'rigidMatrices':        rigidMatrices,
                    'errorPercentBreak':    errorPercentBreak,
                    'lagragian':            1.0,
                    'existingSkinCluster':  existingSkinCluster,
                    'maxCPU':               maxCPU,}
    
    storageNode   = create_node( 'network', add_dict=add_dict, set_dict=set_dict )
    
    cmds.skinningDecomposition( storageNode = storageNode )
    
    
    
    # { vId:{ jntId: .5, jntId: .5 },   ... }
    weights     = {}
    
    for vId in vertexIds :
        wIds            = cmds.getAttr( storageNode + '.weightIds[%s]' %vId )
        wValues         = cmds.getAttr( storageNode + '.weights[%s]' %vId )
        
        if (not wIds) or (not wValues) or (len(wIds)!=len(wValues)):
            print('msh = %s\nvId = %s\nwIds = %s\nwValues = %s' %(animatedShape,vId,wIds,wValues))
            cmds.error('');return
        
        weights[vId]    = dict( zip(wIds, wValues) )
    
    error           = cmds.getAttr( storageNode + '.error')
    iterationDone   = cmds.getAttr( storageNode + '.iterationDone')
    
    
    #
    cmds.delete( storageNode  )
    
    return weights, error, iterationDone


def skin( onShape, joints, weights, maxInf ):
    '''vertexIds are included in weights now '''
    
    
    #** firstly dont normalize to avoid crappy warning messages
    normWgts        = True
    maintainMaxInf  = True
    
    
    cmds.delete( onShape, ch=True )
    
    skinNode    = cmds.skinCluster( onShape, joints, 
                        mi    = maxInf,
                        omi    = maintainMaxInf,
                        nw    = 0,
                        sm    = 0,
                        tsb    = True  ) [0]
    
    #set  :
    set_skin_weights( skinNode, weights  )
    
    
    #** normalize :
    if normWgts :
        cmds.skinCluster( skinNode, forceNormalizeWeights=True, edit=True )
        cmds.setAttr(  skinNode+'.normalizeWeights', normWgts   )
    
    return skinNode



def get_matching_percent( error ):
    return 100.0*(1.0-error)

