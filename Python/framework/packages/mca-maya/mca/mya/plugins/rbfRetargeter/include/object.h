

#include <maya/MStringArray.h>
#include <maya/MObjectArray.h>




MStatus get_Obj_from_name( const MString& name, MObject& obj, MFn::Type checkFn );

MStatus get_Objs_from_names( const MStringArray& names, MObjectArray& objs, MFn::Type checkFn ) ;

