

#include "retargetShapes.h"

#include <maya/MFnPlugin.h>



MStatus initializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj, "Hans Godard", "1.0", "Any");
        
	status = plugin.registerCommand( RetargetShapes::name, RetargetShapes::creator, RetargetShapes::newSyntax  );
	//status = plugin.registerCommand( RetargetShapes::name, RetargetShapes::creator  );
	if (!status) {
			status.perror("registerCommand");
			return status;
	}
	return status;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );
        
	status = plugin.deregisterCommand( RetargetShapes::name );
	if (!status) {
			status.perror("deregisterCommand");
			return status;
	}
	return status;
}



