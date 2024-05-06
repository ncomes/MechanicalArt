


#include "stdafx.h"



MStatus get_Obj(  MString& name, MObject& obj, MFn::Type checkFn );

MStatus get_Objs(  MStringVec& names, MObjectArray& objs, MFn::Type checkFn );



MStringArray attribute_strings_to_disconnect() ;
MStringArray attribute_strings_to_animate(bool& rigid) ;


void disconnect_input_connections( MFnDagNode& dagNode, MStringArray& attrs, MDGModifier& modifier  ) ;

void create_animCurves( MFnDagNode& dagNode, MStringArray& attrs,  MObjectVec& animCurves_Objs ) ;

void set_animCurves(	MMatrix& mm,
						MObjectVec& animCurves_Objs,
						EulerRo& ro,
						MTime& time) ;

