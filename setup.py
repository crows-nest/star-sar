import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setuptools.setup(
   name='star SAR',
   version='0.1',
   description='a DDF SAR solution',
   author='Jeff Venicx',
   author_email='jeve0658@colorado.edu',
   install_requires=requirements, 
   python_requires= '>=3.6'
)