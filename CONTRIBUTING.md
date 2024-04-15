In this documentations you will find some rules that you should follow when writing code for DCC Python tools. The objective of those conventions are:

Have a consistent code through our code base, so code its easy to read by all team members.

Write our code in a pythonic way: following the recommendations defined by PEP.

Following this rules will allow us:

Write correct and pythonic code.

Make our code easier to maintain.

Improve the readability of our code.

This is our Python Style Guide Bible: PEP8

 

## General
 

 

This is valid:

 

Open image-20210423-015053.png
image-20210423-015053.png
This is not valid:

 

Maximum length is 120 characters per line.

DID YOU KNOW?

For historic reasons, PEP8 defines maximum length to 80 characters. Nowadays that does not make too much sense because screens are wider. 

PyCharm sets by default the maximum length to 120 characters. Its indicated by the line indicated in the image above.

 

# this is valid
print('Hello World')


# this is NOT valid
print( 'Hello World' )
NEVER add an space between a start/end parenthesis.



# this is valid
['this', 'is', 'an', 'apple']


# this is NOT valid
['this','is','an','apple']
After a comma, ALWAYS add a space.



# this is a valid string
my_string = 'Hello World'
# this is also valid but we should try simple quotes if possible
my_string = "Hello World"
my_string = "Hello 'my friend'"  # this is a good example of double quotes ussage
Strings should be defined using simple quotes.

Double quotes are also valid but we should try to use simple quotes when possible.



# this is valid
if path not in sys.path:
  sys.path.append(path)


# this is not valid
if not path in sys.path:
  sys.path.append(path)
Test for membership needs to be not in.



# this is valid
print('Hello World')
print('Bye World')


# this is not valid
print('Hello World')
print('Bye World')
Between two lines of code we should not add more than one line

This is better:



def cool_depth(path):
  if not os.path.exists(path):
    return None
  if len(path) < 10:
    return None
  return path
than this:



def cool_depth(path):
  if os.path.exists(path):
    if len(path) < 10:
      return path
  return None
Try to avoid to have too many levels of depths in if/else statements.



# this is valid
import cpg.core.path as path
path.print('hello')


# this is NOT valid
import cpg.core.path as path;path.print('hello')
NEVER add two commands in the same line separated by ;



# this is valid
index = index + 1


# this is NOT valid
index = index+1
Between arithmetics operations ALWAYS add spaces.

Python Headers
Headers are the first lines defined in a Python file.

## Never
- Should not include authors, dates or nothing like that. All our source is stored in a repository that contains all this information. When you do not have too much files,  updating the headers is easy, when you need to maintain lot of code is a nightmare.

- Should not include any kind of changelog information. All this information should be reflected in our repository commits.

- Should not include any kind of information regarding versions. Tool versioning will be managed in a different way. And again, we will use our repository information (and/or metadata files) to handle this.

- Should not include any kind of license/copyright information. This information should be located in a LICENSE file located in the root of the repository.

- Never leave imports that are not being used if it’s not strictly necessary (if that’s the case write a comment saying WHY that unused import should not be removed).

  
## Should
- Should include an statement to force the first interpreter defined in PATH to be used (PEP 394). 

- Should define a predefined Python source encoding. utf-8 is recommended to support special characters. (PEP 263)

- Should include a description (the most descriptive, the better) of what is expected this file to contain.

- To make sure that we force ourselves to write Python 3 compatible code its recommended to use __future__ module (PEP 236)



#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module that contains generic Python functions to handle paths in a cross-platform way
"""
from __future__ import print_function, division, absolute_import
 

 



#! /usr/bin/env python
# -*- coding: utf-8 -*-
Special Python declarations:

Makes Python use the first interpreter defined in PATH (useful when calling our code through command line). 

Defines utf-8 as the Python source code to use.



"""
Module that contains generic Python functions to handle paths in a cross-platform way
"""
 

Multiple lines comment with a proper description of what the file contains.

from __future__ import print_function, division, absolute_import

Import that will force us to:

Use print using () (Python 3 way). (PEP 3105)

Make sure division operations work as expected. (PEP 238)

return 10/1000 without future this would return 0; with future this would return 0.01.

Force the usage of absolute imports. (PEP 328).

If we write code that does not follow this rules, Python interpreter will raise an exception.

## Imports
This section goes after the headers definition. Module imports are the way Python has to import code from other Python files (kinda similar to include header files in C++).

Avoid using relative imports:

Implicit relative imports are not supported in Python 3.

Can be REALLY difficult for other developers to know where is the module we are trying to import.

When working with multiple Python packages, If two modules has the same name it’s very easy that you end up importing the wrong module.

NEVER EVER use wildcard imports.

Keep imports at the top of the file.

Should use absolute imports.

Imports should be organized into groups

Builtin/Standard Python imports.

Third-party/External libraries imports.

Specific application/library imports.

Imports should be ordered alphabetically or by its length.

Between each types of imports we should add a blank line.

Imports should be placed from shorter to larger.

Ke

Absolute Imports VS Relative Imports

DID YOU KNOW?

By using absolute imports instead of relative imports we can easily “reload” our Python code when working inside DCCs interpreters. For example, if the root module of our package is called cpg and we call our imports using absolute imports: from cpg.tools.picker.core import consts we can easily reload all our modules in the following way (this way works in both Python 2 and 3):



def reload_modules():
    modules_to_reload = ('cpg',)
    for k in sys.modules.copy().keys():
        if k.startswith(modules_to_reload):
            del sys.modules[k]
reload_modules()
 

 



from Qt.QtCore import *
This is a Python anti-pattern pg 29.



import validate
import export
Those are relative imports. This kind of imports are valid in Python 2/3 but they are nightmare for other developers:

Where those modules are located? At a first glance, it’s impossible to know.

What happens if other third packages have a module called validate? We won’t be able to be 100% sure that proper validate module is imported.



from . import validate
 

This is a relative explicit import and is supported in Python 3. The . means the current directory, so this line will try to import a module named validate located in the same directory of the current module.

This relative import is a bit more clear for the developer. The only problem is that sys.modules dictionary can get a bit messy by using this kind of imports and can be complex to track some specific types of errors.

My recommendation would be to avoid them.

 



from .validate import testClass
 

This is a relative implicit import and they are not supported in Python 3. Just avoid them.

All the imports are valid but the order is messy.



import maya.cmds as cmds
import maya.mel as mel
import os
import inspect
from collections import defaultdict
Imports follow an order an its much cleaner for the developer to know the different modules types we are importing here.



# Builtin Python imports (shorter first)
import os
import inspect
from collections import defaultdict
# Third-party imports
import maya.cmds as cmds
import maya.mel as mel
# Specific imports
from cpg.core import utils
 



# this is valid import
import xml.etree.ElementTree as et


# this is not a valid import
import xml.etree.ElementTree as ET
Import namespaces ALWAYS must be lower case.

Instance Variables


class MyClass(object):
  def __init__(self):
    self.num_joints = 5
    self.num_controls = 3
    self.name = 'component'
Variable names should be all lower case. (PEP8)

Words in a instance variable name should be separated by an underscore, following snake_case style. (PEP8) 

Those  are bad examples for names:

data_structure (too general).

my_list (too general).

info_map (too general).

dict_to_store_data_ordered_by_bigger_values (too long).

Those are good examples:

user_profile

menu_options

word_definitions

Avoid using names that are too general or too wordy (non-descriptive names).



for i in range(10):
  print(i)
Single letter names are allowed by we should only use them in very specific cases:

Loops



class MyClass(object):
  def __init__(self):
    self._private_variable = None
Non-public instance variables should begin with a single underscore.



class MyClass(object):
  def __init__(self):
    self.__private_variable = None
DID YOU KNOW?

This variable is automatically mangled by Python interpreter and converted into:

'_MyClass__private_variable

This is used by Python to avoid naming clashes. In some scenarios can cause PyCharm to have troubles while debugging them for that reason we should avoid using them.

Avoid the usage of double underscore names. Those variables are mangled by Python interpreter and can be REALLY DIFFICULT to debug them.

Constants


logger = logging.getLogger(__name__)
Global variable names should be all lower case. (PEP8)

Words in a global variable name should be separated by an underscore, following snake_case style. (PEP8) 

Global Variables


global MY_GLOBAL_VARIABLE
Global variable names should be all upper case. (PEP8)

Words in a global variable name should be separated by an underscore, following snake_case style. (PEP8) 

 

Functions/Methods
This section includes information about throw to functions should be defined.

 



# this is a bad function name
def printString(text):
  pass


# this is a correct function name
def print_string(text):
  pass
Functions name should be all lower case. (PEP8)

Words in a function name should be separated by an underscore, following snake_case style. (PEP8) 



class MyClass(object):
  def _get_text(self):
    return 'bye'
Non-public functions should begin with a single underscore.



class MyClass(object):
  def _get_text(self):
      return 'bye'
DID YOU KNOW?

This function name is automatically mangled by Python interpreter and converted into:

'_MyClass__get_text

This is used by Python to avoid naming clashes. In some scenarios can cause PyCharm to have troubles while debugging them for that reason we should avoid using them.

Avoid the usage of double underscore names. Those variables are mangled by Python interpreter and can be REALLY DIFFICULT to debug them.

Function/Method Arguments


class MyClass(object):
  def _get_text(self):
    # this is valid
    return 'bye'


class MyClass(object):
  def _get_text(abc):
    # this is NOT valid
    return 'bye'
Instance methods should have their first argument named self.

 



class MyClass(object):
  @classmethod
  def _get_text(cls):
    # this is valid
    return 'bye'


class MyClass(object):
  @classmethod
  def _get_text(abc):
    # this is NOT valid
    return 'bye'
Class methods should have their first argument named cls.



# this is valid
def print_text(text='hello'):
  print(text)


# this is NOT valid
def print_text(text = 'hello'):
  print(text)
After an equal sign NEVER add spaces



# this is valid
def print_string(text):
  pass
def print_string2(text):
  pass


# this is not valid
def print_string(text):
  pass
def print_string2(text):
  pass
Between two global functions must to be two lines of separation.



# this is valid
def test(data_info=None):
  data_info = data_info or dict()
# this is not valid:
def test(data_info=dict()):
  pass
NEVER initialize mutable types in functions arguments.

 

This can cause LOT of very complicated bugs to track.

Classes


# this class valid
class HelloWorld(object):
  pass


# this class is NOT valid
class hello_world(object):
  pass
Class name should follow the UpperCaseCamelCase convention.

Packages
Some examples of valid package names:

core

modules

animtools (prefererred over anim_tools).

Package names should be all lower case.

When multiple words are needed, an underscore should separate them

It’s recommended to stick to 1 word names.

Modules
Some examples of valid module names:

hello.py

helloworld.py (preferred over hello_world.py).

Package names should be all lower case.

When multiple words are needed, an underscore should separate them

It’s recommended to stick to 1 word names.



# this is valid
def test():
  pass
def test2():
  pass


# this is NOT valid
def test():
  pass
def test2():
  pass
ALL Python module Python files should end with an empty line space.

Comments
This section includes information about how comments should be used in different parts of the code.



# this is a valid comment


#this is NOT a valid comment
A comment ALWAYS need to start with # and an space.



def print_name(self):
    print(self.name)  # comment is correct


def print_name(self):
    print(self.name) # this comment needs an extra space
At least two spaces before inline comment. Not doing this is an anti-pattern. (PEP8).



# this is a good comment


# This is not a good comment
In one line comments, first letter should be always lowercase.

Docstrings


# this is valid docstring
def test():
  """
  This is a test function
  """
  pass


# this is NOT valid docstring
def test():
  """
  this is a test function
  """
  pass
In docstrings, first letter should be always upper case.



# this is correct
def hello_world():
  """
  Prints hello world string
  """
  pass


# this is NOT correct
def hello_world():
  """
  Prints hello world string
  """
  pass
After defining a docstring, we ALWAYS must add an empty line.



# this is correct
def hello_world():
  """
  Prints hello world string
  """
  pass


# this is NOT correct 
def hello_world():
    '''
    Prints hello world string
    '''
    pass    
When commenting functions using docstrings we always need to use triple-double quote strings. (PEP 257)

If/Else Statements


# this is a valid if statement
if var == 5:
  print('hello world')


# this is NOT a valid if statement
if var == 5:
  print('hello world')
First line after an if statement cannot be an empty line.

Exceptions


# this is a valid custom exception
class CustomExceptionError(Exception):
  pass


# this is not a valid custom exception
class CustomException(Exception):
  pass
Custom exceptions names should always end with Error.



# this is a valid try/exception clause
try:
  test_var = get_variable()
except RuntimeError as exc:
  logger.error('Something happened: {}'.format(exc))


# this is also a valid try/exception clause (but avoidable if possible)
try:
  test_var = get_variable()
except Exception as exc:
  logger.error('Something happened: {}'.format(exc))


# this is also a valid try/exception clause (but avoidable if possible)
try:
  test_var = get_variable()
except Exception:
  logger.error('Something happened: {}'.format(traceback.format_exc()))


# this is NOT a valid try/exception clause
try:
  test_var = get_variable()
except:
  logger.error('Something happened')
A try/except clause always should define an Exception.

The most specific the exception catched the better. We should try to avoid using the generic Exception.

The exception name ALWAYS should be exc. Please no use e letter (which is quite common to see in codes).

Useful information
PEP8 (Python Guide Style)

How to Write Beautiful Python Code With PEP8
