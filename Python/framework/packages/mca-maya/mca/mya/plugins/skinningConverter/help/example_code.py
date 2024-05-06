

import conversion
import decomposition




# in all the cases,  your animated shape MUST start on the first frame by its rest pose/shape
# Or by you consider as rest shape




# example 1

# I want to convert a shape/shapes   to bones + skinning
# inputs are animated shapes ( 1 shape, or N shapes )


animated_meshes = ['pSphereShape1']    # or ['...','...','...']
numJoint        = 40
maxInf          = 8
startFrame, endFrame	= 0, 100
frames         	= [ float(item) for item in xrange(startFrame, endFrame+1) ]
maxIteration    = 20

skinMeshes, newJoints, initJnts, error, iterDone  = conversion.perform( animated_meshes, numJoint, maxInf, frames, maxIteration,
		                                                                    errorPercentBreak   = errorPercentBreak,
                                                                            deleteInitJoints    = True,
                                                                            rigidMatrices       = rigidMatrices )



# example 2

# I want to get the best skinning  using existing animated bones, for example  facial blendShapes to skinning.
# You must create the bones, their movement  and  the shapes by your own way.


startFrame, endFrame	= 0, 725
frames         	= [ float(item) for item in xrange(startFrame, endFrame+1) ]
animatedShape  	= 'pSphereShape1'
vertexIds      	= get_vertexIds( animatedShape )
jnts 		   	= cmds.ls(sl=1)

maxInf   		= 8

decomposition.perform( animatedShape,
			vertexIds,
			jnts,
			frames,
			maxInf,

			duplicateShape     = True,
			duplicateJoints    = False,
			setMatrices		= False,  ) 



		
		
		
