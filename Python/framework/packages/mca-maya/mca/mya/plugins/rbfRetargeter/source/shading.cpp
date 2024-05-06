
#include "shading.h"


#include <vector>

#include <maya/MSelectionList.h>

#include <maya/MFnDagNode.h>
#include <maya/MDagPath.h>

#include <maya/MFnSet.h>

#include <maya/MItMeshPolygon.h>






void assign_shaders( MObjectArray& shader_Objs, MIntArray& shaderIds_per_face, MObject& mshTR_Obj  )
{

	int numShader	= shader_Objs.length() ;


	if (numShader==1)
	{
		// if there is only one    assign all at once

		MFnSet shader_Set( shader_Objs[0] ) ;

		//shader_Set.addMember( msh_Obj );
		shader_Set.addMember( mshTR_Obj );
	}


	else
	{
		// else assign per faces
		

		//
		// NEVER use method .dagPath, it doesnt work
		MFnDagNode msh_DagNode( mshTR_Obj );

		MDagPath msh_Path ;
		msh_DagNode.getPath( msh_Path ) ;
		msh_Path.extendToShape() ;

		MItMeshPolygon iter( msh_Path );


		for (iter.reset(); !iter.isDone(); iter.next() )
		{
			int idx		= iter.index() ;
			int shaderId_for_this_face	= shaderIds_per_face[idx] ;
			//sets[ shaderId_for_this_face ].addMember( msh_Path, iter.currentItem() );

			MFnSet( shader_Objs[shaderId_for_this_face] ).addMember( msh_Path, iter.currentItem() ) ;
		}
		

		// do with another way,  because MFnSet doesnt work in vector ( they forgot to declare the "=" in the class )

		/*
		// build vector of SelectionList
		std::vector<MSelectionList> selectionLists ;
		selectionLists.resize( numShader ) ;

		for (int ii=0 ; ii<numShader; ii++)
		{
			MSelectionList sel ;
			selectionLists[ii]	= sel ;
		}


		// fill SelectionLists with components,   need dagPath
		// NEVER use method .dagPath, it doesnt work
		MFnDagNode msh_DagNode( mshTR_Obj );

		MDagPath msh_Path ;
		msh_DagNode.getPath( msh_Path ) ;
		msh_Path.extendToShape() ;

		MItMeshPolygon iter( msh_Path );


		for (iter.reset(); !iter.isDone(); iter.next() )
		{
			int idx		= iter.index() ;
			int shaderId_for_this_face	= shaderIds_per_face[idx] ;
			
			selectionLists[ shaderId_for_this_face ].add( msh_Path, iter.currentItem(), true );
		}


		// assign SelectionLists to MFnSets
		for (int ii=0 ; ii<numShader; ii++)
		{
			MFnSet shader_Set( shader_Objs[ii] ) ;

			shader_Set.addMembers( selectionLists[ii]  );
		}
		*/
	}

}
