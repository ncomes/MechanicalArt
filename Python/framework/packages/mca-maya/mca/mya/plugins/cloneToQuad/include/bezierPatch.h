

#include "stdafx.h"


double lerp( double d0, double d1, double t ) ;

MVector lerp_MVectors( MVector& v0, MVector& v1, double& t  ) ;

double set_range( double x, double x0, double x1, double y0, double y1 ) ;

int ipow(int base, int exp);



void get_tangent( MPoint& p0, MPoint& p1, MVector& n,
					double& edge_ratio ,
					double& curvature_ratio,
					MVector& t ) ;


void eval_hermite_patch(	MPoint& p00,	MPoint& p01,	MPoint& p10,	MPoint& p11,
							MVector& n00,	MVector& n01,	MVector& n10,	MVector& n11,
							MVector& tu00,	MVector& tu01,	MVector& tu10,	MVector& tu11,
							MVector& tv00,	MVector& tv01,	MVector& tv10,	MVector& tv11, 
							double& u, double& v, double& w,
							MPoint& p  );





bool intersection_line_line(	MPoint& p1, MVector& v1,  MPoint& p2, MVector& v2,
								MPoint& inter  ) ;

void get_middle_point(	MPoint& p03,  MPoint& p01,	MPoint& p00,	MPoint& p10,	MPoint& p30,
						MVector& n03,				MVector& n00,					MVector& n30,
						MPoint& p11 ) ;



void eval_bezier_curve( MPoint& p0, MPoint& p1, MPoint& p2, MPoint& p3,
						double &t,
						MPoint& p )  ;

void eval_bezier_tangent( MPoint& p0, MPoint& p1, MPoint& p2, MPoint& p3,
						double &t,
						MVector& n) ;

void eval_bezier_patch(		MPoint& p00, MPoint& p01, MPoint& p02, MPoint& p03,
							MPoint& p10, MPoint& p11, MPoint& p12, MPoint& p13,
							MPoint& p20, MPoint& p21, MPoint& p22, MPoint& p23,
							MPoint& p30, MPoint& p31, MPoint& p32, MPoint& p33,
							double &u,  double &v, double &w,
							MPoint& p )   ;



void c_func( MVector& D, MVector& n0, MVector& n1,  MVector& res) ;

void eval_nagata_quad_patch(	MPoint& p00,	MPoint& p01,	MPoint& p10,	MPoint& p11,
								MVector& n00,	MVector& n01,	MVector& n10,	MVector& n11,
								double& u, double& v, double& w,
								MPoint& p  ) ;


double distance_2d( doubleVec& p0, doubleVec& p1 );

double triangle_area( doubleVec& p0, doubleVec& p1, doubleVec& p2 );

void get_generalized_barycentric(	doubleVec& p,
									doubleVecVec& pnts,	// = p00, p10, p11, p01  in this order
									doubleVec& barys ) ;

void eval_bary( MPoint&  p00, MPoint&    p10, MPoint&    p11, MPoint&    p01,
				MVector& n00, MVector&   n10, MVector&   n11, MVector&   n01,
				double&  bary00, double& bary10, double& bary11, double& bary01,
				MPoint& p );


void eval_phong(	MPoint& p00,	MPoint& p10,	MPoint& p11,	MPoint& p01,
					MVector& n00,	MVector& n10,	MVector& n11,	MVector& n01,  MVector& face_nrm,
					MPoint& cloned_Pnt,
					double& bary00, double& bary10, double& bary11, double& bary01,
					MPoint& p  ) ;

