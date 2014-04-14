'''
Created on 2014-1-21

@author: Administrator
'''

'''
    1.create folder: folder-name
    2.copy ***.py into folder-name
    3.create setup.py
        -------------------------------------------
        setup(
          name = 'athlete' ,
          version = '1.0.0',
          py_modules = ['athelets'],#module-name
          author = 'kane',
          )
        -------------------------------------------
    4.cmd>>cd folder-name
    5.[   python setup.py sdist    ]   compile
    6.[   python setup.py install ]    install
        
'''

from distutils.core import setup ;

setup(
      name = 'athlete' ,
      version = '1.0.0',
      py_modules = ['athelets'],#module-name
      author = 'kane',
      )