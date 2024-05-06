

#include "greenDeformer.h"

#include <maya/MFnPlugin.h>



PLUGIN_EXPORT MStatus initializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj, "Hans Godard", "1.0", "Any");

	status = plugin.registerNode(GreenDeformer::name, GreenDeformer::id, GreenDeformer::nodeCreator, GreenDeformer::nodeInitializer, MPxNode::kDeformerNode);
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

	status = plugin.deregisterNode(GreenDeformer::id);
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}
	return status;
}