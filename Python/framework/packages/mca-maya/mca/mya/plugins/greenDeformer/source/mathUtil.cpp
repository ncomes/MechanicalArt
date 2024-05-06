


#include "mathUtil.h"




double blend2( double& d0, double& d1, double& t )
{
	return ( (1.0-t)*d0 + t*d1  ) ;
}



MPoint	blend_2_MPoints( MPoint& pnt0, MPoint& pnt1, double t )
{
	return MPoint(	blend2( pnt0.x, pnt1.x, t ),
					blend2( pnt0.y, pnt1.y, t ),
					blend2( pnt0.z, pnt1.z, t ) );
}




double get_triangle_area( MPoint& A, MPoint& B, MPoint& C)
{
	return (.5 * ((B-A)^(C-A)).length()) ;
}



