import setuptools
import pathlib
import os

here = pathlib.Path(__file__).parent.resolve()

with open(os.path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="publistgen",
    version='0.1.0',
    author="Thorsten Wißmann",
    author_email="edu@thorsten-wissmann.de",
    description="generate static publication lists from bibtex files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/t-wissmann/publistgen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'biblib',
    ],
    python_requires='>=3.6',
)
