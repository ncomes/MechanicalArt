
1/

Put the Python Plugin in your plugin folder :

example :
C:\Users\userName\Documents\maya\2013-x64\plug-ins   ( create the "plug-ins" folder if it does not exist )




2/

Put the .png files in your icon folder :

example :
C:\UsersuseName\Documents\maya\2013-x64\prefs\icons



3/

Run Maya, go to the plugin Manager and check the zapanSmoothDistance.py



4/

Create the node with the MEL command :

createNode zapanSmoothDistance ;





DOC :

This node allow you to limit the distance of a Transform node from a Root Transform node, with a progressive damping.
We can call it the Smooth Transform.
The Smooth Transform is driven by a Driver Transform.


A good application is with an Ik Chain, you can set in the node the total length for the Chain, in the .distanceMax attribute.
then just parent your Ik Handle under the Smooth Transform.
The result is an Ik Smooth / Ik Soft, with no pop when the Driver Transform is far from the Root.

A sample scene is included.


Inputs :
.rootMatrix : the matrix used for starting the distance.
.moveMatrix : the matrix used for ending the distance.
.distanceMax : the outMatrix will not exceed this distance from the rootMatrix.
.smoothPercent : the percentage of the distanceMax from which starts amortizing/smoothing.
.smoothWeight : just a blend value [.0, 1.0] for blending the outMatrix between its smoothest position and its maximum position ( the moveMatrix ).
.strechWeight : an additive input not necessary but easier if you want to combine the nodes zapanSmoothDistance + zapanStrech.
.relativeMatrix : the inverse matrix post-multiplied by the outMatrix.

Outputs :
.outTranslate : the new translation, respecting the maxDistance from rootMatrix, it can be called ".smoothTranslate"
.outDistance : just the simple distance between rootMatrix and moveMatrix.
.outDistanceSmooth : the distance from root to outTranslate.





