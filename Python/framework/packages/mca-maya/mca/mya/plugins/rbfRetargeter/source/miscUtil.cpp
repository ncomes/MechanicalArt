
#include "miscUtil.h"

#include <maya/MFnDagNode.h>
#include <maya/MBoundingBox.h>

#include <algorithm>




MBoundingBox merge_AABB( MObjectArray& objs )
{
	MFnDagNode dag0( objs[0]  ) ;

	MBoundingBox bb		= dag0.boundingBox() ;


	if (objs.length()==1)
	{
		return bb ;
	}

	else // >1
	{
		for (unsigned int ii=1 ; ii<objs.length(); ii++)
		{
			MFnDagNode dagn( objs[ii] ) ;
	
			bb.expand( dagn.boundingBox() ) ;
		}


		return bb ;
	}
	
}




MPointArray points_on_sphere( int numPnt, double scale[3], MPoint center )
{
	MPointArray pnts( numPnt ) ;

	double N	= (double)numPnt ;

	double pi	= 3.14159265358979323846 ;

	double inc	= pi * (3.0 - sqrt(5.0)) ;
	double off	= 2.0 / N ;

	
	for (int kk=0; kk<numPnt; kk++)
	{
		double y	= kk * off - 1.0 + (off / 2.0) ;
		double r	= sqrt(1.0 - y*y) ;
		double phi	= kk * inc ;
		
		pnts.set( kk, (center[0]+scale[0]*cos(phi)*r), (center[1]+scale[1]*y), (center[2]+scale[2]*sin(phi)*r)  ) ;
	}

	return pnts ;
}



MPointArray get_volume_pnts( MObjectArray& objs )
{

	MBoundingBox bb		= merge_AABB( objs );

	MPoint mid			= bb.center() ;
	MPoint max			= bb.max() ;
	double radius		= sqrt( (mid[0]-max[0])*(mid[0]-max[0])+(mid[1]-max[1])*(mid[1]-max[1])+(mid[2]-max[2])*(mid[2]-max[2])) ;

	radius	*= 3.0 ;

	double scale[3]	= {radius,radius,radius} ;

	return points_on_sphere( 200, scale, mid ) ;
}



double get_radius_and_center( MObjectArray& objs,  MPoint& out_center )
{

	MBoundingBox bb		= merge_AABB( objs );

	MPoint mid			= bb.center() ;
	MPoint max			= bb.max() ;
	double radius		= sqrt( (mid[0]-max[0])*(mid[0]-max[0])+(mid[1]-max[1])*(mid[1]-max[1])+(mid[2]-max[2])*(mid[2]-max[2])) ;

	
	// out
	out_center		= mid ;

	return radius ;
}




void get_spheres( double radius1, double radius2, MPoint& center1, MPoint& center2,  MPointArray& out_sphere_Pnts1, MPointArray& out_sphere_Pnts2,
					int& sphere_len )
{

	// get max radius  and build the 2 sphere points   on the 2 centers
	double maxRad	= std::max( radius1, radius2 ) ;
	maxRad			*= 3.0 ;


	double scale[3]	= {maxRad,maxRad,maxRad} ;

	out_sphere_Pnts1	= points_on_sphere( sphere_len, scale, center1 ) ;
	out_sphere_Pnts2	= points_on_sphere( sphere_len, scale, center2 ) ;
}




void build_spheres(	MPointArray& used_src_Pnts, MPointArray& used_tgt_Pnts,
					MObject& source_Obj, MObjectArray& shape_Objs, MObject& target_Obj,
					int& sphere_len )
{
	// build  sphere points around all the source+shapes  to allow the max volume possible for the RBF
	// and a second sphere as target points

	int src_len		= used_src_Pnts.length() ;

	MObjectArray tmp1_Objs( shape_Objs ) ;
	tmp1_Objs.insert( source_Obj, 0 ) ;

	MObjectArray tmp2_Objs( 1 ) ;
	tmp2_Objs[0]	= target_Obj ;

	
	MPoint center1_Pnt ;
	double radius1	= get_radius_and_center( tmp1_Objs,  center1_Pnt ) ;

	MPoint center2_Pnt ;
	double radius2	= get_radius_and_center( tmp2_Objs,  center2_Pnt ) ;

	
	MPointArray volume1_Pnts ;
	MPointArray volume2_Pnts ;
	get_spheres( radius1, radius2, center1_Pnt, center2_Pnt,  volume1_Pnts, volume2_Pnts, sphere_len );



	// merge all vert to a new List
	used_src_Pnts.setLength( src_len + sphere_len );
	used_tgt_Pnts.setLength( src_len + sphere_len );

	for (int ii=0; ii<sphere_len; ii++) {
		used_src_Pnts[src_len+ii]	= volume1_Pnts[ii] ;
		used_tgt_Pnts[src_len+ii]	= volume2_Pnts[ii] ; }
}



MIntArray range( int x )
{
	MIntArray v ;
	v.setLength( x );

	for (int ii=0;ii<x;ii++)
	{
		v.set( ii, ii );
	}

	return v ;
}
