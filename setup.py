from setuptools import setup

setup(
    name='msa-example',
    version='0.1.0',    
    description='An example Python MSA package',
    author='Nicolas Carrez',
    author_email='nicolas.carrez@gmail.com',
    license='BSD 2-clause',
    packages=['msaexample'],
    package_data={'msaexample': ['static/*']},
    include_package_data=True,
    install_requires=[
        'fastapi',
        'sqlalchemy',
    ],
)
