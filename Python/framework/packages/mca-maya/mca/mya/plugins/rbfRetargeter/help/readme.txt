


C++

- Create a new Maya Plugin Wizard Plugin with name "retargetShapes"

- Delete all the files (h and cpp) created by the project.

- Replace by my files instead, ( those in the "retargetShapes" folder )

- Set the solution to release  ( important, no debug )


- I provide my current version of Eigen, you can also download the latest version here :
	http://eigen.tuxfamily.org/index.php?title=Main_Page

- Setup the "include" directory of Eigen in the project. (check the 2 pictures)


- Compile.

- Copy the new .mll in your Maya plugin directory.
	( "C:\Users\*user_name*\Documents\maya\201*\plug-ins" )		// create it if it does not exist.



PYTHON

- Copy the .py in your Maya Script directory.
	( "C:\Users\*user_name*\Documents\maya\201*\scripts" )




IN MAYA


- Open the attached Maya scene ( help/sample.ma )


- run in a Python tab :


import rbfRetargeter

win = rbfRetargeter.showUI()



- In the GUI,  set a Source mesh

- set source shapes

- set Target(s)

- Push "Build Shapes" button !





