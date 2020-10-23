# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packagename = "pcbtesterinterface"

setuptools.setup(
    name=packagename, # Replace with your own username
    version="0.0.1",
    author="Marco Mörz",
    author_email="marcomoerz@gmail.com",
    description="The interface for the pcbtester",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Semi-ATE/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
       'pluggy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)