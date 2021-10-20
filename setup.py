from setuptools import setup

setup(
    name='msa_example',
    version='0.1.0',    
    description='An example Python MSA package',
    author='Nicolas Carrez',
    author_email='nicolas.carrez@gmail.com',
    license='BSD 2-clause',
    packages=['msa_example'],
    package_data={'msa_example': ['static/*']},
    include_package_data=True,
    install_requires=[
        'fastapi',
        'sqlalchemy',
    ],
)
