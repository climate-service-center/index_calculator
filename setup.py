#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("index_calculator/__init__.py") as init_file:
    lines = init_file.read().strip().replace(" ", "").split("\n")
    for line in lines:
        if "__version__" in line:
            __version__ = line.split("=")[-1]
            __version__ = __version__.replace('"', "")
            break


def _read_txt(txt_file):
    return open(txt_file).read().strip().split("\n")


requirements = _read_txt("ci/requirements/requirements.txt")

setup_requirements = _read_txt("ci/requirements/requirements_dev.txt")

test_requirements = []

setup(
    author="Ludwig Lierhammer",
    author_email="ludwig.lierhammer@hereon.de",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="Python index-calculator is an xclim wrapper"
    "to calculate climate indices from CMORized netCDF files.",
    entry_points={
        "console_scripts": [
            "index_calculator=index_calculator.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="index_calculator",
    name="index_calculator",
    packages=find_packages(include=["index_calculator", "index_calculator.*"]),
    package_data={"index_calculator": ["*/*.nc", "*/*.json"]},
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ludwiglierhammer/index_calculator",
    version=__version__,
    zip_safe=False,
)
