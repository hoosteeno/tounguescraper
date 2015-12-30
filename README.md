# Tounguescraper

This script scrapes phrases from a dtd file, then scrapes their translations from transvision.mozfr.org, then updates pofiles with those translations.

## Requirements

* [svn client](https://subversion.apache.org/)
* A local copy of the [locales repository](http://http://svn.mozilla.org/projects/l10n-misc/trunk/input/locale/)
* Python libs: polib, scrapy

## Usage

`scrapy runspider tounguescraper.py`
