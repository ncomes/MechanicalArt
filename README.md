# Mechanical Art - Framework for Rigging Assets in Games

[![Python3](https://img.shields.io/badge/Python-3.7-yellow?logo=python)](https://www.python.org/)
[![Maya 2022](https://img.shields.io/badge/Maya-2022-orange?logo=autodesk)](https://www.autodesk.com/)
[![Maya 2024](https://img.shields.io/badge/Maya-2024-orange?logo=autodesk)](https://www.autodesk.com/)
[![Maya 2025](https://img.shields.io/badge/Maya-2025-orange?logo=autodesk)](https://www.autodesk.com/)

Framework for Rigging Assets in Games

***

## Setup for Character Technical Artists / Riggers

1) Make sure that you have installed a clean Python 3 interpreter in your machine.
2) Clone <a href="https://github.com/ncomes/MechanicalArt" target="_blank">
3) Execute setup_repos.bat to clone all the necessary repos into ```packages``` folder (it will be created)
4) Execute MCA Launcher.exe to create a Python 3 virtual environment and to install all the mca repos and their dependencies.
5) Execute the following code if you want to start manually.

```python
## Start up ##
import os
import sys

#################################################
root_paths = [r'E:\MechanicalArt\Python\framework\packages\mca-common',
			  r'E:\MechanicalArt\Python\framework\packages\mca-common\mca\common\startup\dependencies\py3']

for path in root_paths:
	if os.path.isdir(path) and os.path.normpath(path) not in sys.path:
		sys.path.append(path)


from mca.common.startup import startup
startup.init(dcc='maya', skip_dialog=False, hide_envs=True)


# Shutdown - This is used to shutdown the codebase.
startup.shutdown('maya')
```
