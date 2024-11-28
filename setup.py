from setuptools import find_packages, setup
from typing import List

hyphen_e='-e .'

def get_requirements(file_path:str)->List[str]:
    """
    This Function will return the list of all the libraries present in requirements
    """
    requirements=[]
    with open(file_path) as file:
        requirements=file.readlines()
        requirements=[req.replace('\n',' ') for req in requirements]

        if hyphen_e in requirements:
            requirements.remove(hyphen_e)
            return requirements

setup(
    name='mlproject',
    version='0.0.01',
    author = 'Dnyan',
    author_email='dnyan.bs@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)