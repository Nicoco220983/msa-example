from setuptools import setup, find_packages

setup(
    name='msaexample',
    version='0.1.0',    
    description='An example Python MSA package',
    author='Nicolas Carrez',
    author_email='nicolas.carrez@gmail.com',
    license='BSD 2-clause',
    packages=find_packages(),
    package_data={'msaexample': ['static/*']},
    include_package_data=True,
    install_requires=[
        'fastapi',
        'sqlalchemy',
    ],
)
