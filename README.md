# Tounguescraper

This script scrapes phrases from a [dtd file](http://mxr.mozilla.org/mozilla-central/source/mobile/android/locales/en-US/chrome/aboutFeedback.dtd?raw=1), then scrapes their translations from the [transvision.mozfr.org](https://transvision.mozfr.org/) API, then updates pofiles with those translations.

After it is run the changes to svn files must be committed.

## Requirements

* [svn client](https://subversion.apache.org/)
* A local copy of the [locale repository](http://http://svn.mozilla.org/projects/l10n-misc/trunk/input/locale/) in a directory called `locale` in the cwd
* Python libs: `polib`, `scrapy`

## Usage

`scrapy runspider tounguescraper.py`
