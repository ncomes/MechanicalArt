

#include "cloneToQuad.h"

#include <maya/MFnPlugin.h>



PLUGIN_EXPORT MStatus initializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj, "NaughtyDog - Hans Godard", "1.0", "Any");

	status = plugin.registerNode(CloneToQuad::name, CloneToQuad::id, CloneToQuad::nodeCreator, CloneToQuad::nodeInitializer );
	if (!status) {
		status.perror("registerNode");
		return status;
	}
	return status;
}

PLUGIN_EXPORT MStatus uninitializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj);

	status = plugin.deregisterNode(CloneToQuad::id);
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}
	return status;
}