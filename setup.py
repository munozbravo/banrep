from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_one = fh.read()

setup(
    name="banrep",
    version="0.0.1",
    description="Funciones y rutinas para BanRep",
    long_description=long_one,
    long_description_content_type="text/markdown",
    url="https://github.com/munozbravo/banrep",
    author="dataficado",
    author_email="dataficado@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7.3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
