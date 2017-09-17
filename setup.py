import setuptools
import sys


dependencies = {'cssselect', 'lxml', 'requests', 'six'}
if sys.version_info < (3, 4):
    dependencies.add('enum34')


setuptools.setup(
    name='MalCat',
    version='0.0.0',
    description='MAL list-to-text processing tools.',
    # long_description=readme,

    author='Doomcat55',
    author_email='Doomcat55@gmail.com',
    url='https://github.com/Doomcat55/MalCat',

    packages=setuptools.find_packages(exclude=('tests',)),
    include_package_data=True,

    setup_requires={'pytest-runner'},
    install_requires=dependencies,
    tests_require={'pytest'},

    license='MIT'
)
