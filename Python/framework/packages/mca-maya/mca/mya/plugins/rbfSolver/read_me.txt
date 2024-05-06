
1/

Put the Python Plugin in your plugin folder :

example :
C:\userName\Documents\maya\2015\plug-ins   ( create the "plug-ins" folder if it does not exist )




2/

Put the .png files in your icon folder :

example :
C:\userName\Documents\maya\2015\prefs\icons



3/

Run Maya, go to the plugin Manager and check the  "rbfSolver"



4/

Create the node with the MEL command :

createNode rbfSolver;





DOC :

Radial Basis Function Solver.

This Node allows to interpolate an input in a system defined by poses, each pose describes a Key and a Value.
So the concept is similar to the DrivenKey.

But a regular DrivenKey has 1-dimensional Keys  and 1-dimensional Values.
Basically each Key is a Float, and its Value is a Float.


The RBF solver has N-dimensional Keys  and M-dimensional Values.
It simply means, Keys can be anything, and Values can be anything.

For example a Key can be a 3D position, and its Value an RGBA color, so a 4D Value ( Check my Sample scene )



A good example is a Character Shoulder, how to drive the shoulder BlendShapes ?
Instead of using a Pose Deformer, which is basically a RBF per-Vertex ( so very expensive ), a very clean and efficient way is to setup the RBF solver such as :


Each Pose will be defined by a 3D Key, the Arm joint aim-Vector.
The Value of each Key will be the BlendShape weights for that Pose.

When the Arm joint (and/or more joints) is through this Pose, my Output BlendShapes will receive these Values.

All the interpolation between the Poses is computed by the RBF solver.


This kind of problem is very easy to solver using the RBF solver !





INPUT
.poses[i]
	.state : bool, use that pose or not
	.nKey : the key of that pose, N-dimentional
	.mValue : the value of that pose, M-dimensional 

.nInput : the input sliding between the pose keys, it is N-dimensional 


OUTPUT
.mOutput : the output M-dimensional 






