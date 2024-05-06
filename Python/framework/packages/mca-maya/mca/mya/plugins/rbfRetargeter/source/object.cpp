


#include "object.h"

#include <maya/MSelectionList.h>
#include <maya/MGlobal.h>




MStatus get_Obj_from_name( const MString& name, MObject& obj, MFn::Type checkFn=MFn::kBase )
//
{
	MSelectionList sel ;
	MStatus status	= MStatus::kSuccess;

	status		= sel.add( name ) ;

	if (status!=MStatus::kSuccess)
	{
		MString error("Node does not exist : ") ; error+=name;
		MGlobal::displayInfo( error );
		return MStatus::kFailure ;
	}

	// check if hasFn==kMEsh
	sel.getDependNode( 0, obj );
	
	if ( obj.hasFn( checkFn ) != true )
	{
		MString error("Node must have specified Fn, check this : ") ; error+=name;
		MGlobal::displayInfo( error );
		return MStatus::kFailure ;
	}

	return MStatus::kSuccess ;
}



MStatus get_Objs_from_names( const MStringArray& names, MObjectArray& objs, MFn::Type checkFn=MFn::kBase )
//
// fill input objs, return kFailure if ony one name doesnt exist
{
	int num		= names.length();
	objs.setLength( num );


	MSelectionList sel ;
	MStatus status	= MStatus::kSuccess;


	for (int ii=0 ; ii<num; ii++)
	{
		//
		status		= sel.add( names[ii] ) ;

		if (status!=MStatus::kSuccess)
		{
			MString error("All arguments must be different existing nodes, check this : ") ; error+=names[ii];
			MGlobal::displayInfo( error );
			return MStatus::kFailure ;
		}

		
		// check if hasFn==kMEsh
		MObject obj ;
		sel.getDependNode( ii, obj );
		
		if ( obj.hasFn( checkFn ) != true )
		{
			MString error("All arguments must have Fn==kMesh, check this : ") ; error+=names[ii];
			MGlobal::displayInfo( error );
			return MStatus::kFailure ;
		}


		// else
		objs[ii]	= obj ;
	}

	return status ;
}














