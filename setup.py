#!/usr/bin/env python

import codecs
import os
import re

from setuptools import find_packages, setup

cwd = os.path.abspath(os.path.dirname(__file__))


def read(filename):
    with codecs.open(os.path.join(cwd, filename), "rb", "utf-8") as h:
        return h.read()


metadata = read(os.path.join(cwd, "herepy", "__init__.py"))


def extract_metaitem(meta):
    meta_match = re.search(
        r"""^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]""".format(meta=meta),
        metadata,
        re.MULTILINE,
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="herepy",
    version=extract_metaitem("version"),
    license=extract_metaitem("license"),
    description=extract_metaitem("description"),
    long_description=(read("README.rst")),
    long_description_content_type="text/x-rst",
    author=extract_metaitem("author"),
    author_email=extract_metaitem("email"),
    maintainer=extract_metaitem("author"),
    maintainer_email=extract_metaitem("email"),
    url=extract_metaitem("url"),
    download_url=extract_metaitem("download_url"),
    packages=find_packages(exclude=("tests", "docs")),
    package_data={"herepy": ["py.typed"]},
    platforms=["Any"],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="here api, here technologies, here python api clients, rest api clients",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
