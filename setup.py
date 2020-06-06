import os
from setuptools import setup


os.chdir(os.path.abspath(os.path.dirname(__file__)))


req = []
setup_req = [
    'cffi>=1.14,<2',
]
setup(name='cmph',
      version='0.1',
      packages=['cmph'],
      setup_requires=setup_req,
      install_requires=req,
      cffi_modules=['ffi_builder.py:ffi_builder'],
      description="CMPH wrapper",
      author="Remi Rampin",
      author_email='remi.rampin@nyu.edu',
      maintainer="Remi Rampin",
      maintainer_email='remi.rampin@nyu.edu',
      long_description="CMPH wrapper",
      license='MIT')
