



#include "conversion.h"





bool is_int_in_mapFirst( int key, MIntArrayMap& myMap )
{

	MIntArrayMap::iterator it	= myMap.find( key );

	if (it == myMap.end() )
	{	return false ; }

	return true ;
}



