import json
import os
import polib
import re
import scrapy

class ToungueScraper(scrapy.Spider):

    # Must have a locale directory in pwd, which should be a
    # local copy of http://svn.mozilla.org/projects/l10n-misc/trunk/input/

    name = 'toungescraper'

    po_files = {}

    transvision_url = 'https://transvision.mozfr.org/api/v1/entity/release/?id=mobile/android/chrome/aboutFeedback.dtd'

    # Start with the dtd, which contains l10n entities
    start_urls = [
        'http://mxr.mozilla.org/mozilla-central/source/mobile/android/locales/en-US/chrome/aboutFeedback.dtd?raw=1'
    ]

    # Write pofiles with translated strings
    def write_pofile(self, f, phrases):
        pofile = polib.pofile(f)
        for msgi, msgs in phrases.iteritems():
            entry = polib.POEntry(
                msgid = msgi,
                msgstr = msgs
            )
            pofile.append(entry)
        pofile.save(f)

    # When the spider closes, process all the l10n strings it got
    def close(spider, reason):
        for locale in spider.po_files:
            print "NOW PROCESSING %s" % (locale)

            f_under = 'locale/%s/LC_MESSAGES/django.po' % (locale)
            f_dash = 'locale/%s/LC_MESSAGES/django.po' % (locale.replace('_', '-'))

            if os.path.isfile(f_under):
                spider.write_pofile(f_under, spider.po_files[locale])

            elif os.path.isfile(f_dash):
                spider.write_pofile(f_dash, spider.po_files[locale])

            else:
                print "--> %s and %s don't exist" % (f_under, f_dash)

    # Grab each l10n entity, turn it into a url, request its localization
    def parse(self, response):

        for entity in response.body_as_unicode().split('\n'):
            m = re.match("^\<\!ENTITY\s(\S+)", entity)
            if m:
                url = '%s:%s' % (self.transvision_url, m.groups()[0])
                yield scrapy.Request(url, self.parse_localizations)


    # Grab the localizations for each phrase,
    # clean up,
    # add to global pofiles dict
    def parse_localizations(self, response):

        phrase_json = json.loads(response.body_as_unicode())
        msgid = phrase_json['en-US'].replace("&brandShortName;", "Firefox")

        for locale, msgstr in phrase_json.iteritems():
            locale = locale.replace("-", "_") 
            msgstr = msgstr.replace("&brandShortName;", "Firefox")
            if locale in self.po_files:
                self.po_files[locale][msgid] = msgstr
            else:
                self.po_files[locale] = {msgid: msgstr,}
            #print 'In %s, %s is "%s"' % (locale, msgid, msgstr)
