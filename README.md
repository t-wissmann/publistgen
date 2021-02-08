# publistgen: generate static publication lists from bibtex files

The `publistgen.py` script generates html bibliography lists from bibtex-files.
It uses the python library [biblib](https://github.com/aclements/biblib) for
parsing bib files. It is the only reliable bibtex parser I have used so far.

The script was written for [my own publication
list](https://thorsten-wissmann.de/publications.html) but I got several requests to make it publicly available.

## Requirements

* Python 3
* [biblib](https://github.com/aclements/biblib) (Either globally or cloned to the subdirectory `biblib/`)
