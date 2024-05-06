

#include "object.h"





MStatus get_Obj( MString& name, MObject& obj, MFn::Type checkFn=MFn::kBase )
//
{
	MSelectionList sel ;
	MStatus status	= MStatus::kSuccess;

	status		= sel.add( name ) ;

	if (status!=MStatus::kSuccess)
	{
		MString error("Node does not exist : ") ; error+=name;
		MGlobal::displayInfo( error );
		return MStatus::kUnknownParameter ;
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




MStatus get_Objs( MStringVec& names, MObjectArray& objs, MFn::Type checkFn=MFn::kBase )
//
// fill input objs, return kFailure if ony one name doesnt exist
{
	int num		= (int) names.size();
	objs.setLength( num );


	MSelectionList sel ;
	MStatus status	= MStatus::kSuccess;


	for (int ii=0 ; ii<num; ii++)
	{
		//
		status		= sel.add( names[ii] ) ;

		if (status!=MStatus::kSuccess)
		{
			MString error("Node does not exist : ") ; error+=names[ii];
			MGlobal::displayError( error );
		}

		
		// check if hasFn==kMEsh
		MObject obj ;
		sel.getDependNode( ii, obj );
		
		if ( obj.hasFn( checkFn ) != true )
		{
			MString error("Node must have specified Fn, check this : ") ; error+=names[ii];
			MGlobal::displayError( error );
		}


		// else
		objs[ii]	= obj ;
	}

	return status ;
}





MStringArray attribute_strings_to_disconnect()
{
	MStringArray attrs ;

	attrs.append( "t" );
	attrs.append( "tx" );
	attrs.append( "ty" );
	attrs.append( "tz" );
	attrs.append( "r" );
	attrs.append( "rx" );
	attrs.append( "ry" );
	attrs.append( "rz" );

	// flexible
	attrs.append( "s" );
	attrs.append( "sx" );
	attrs.append( "sy" );
	attrs.append( "sz" );
	attrs.append( "sh" );
	attrs.append( "shxy" );
	attrs.append( "shxz" );
	attrs.append( "shyz" );

	return attrs ;
}

MStringArray attribute_strings_to_animate( bool& rigid)
{
	MStringArray attrs ;

	attrs.append( "tx" );
	attrs.append( "ty" );
	attrs.append( "tz" );
	attrs.append( "rx" );
	attrs.append( "ry" );
	attrs.append( "rz" );

	// flexible
	if (rigid==false)
	{
		attrs.append( "sx" );
		attrs.append( "sy" );
		attrs.append( "sz" );
		attrs.append( "shxy" );
		attrs.append( "shxz" );
		attrs.append( "shyz" );
	}

	return attrs ;
}



void disconnect_input_connections( MFnDagNode& dagNode, MStringArray& attrs, MDGModifier& modifier  )
{
	for (unsigned int ii=0; ii<attrs.length(); ii++)
	{
		MPlug plug	= dagNode.findPlug( attrs[ii]  ) ;

		MPlugArray source_Plugs ;
		plug.connectedTo( source_Plugs,true,false);

		if (source_Plugs.length() >0) {
			modifier.disconnect( source_Plugs[0], plug ); }
	}
}


void create_animCurves( MFnDagNode& dagNode, MStringArray& attrs, MObjectVec& animCurves_Objs )
{
	unsigned int num	= attrs.length() ;
	animCurves_Objs.resize( num );

	for (unsigned int ii=0; ii<num; ii++)
	{
		MPlug plug	= dagNode.findPlug( attrs[ii]  ) ;
		
		if (!plug.isKeyable()) {
			plug.setKeyable(true); }

		MFnAnimCurve animCurve ;
		animCurves_Objs[ii]		= animCurve.create( plug);
	}
}


void set_animCurves(	MMatrix& mm,
						MObjectVec& animCurves_Objs,
						EulerRo& ro,
						MTime& time )
{
	
	// dim attrs = dim animCurves_Objs
	int dim		= (int) animCurves_Objs.size() ;
	doubleVec values( dim ) ;


	// get translation
	values[0]	= mm(3,0);
	values[1]	= mm(3,1);
	values[2]	= mm(3,2);
	

	// get rotation euler
	MTransformationMatrix transfo( mm ) ;
	MEulerRotation euler	= transfo.eulerRotation() ; // kXYZ

	if (ro != MEulerRotation::kXYZ ) {
		euler.reorderIt( ro ); }

	values[3]	= euler.x ;
	values[4]	= euler.y ;
	values[5]	= euler.z ;


	// get scale + shear
	if (dim==12)
	{
		double scale[3] ;
		transfo.getScale( scale, MSpace::kTransform );
		values[6]	= scale[0] ;
		values[7]	= scale[1] ;
		values[8]	= scale[2] ;

		double shear[3] ;
		transfo.getShear( shear, MSpace::kTransform );
		values[9]	= shear[0] ;
		values[10]	= shear[1] ;
		values[11]	= shear[2] ;
	}


	// set key for each animCurve
	for ( int ii=0; ii<dim; ii++)
	{
		MFnAnimCurve( animCurves_Objs[ii] ).addKey( time, values[ii] );
	}

}






