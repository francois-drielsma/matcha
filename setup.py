#!/usr/bin/env python

import setuptools

VER = "0.1.0"

setuptools.setup(
    name="crt_tpc_matcher",
    version=VER,
    author="Andrew J. Mogan",
    author_email="andrew.mogan@colostate.edu",
    description="A package for matching CRT hit information with TPC tracks.",
    url="https://github.com/andrewmogan/crt_tpc_matcher",
    packages=setuptools.find_packages(where="src"), 
    package_dir={"":"src"},
    install_requires=[],
    python_requires='>=3.6',
)
