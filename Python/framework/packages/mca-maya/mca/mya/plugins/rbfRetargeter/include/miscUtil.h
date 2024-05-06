

#include <maya/MObject.h>
#include <maya/MObjectArray.h>
#include <maya/MBoundingBox.h>

#include <maya/MIntArray.h>
#include <maya/MPointArray.h>
#include <maya/MPoint.h>


MBoundingBox merge_AABB( MObject& obj0, MObjectArray& objs ) ;

MPointArray points_on_sphere( unsigned int numPnt, double scale[3], MPoint center );

MPointArray get_volume_pnts( MObjectArray& objs ) ;



double get_radius_and_center( MObjectArray& objs,  MPoint& out_center  ) ;

void get_spheres( double radius1, double radius2, MPoint& center1, MPoint& center2,  MPointArray& out_sphere_Pnts1, MPointArray& out_sphere_Pnts2, int& sphere_len  ) ;

void build_spheres(	MPointArray& used_src_Pnts, MPointArray& used_tgt_Pnts,
					MObject& source_Obj, MObjectArray& shape_Objs, MObject& target_Obj,
					int& sphere_len );

MIntArray range( int x ) ;

