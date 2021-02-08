# publistgen: generate static publication lists from bibtex files

The `publistgen.py` script generates html bibliography lists from bibtex-files.
It uses the python library [biblib](https://github.com/aclements/biblib) for
parsing bib files. It is the only reliable bibtex parser I have used so far.

The script was written for [my own publication
list](https://thorsten-wissmann.de/publications.html) but I got several requests to make it publicly available.

## Requirements

* Python 3
* [biblib](https://github.com/aclements/biblib) (Either globally or cloned to the subdirectory `biblib/`)

## Installation

Either install via `python setup.py install` or by simply cloning the [biblib](https://github.com/aclements/biblib) library
to the `biblib/` subdirectory.

## Usage

Run
```bash
/path/to/publistgen.py bibfile.bib > publications.html
```
to generate `publications.html` which can be embedded in another html file. If
you want to customize the output e.g. by linking to homepages of authors, you
can overwrite default settings in a `publist.py` config file:
```python
# a dict mapping author names (in utf8) to their homepage url
author_homepages = {
    'Thorsten Wißmann': "http://www8.informatik.uni-erlangen.de/thorsten",
}
```
