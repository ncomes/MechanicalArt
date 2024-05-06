


C++

- Create a new Maya Plugin Wizard Plugin with name 'skinningDecomposition'

- Delete all the files (h and cpp) created by the project.

- Replace by my files instead, ( those in the skinningDecomposition folder )


- Set the solution to release  ( important, no debug )

- I provide my current version of Eigen, you can also download the latest version here :
	http://eigen.tuxfamily.org/index.php?title=Main_Page

- Setup the "include" directory of Eigen in the project. (check the 2 pictures)


- Compile.

- Copy the new .mll in your Maya plugin directory.




PYTHON

- Copy the new .py in your Maya Script directory.




IN MAYA

- run in a Python tab :


import skinningConverter

win = skinningConverter.showUI()