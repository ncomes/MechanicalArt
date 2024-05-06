

#include "bezierPatch.h"



double lerp( double d0, double d1, double t )
{
	return ( (1.0-t)*d0 + t*d1  ) ;
}

MVector lerp_MVectors( MVector& v0, MVector& v1, double& t  )
{
	MVector v ;
	v.x		= lerp( v0.x, v1.x, t ) ;
	v.y		= lerp( v0.y, v1.y, t ) ;
	v.z		= lerp( v0.z, v1.z, t ) ;
	return v ;
}


double set_range( double x, double x0, double x1, double y0, double y1 )
{
	return  y0 + (x-x0)*(y1-y0)/(x1-x0)  ;
}


int ipow(int base, int exp)
// positive exp only
{
    int result = 1;
    while (exp)
    {
        if (exp & 1)
            result *= base;
        exp >>= 1;
        base *= base;
    }
    return result;
}




/*
void get_tangent( MPoint& p0, MPoint& p1, MVector& n,
					double& edge_ratio ,
					double& curvature_ratio ,
					MVector& tgt )
{
	MVector e_0_1	= p1-p0 ;


	if (curvature_ratio < epsilon)
	{
		tgt		= edge_ratio * e_0_1 ;
	}

	else 
	{
		MVector e_0_1_n		= e_0_1.normal() ;
		double e_len		= e_0_1.length() ;

		tgt		=  ((n ^ e_0_1_n) ^ n).normal() ;

		tgt		= lerp_MVectors( e_0_1_n, tgt,  curvature_ratio ) ;
		tgt.normalize() ;

		tgt		*=  e_len * edge_ratio ;
	}

}


extern Matrix4d H, Ht	;

void eval_hermite_patch(	MPoint& p00,	MPoint& p01,	MPoint& p10,	MPoint& p11,
							MVector& n00,	MVector& n01,	MVector& n10,	MVector& n11,
							MVector& tu00,	MVector& tu01,	MVector& tu10,	MVector& tu11,
							MVector& tv00,	MVector& tv01,	MVector& tv10,	MVector& tv11, 
							double& u, double& v, double& w,
							MPoint& p  )
{
	// Pnt(u,v) = Ut H B Ht V
	//
	// TgtU(u,v) = dUt H B Ht V
	// TgtV(u,v) = Ut H B Ht dV
	// Nrml(u,v) = TgtU(u,v) ^ TgtV(u,v)
	
	// H is hermite coefficient matrix
	Matrix4d H ; H <<	2,-2,1,1,
						-3,3,-2,-1,
						0,0,1,0,
						1,0,0,0 ;
	Matrix4d Ht		= H.transpose() ;
	

	// FU FV    FU' FV' (derivatives)
	RowVector4d Ut ;	Ut << u*u*u, u*u, u, 1 ;
	RowVector4d dUt ;	dUt << 3*u*u, 2*u, 1, 0 ;

	Vector4d V ;		V << v*v*v, v*v, v, 1  ;
	Vector4d dV ;		dV << 3*v*v, 2*v, 1, 0  ;


	// compute P.x y z  and  tgts.x y z
	MVector tgtU, tgtV ;

	//MVector d00		= tu00 ^ tv00 ;
	//MVector d01		= tu01 ^ tv01 ;
	//MVector d10		= tu10 ^ tv10 ;
	//MVector d11		= tu11 ^ tv11 ;

	for (int xx=0; xx<3; xx++)
	{
		// Geometry Matrix
		Matrix4d Bxx ; Bxx <<	p00[xx], p01[xx], tv00[xx], tv01[xx],
								p10[xx], p11[xx], tv10[xx], tv11[xx],
								tu00[xx], tu01[xx],	n00[xx], n01[xx],
								tu10[xx], tu11[xx],	n10[xx], n11[xx] ;

		Matrix4d H_Bxx_Ht	= H * Bxx * Ht ;

		// point and tgts
		//p[xx]		= Ut * H * Bxx * Ht * V ;
		p[xx]		= Ut  * H_Bxx_Ht * V ;
		tgtU[xx]	= dUt * H_Bxx_Ht * V ;
		tgtV[xx]	= Ut  * H_Bxx_Ht * dV ;
	}


	// nrm	= (tgtU ^ tgtV).normal() ;

	//double quad_area	= 

	p		+= w * (tgtV ^ tgtU).normal() ;  // V*U instead of U*V because of a bad sign somewhere and I dont care haaahahaahaa
}




void c_func( MVector& D, MVector& n0, MVector& n1,  MVector& res)
{
	MVector v	= .5*(n0 + n1) ;
	MVector dv	= .5*(n0 - n1) ; 
	double d	= D * v ;     
	double dd	= D * dv ;  
	double c	= n0 * ( n0 - (2.0*dv) ) ;
	
	if ( c < -1.0 + epsilon || c > 1.0 - epsilon )
		res = MVector::zero ;

	else  {
		double dc	= n0 * dv ;
		res		= ((dd / (1.0-dc)) * v)  +  ((d/dc) * dv) ;   }
}



void eval_nagata_quad_patch(	MPoint& p00,	MPoint& p01,	MPoint& p10,	MPoint& p11,
								MVector& n00,	MVector& n01,	MVector& n10,	MVector& n11,
								double& u, double& v, double& w,
								MPoint& p  )
// from Nagata white paper ...
{
	MVector d1	= p10 - p00 ;
	MVector d2	= p11 - p10 ;
	MVector d3	= p11 - p01 ;
	MVector d4	= p01 - p00 ;

	MVector c1	;  c_func( d1, n00, n10,  c1 );
	MVector c2	;  c_func( d2, n10, n11,  c2 );
	MVector c3	;  c_func( d3, n01, n11,  c3 );
	MVector c4	;  c_func( d4, n00, n01,  c4 );
	 
	MVector  c00( p00 );
	MVector  c10	= d1 - c1 ;
	MVector  c01	= d4 - c4 ;
	MVector  c11	= d2 - d4 + c1 - c2 - c3 + c4 ;
	MVector& c20	= c1 ;
	MVector& c02	= c4 ;
	MVector  c12	= c2 - c4 ;
	MVector  c21	= c3 - c1 ;

	// p	= c00 + c10*u + c01*v + c11*u*v + c20*u*u + c02*v*v + c21*u*u*v + c12*u*v*v ; 

	// tangents = partial derivation u and v
	// tu	= 0   + c10   + 0     + c11*v   + 2*c20*u + 0       + 2*c21*v*u + c12*v*v   ;
	// tv	= 0   + 0     + c01   + c11*u   + 0       + 2*c02*v + c21*u*u   + 2*c12*u*v ;

	MVector tgtU, tgtV ;

	for (int xx=0; xx<3; xx++) {
		p[xx]	= c00[xx] + c10[xx]*u + c01[xx]*v + c11[xx]*u*v + c20[xx]*u*u + c02[xx]*v*v + c21[xx]*u*u*v + c12[xx]*u*v*v ;

		tgtU[xx]= 0	  + c10[xx]   + 0     + c11[xx]*v   + 2*c20[xx]*u + 0       + 2*c21[xx]*v*u + c12[xx]*v*v   ;
		tgtV[xx]= 0   + 0     + c01[xx]   + c11[xx]*u   + 0       + 2*c02[xx]*v + c21[xx]*u*u   + 2*c12[xx]*u*v ;
	}

	//
	p	+= w * (tgtV ^ tgtU).normal() ;

}

*/



double distance_2d( doubleVec& p0, doubleVec& p1 )
{
	return sqrt( (p1[0]-p0[0])*(p1[0]-p0[0]) + (p1[1]-p0[1])*(p1[1]-p0[1]) );
}


double triangle_area( doubleVec& p0, doubleVec& p1, doubleVec& p2 )
{
	double a = distance_2d( p0, p1  ) ;
	double b = distance_2d( p0, p2  ) ;
	double c = distance_2d( p1, p2  ) ;

	double s = (a + b + c) / 2.0;
	return sqrt(s*(s - a)*(s - b)*(s - c)) ;
}



void get_generalized_barycentric(	doubleVec& p,
									doubleVecVec& pnts,	// = p00, p10, p11, p01  in this order
									doubleVec& barys )
// the point MUST BE ON the polygon otherwise the following formula does not work.
// In this plugin it's 2D so no problem.
{

	//  10 ---- 11      3 ---- 2     v            x
	//  .       .       .      .     .            .
	//  .       .       .      .     .            .
	//  00 ---- 10      0 ---- 1     ...... u     ...... z    z-x  because Maya axis are like that (right hand)

	barys.resize( 4 );

	intVec next_ids( 4 );
	intVec prev_ids( 4 );
	for (int ii=0; ii<4; ii++) {
		next_ids[ii]	= (ii+1)%4 ;
		prev_ids[ii]	= (ii+4-1)%4 ; }


	//
	doubleVec As( 4 );
	doubleVec Cs( 4 );
	for (int ii=0; ii<4; ii++) {
		As[ii]	= triangle_area( p, pnts[ii], pnts[next_ids[ii]]) ;
		Cs[ii]	= triangle_area( pnts[ii], pnts[next_ids[ii]], pnts[prev_ids[ii]]  );  }

	//
	doubleVec ws( 4 );
	double w_sum	= .0 ;

	for (int ii=0; ii<4; ii++) {
		ws[ii]			= Cs[ii] * As[next_ids[ii]] * As[next_ids[next_ids[ii]]] ;
		w_sum			+= ws[ii] ; }

	for (int ii=0; ii<4; ii++) {
		barys[ii]	= ws[ii] / w_sum ; }
}



void eval_bary( MPoint&  p00, MPoint&    p10, MPoint&    p11, MPoint&    p01,
				MVector& n00, MVector&   n10, MVector&   n11, MVector&   n01,
				double&  bary00, double& bary10, double& bary11, double& bary01,
				MPoint& p )
{

	// reset
	p.x=.0; p.y=.0; p.z=.0;

	// Point reproduction
	// Linear normal interpolation (phong normal)
	MVector n ;
	for (int xx=0; xx<3; xx++) {
		p[xx]	+= p00[xx]*bary00 + p10[xx]*bary10 + p11[xx]*bary11 + p01[xx]*bary01   ;
		n[xx]	+= n00[xx]*bary00 + n10[xx]*bary10 + n11[xx]*bary11 + n01[xx]*bary01   ; }




}



/*

void eval_phong(	MPoint& p00,	MPoint& p10,	MPoint& p11,	MPoint& p01,
					MVector& n00,	MVector& n10,	MVector& n11,	MVector& n01,  MVector& face_nrm,
					MPoint& cloned_Pnt,
					double& bary00, double& bary10, double& bary11, double& bary01,
					MPoint& p  )
{
	// reset
	p.x=.0; p.y=.0; p.z=.0;

	// Point reproduction
	// Linear normal interpolation
	MVector n ;
	for (int xx=0; xx<3; xx++) {
		p[xx]	+= p00[xx]*bary00 + p10[xx]*bary10 + p11[xx]*bary11 + p01[xx]*bary01   ;
		n[xx]	+= n00[xx]*bary00 + n10[xx]*bary10 + n11[xx]*bary11 + n01[xx]*bary01   ; }

	//n.normalize() ;



	//  10 ---- 11      3 ---- 2     v            x
	//  .       .       .      .     .            .
	//  .       .       .      .     .            .
	//  00 ---- 10      0 ---- 1     ...... u     ...... z    z-x  because Maya axis are like that (right hand)

	double& u	= cloned_Pnt.z ;
	double& v	= cloned_Pnt.x ;
	double h	= cloned_Pnt.y ;


	// I need 3 info
	//double dot_n_fn		= n * face_nrm ;
	
	MVector& corner_nrm ;
	if		(u<.5 && v<.5)
	{
		corner_nrm=n00;



	}
	else if (u>.5 && v<.5)	{ corner_nrm=n10; }
	else if (u>.5 && v>.5)	{ corner_nrm=n11; }
	else if (u<.5 && v>.5)	{ corner_nrm=n01; }

	double dot_n_u	= n * 
	double dot_n_v	= 


	//double inv_dot	= 1.0 / (n * face_nrm)  ;
	//h	*= inv_dot ;

	p	+= h * n ;

}





bool intersection_line_line(	MPoint& p1, MVector& v1,  MPoint& p2, MVector& v2,
								MPoint& inter  )
	// true if they are intersected, false else.
{
    MVector	w	= p1 - p2 ;
    double	a	= v1 * v1 ;			// always >= 0
    double	b	= v1 * v2 ;
    double	c	= v2 * v2 ;			// always >= 0
    double	d	= v1 * w ;
    double	e	= v2 * w ;
    double	D	= a*c - b*b ;		// always >= 0
    double  sc, tc;


    // compute the line parameters of the two closest points
    if (D < epsilon) {					// the lines are almost parallel
        sc		= 0.0;
		tc		= b>c ? d/b : e/c ; }	// use the largest denominator
    else {
        sc		= (b*e - c*d) / D ;
        tc		= (a*e - b*d) / D ; }


    //
	MPoint inter1	= p1 + (sc * v1) ;
	MPoint inter2	= p2 + (tc * v2) ;
    //MVector   dP = w + (sc * v1) - (tc * v2);  // =  L1(sc) - L2(tc)


	if (inter1.distanceTo(inter2) < epsilon) {
		inter	= inter1 ;
		return true ;}

	else  {
		inter.x		= .5*(inter1.x + inter2.x) ;
		inter.y		= .5*(inter1.y + inter2.y) ;
		inter.z		= .5*(inter1.z + inter2.z) ;
		return false ; }
}



void get_middle_point(	MPoint& p03,  MPoint& p01,	MPoint& p00,	MPoint& p10,	MPoint& p30,
						MVector& n03,				MVector& n00,					MVector& n30,
						MPoint& p11 )
{

	MVector edge_normal_1	= (n00 + n03).normal() ;
	MVector dir_01			= edge_normal_1 ^ n00 ;

	MVector edge_normal_2	= (n00 + n30).normal() ;
	MVector dir_10			= edge_normal_2 ^ n00 ;

	MPoint inter ;
	bool is_intersection	= intersection_line_line( p01, dir_01, p10, dir_10,  inter  );

	if (!is_intersection) {
		// shiiiit
	}

	p11		= inter ;
}




void eval_bezier_curve( MPoint& p0, MPoint& p1, MPoint& p2, MPoint& p3,
						double &t,
						MPoint& p ) 
{ 
    double b0	= (1 - t) * (1 - t) * (1 - t); 
    double b1	= 3 * t * (1 - t) * (1 - t); 
    double b2	= 3 * t * t * (1 - t); 
    double b3	= t * t * t; 

	p.x		= b0*p0.x + b1*p1.x + b2*p2.x + b3*p3.x ;
	p.y		= b0*p0.y + b1*p1.y + b2*p2.y + b3*p3.y ;
	p.z		= b0*p0.z + b1*p1.z + b2*p2.z + b3*p3.z ;
} 
 
void eval_bezier_tangent( MPoint& p0, MPoint& p1, MPoint& p2, MPoint& p3,
						double &t,
						MVector& n)
{
	double b0	= -3*(1 - t)*(1 - t) ;
	double b1	= 3*(t - 1) * (3*t - 1) ;
	double b2	= 6*t - 9*t*t ;
	double b3	= 3*t*t ;

	n.x		= b0*p0.x + b1*p1.x + b2*p2.x + b3*p3.x ;
	n.y		= b0*p0.y + b1*p1.y + b2*p2.y + b3*p3.y ;
	n.z		= b0*p0.z + b1*p1.z + b2*p2.z + b3*p3.z ;
}


void eval_bezier_patch(		MPoint& p00, MPoint& p01, MPoint& p02, MPoint& p03,
							MPoint& p10, MPoint& p11, MPoint& p12, MPoint& p13,
							MPoint& p20, MPoint& p21, MPoint& p22, MPoint& p23,
							MPoint& p30, MPoint& p31, MPoint& p32, MPoint& p33,
							double &u,  double &v, double &w,
							MPoint& p ) 
	// w is the height
{ 
	MPoint uCurve0  ;  eval_bezier_curve( p00, p01, p02, p03,  u, uCurve0 ) ;
	MPoint uCurve1  ;  eval_bezier_curve( p10, p11, p12, p13,  u, uCurve1 ) ;
	MPoint uCurve2  ;  eval_bezier_curve( p20, p21, p22, p23,  u, uCurve2 ) ;
	MPoint uCurve3  ;  eval_bezier_curve( p30, p31, p32, p33,  u, uCurve3 ) ;

    eval_bezier_curve( uCurve0, uCurve1, uCurve2, uCurve3, v, p ); 


	// I need 2 tangents :

	MVector tv  ;  eval_bezier_tangent( uCurve0, uCurve1, uCurve2, uCurve3, v, tv ); 

	MPoint vCurve0  ;  eval_bezier_curve( p00, p10, p20, p30,  v, vCurve0 ) ;
	MPoint vCurve1  ;  eval_bezier_curve( p01, p11, p21, p31,  v, vCurve1 ) ;
	MPoint vCurve2  ;  eval_bezier_curve( p02, p12, p22, p32,  v, vCurve2 ) ;
	MPoint vCurve3  ;  eval_bezier_curve( p03, p13, p23, p33,  v, vCurve3 ) ;

	MVector tu  ;  eval_bezier_tangent( vCurve0, vCurve1, vCurve2, vCurve3, u, tu ); 
	

	//p	+= w * (tu^tv).normal() ;
} 

*/



