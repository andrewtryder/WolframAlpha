###
# Copyright (c) 2012, spline
# All rights reserved.
#
#
###

# my libs
import urllib2
import urllib
import string
try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

# supybot libs
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring

_ = PluginInternationalization('WolframAlpha')

@internationalizeDocstring
class WolframAlpha(callbacks.Plugin):
    """Add the help for "@plugin help WolframAlpha" here
    This should describe *how* to use this plugin."""
    threaded = True
    
    # http://products.wolframalpha.com/api/documentation.html
    def wolframalpha(self, irc, msg, args, optlist, optinput):
        """[--options] <input>
        Returns answer from Wolfram Alpha API based on input.
        Ex: freezing point of water at 20,000ft
        """
        
        # check for API key before we can do anything.
        apiKey = self.registryValue('apiKey')
        if not apiKey or apiKey == "Not set":
            irc.reply("Wolfram Alpha API key not set. see 'config help supybot.plugins.WolframAlpha.apiKey'.")
            return
        
        # first, url arguments, some of which getopts and config variables can manipulate.
        urlArgs = { 'input': optinput,
                    'appid': apiKey,
                    'reinterpret': 'false',
                    'format':'plaintext',
                    'podindex':'1,2,3',
                    'units':'nonmetric'
                  }
                          
        #maxoutput = self.registryValue('maxOutput')
        maxoutput = 10
        # units = self.registryValue('units')
        
        # handle getopts.
        if optlist:
            for (key, value) in optlist:
                if key == 'version':
                    if value.lower() not in validVersions:
                        irc.reply("Invalid version. Version must be one of: {0}".format(validVersions.keys()))
                        return
                    else:
                        version = value.lower()

        # build url.
        url = 'http://api.wolframalpha.com/v2/query?' + urllib.urlencode(urlArgs)
        self.log.info(url)
                    
        # try and query.                        
        try: 
            request = urllib2.Request(url, headers={"Accept" : "application/xml"})
            u = urllib2.urlopen(request)
        except:
            irc.reply("Failed to load url: %s" % url)
            return

        # now try to process XML.
        tree = ElementTree.parse(u)
        document = tree.getroot()

        # check if we have an error
        if document.attrib['success'] == 'false' or document.attrib['error'] == 'true':
            self.log.debug("ERROR processing input: {0}. Document: {1}".format(optinput, str(document)))
            irc.reply("Something went wrong processing request for: {0}".format(optinput))
            return
        
        # error = false but success = false
        # <didyoumeans>
        #   <didyoumeans count='1'>
        #   <didyoumean>frances split</didyoumean>
        # </didyoumeans>
        #   <futuretopic topic='Operating Systems'
        # msg='Development of this topic is under investigation...' />
        
        #retrieving every tag with label 'plaintext'
        #for e in tree.findall('pod'):
	    #        for item in [ef for ef in list(e) if ef.tag=='subpod']:
	    #            for it in [i for i in list(item) if i.tag=='plaintext']:
	    #                if it.tag=='plaintext':
	    #                    data_dics[e.get('title')] = it.text
        

        # Input interpretation and Result are pod titles.

        # now process the output. We put everything in a dict to process easier later on.
        output = {}

        for pod in document.findall('.//pod'):
            title = pod.attrib['title']
            for plaintext in pod.findall('.//plaintext'):
                if plaintext.text:
                    output[title] = plaintext.text.encode('utf-8').replace('\n',' ')
                    
        if len(output) < 1:
            irc.reply("Something went wrong looking up: {0}".format(optinput))
            return
        else:
            for i,each in output.iteritems():
                irc.reply("{0} | {1}".format(i, each))
    
    wolframalpha = wrap(wolframalpha, [getopts({'lines':'int',
                                                            }), 'text'])


Class = WolframAlpha


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=250:
