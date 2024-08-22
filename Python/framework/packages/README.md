# Mechanical Art - Framework for Rigging Assets in Games

[![Python2](https://img.shields.io/badge/Python-2.7-yellow?logo=python)](https://www.python.org/)
[![Python3](https://img.shields.io/badge/Python-3.7-yellow?logo=python)](https://www.python.org/)
[![Maya 2018](https://img.shields.io/badge/Maya-2018-orange?logo=autodesk)](https://www.autodesk.com/)
[![Maya 2022](https://img.shields.io/badge/Maya-2022-orange?logo=autodesk)](https://www.autodesk.com/)
[![pep8](https://img.shields.io/badge/code_style-pep8-blue)](https://counterplay.atlassian.net/wiki/spaces/CGH/pages/1253376053/Python+Code+Style+Guide)

Framework for Rigging Assets in Games

***

## Setup for Character Technical Artists / Riggers

1) Make sure that you have installed a clean Python 3 interpreter in your machine.
4) Execute setup_py3_dev_env.bat to create a Python 3 virtual environment and to install all the CPG repos and their dependencies.
5) Execute the following code.

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


# Shutdown
startup.shutdown('maya')
```
