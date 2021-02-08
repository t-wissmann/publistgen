# publistgen -- generate publication lists

The `biblisttw.py` script generates html bibliography lists from bibtex-files.
It uses the python library [biblib](https://github.com/aclements/biblib) for
parsing bib files -- it is the only reliable bibtex parser I have used so far.

The script was written for [my own publication
list](https://thorsten-wissmann.de/publications.html) but after several
requests I decided to publish it.

## Requirements

* Python 3
* [biblib](https://github.com/aclements/biblib) (Either globally or cloned to the subdirectory `biblib/`)
