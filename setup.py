from __future__ import print_function
from setuptools import setup, Command
import os

import losoto._version


description = 'LOFAR solution tool'
long_description = description
if os.path.exists('README.md'):
    with open('README.md') as f:
        long_description=f.read()


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='losoto',
    version=losoto._version.__version__,
    url='http://github.com/revoltek/losoto/',
    author='Francesco de Gasperin',
    author_email='example@example.com',
    description=description,
    long_description=long_description,
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    tests_require=['pytest'],
    install_requires=['numpy','cython','numexpr>=2.0','tables>=3.0'],
    #scripts = ['say_hello.py'],
    packages=['losoto','losoto.operations'],
    test_suite='test',
    cmdclass = {'test': PyTest},
    )