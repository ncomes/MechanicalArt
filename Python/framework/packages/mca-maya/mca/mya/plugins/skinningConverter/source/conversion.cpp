


#include "conversion.h"





bool is_unique_MIntArray( MIntArray& intArray)
{
	int num = intArray.length() ;

	std::set<int> set ;

	for (int ii=0;ii<num;ii++) {
		set.insert( intArray[ii] ); }

	if (set.size() != num){
		return false ; }

	return true ;
}

bool is_unique_MStringArray( MStringArray& strArray )
{
	int num		= strArray.length();

	for(int ii=0; ii<num; ++ii) {
		for(int jj=ii+1; jj<num; ++jj) {
			if(strArray[ii] == strArray[jj]) return false;
		}
	}
	return true;
}


bool is_unique_MDoublerray( MDoubleArray& dblArray)
{
	int num = dblArray.length() ;

	std::set<double> set ;

	for (int ii=0;ii<num;ii++) {
		set.insert( dblArray[ii] ); }

	if (set.size() != num){
		return false ; }

	return true ;
}





int intVector_position( int& item, intVec& vec )
{

	intVec::iterator it	= std::find(vec.begin (),vec.end(), item);

	if (it == vec.end()) {
		return -1 ; }

	return (int) std::distance( vec.begin(), it ) ;
}




void MStringArray_to_MStringVec( MStringArray& mStringArray, MStringVec& stringVec )
{
	int num		= mStringArray.length();
	stringVec.resize( num );

	for (int ii=0; ii<num; ii++)
	{
		stringVec[ii]	= mStringArray[ii] ;
	}
}

void intSet_to_intVec( intSet& set, intVec& vec )
{
	
	//int num		= (int) set.size() ;
	//vec.resize( num );
	/*
	int ii = 0 ;
	for (intSet::iterator it=set.begin(); it!=set.end(); it++)
	{
		vec[ii++]	= it.
	}
	*/

	//std::copy(set.begin(), set.end(), vec.begin());

	vec.assign( set.begin(), set.end() );
}

void VectorXd_to_doubleVec(VectorXd& x, double epsilon, doubleVec& y )
{
	// clamp
	int num		= (int) x.rows() ;
	y.resize( num ) ;

	double sum	= .0 ;


	for (int ii=0; ii<num;ii++)
	{
		if (x(ii) < epsilon) {
			y[ii]	= .0 ; }
		else {
			y[ii]	= x(ii) ;
			sum		+= y[ii] ;}
	}

	// normalize
	for (int ii=0; ii<num;ii++) {
		y[ii]	/= sum ; }
}



void intVec_to_MIntArray( intVec& vec, MIntArray& mint   )
{
	int num		= (int) vec.size();
	mint.setLength(  num );

	for (int ii=0; ii<num; ii++)
	{
		mint[ii]	= vec[ii] ;
	}
}

void MIntArray_to_intVec(  MIntArray& mint, intVec& vec   )
{
	int num		= mint.length();
	vec.resize(  num );

	for (int ii=0; ii<num; ii++)
	{
		vec[ii]	= mint[ii] ;
	}
}



void doubleVec_to_MDoubleArray( doubleVec& vec, MDoubleArray& mdbl   )
{
	int num		= (int) vec.size();
	mdbl.setLength(  num );

	for (int ii=0; ii<num; ii++)
	{
		mdbl[ii]	= vec[ii] ;
	}
}




EulerRo TransfoRo_to_EulerRo( TransfoRo& tro )
{
	if (tro==MTransformationMatrix::kXYZ )		{return MEulerRotation::kXYZ  ; }
	else if (tro==MTransformationMatrix::kYZX ) {return MEulerRotation::kYZX  ; }
	else if (tro==MTransformationMatrix::kZXY ) {return MEulerRotation::kZXY  ; }
	else if (tro==MTransformationMatrix::kXZY ) {return MEulerRotation::kXZY  ; }
	else if (tro==MTransformationMatrix::kYXZ ) {return MEulerRotation::kYXZ  ; }
	else										{return MEulerRotation::kZYX  ; }
}










