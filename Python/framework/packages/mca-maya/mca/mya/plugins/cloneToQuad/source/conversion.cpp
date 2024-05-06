


#include "conversion.h"





int vecPairII_position( pairII& item, vecPairII& vec )
{
	vecPairII::iterator it	= std::find(vec.begin (),vec.end(), item);

	if (it == vec.end()) {
		return -1 ; }

	return (int) std::distance( vec.begin(), it ) ;
}



void range_MIntArray( int fromVal, int toVal, MIntArray& ranged )
{
	int num		= toVal - fromVal ;
	ranged.setLength( num ) ;

	for (int ii=0; ii<num; ii++) {
		ranged.set( fromVal+ii , ii ); }
}











