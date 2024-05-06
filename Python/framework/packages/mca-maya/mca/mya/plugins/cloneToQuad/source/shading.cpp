



#include "shading.h"





void get_shaders( MObject& msh_Obj,   MObjectArray& shaders, MIntArray& shaderPerPoly )
{
	MFnDagNode msh_DagNode( msh_Obj );
	MDagPath msh_Path  ;  msh_DagNode.getPath( msh_Path ) ;

	// 0 = instanceNumber
	MFnMesh( msh_Path ).getConnectedShaders( 0, shaders, shaderPerPoly );
}



void assign_shaders( MObjectArray& shader_Objs, MIntArray& shaderIds_per_face, MObject& mshObj )
{

	int numShader	= shader_Objs.length() ;


	if (numShader==1)
	{
		// if there is only one    assign all at once

		MFnSet shader_Set( shader_Objs[0] ) ;

		shader_Set.addMember( mshObj );
	}


	else
	{
		// else assign per faces
		MFnDagNode msh_DagNode( mshObj );

		//////
		MDagPath msh_Path ;
		msh_DagNode.getPath( msh_Path ) ;
		//msh_Path.extendToShape() ;

		//MItMeshPolygon iter( msh_Path );
		//////

		MItMeshPolygon iter( mshObj );


		for (iter.reset(); !iter.isDone(); iter.next() )
		{
			int idx			= iter.index() ;
			int& shaderId	= shaderIds_per_face[idx] ;

			MFnSet( shader_Objs[shaderId] ).addMember( msh_Path, iter.currentItem() ) ;
		}
		

	}

}









