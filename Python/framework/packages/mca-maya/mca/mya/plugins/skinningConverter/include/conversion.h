



#include "stdafx.h"





bool is_unique_MIntArray( MIntArray& intArray);

bool is_unique_MStringArray( MStringArray& strArray );

bool is_unique_MDoublerray( MDoubleArray& dblArray);


int intVector_position( int& item, intVec& vec ) ;


void MStringArray_to_MStringVec( MStringArray& mStringArray, MStringVec& stringVec );

void intSet_to_intVec( intSet& set, intVec& vec );

void VectorXd_to_doubleVec(VectorXd& x, double epsilon, doubleVec& y ) ;

void intVec_to_MIntArray( intVec& vec, MIntArray& mint   );

void MIntArray_to_intVec(  MIntArray& mint, intVec& vec   );

void doubleVec_to_MDoubleArray( doubleVec& vec, MDoubleArray& mdbl );


EulerRo TransfoRo_to_EulerRo( TransfoRo& tro ) ;


