# -*- coding: utf-8 -*- 
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
from collections import defaultdict # we use defaultdict vs. OrderedDict for compatability. Requires some workarounds.
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
        """[--num #|--reinterpret|--usemetric|--shortest|--fulloutput] <input>
        
        Returns answer from Wolfram Alpha API based on input.
        
        Use --num number to display a specific amount of lines.
        Use --reinterpret to have WA logic to interpret question if not understood.
        Use --usemetric to not display in imperial units. 
        Use --shortest for the shortest output (ignores lines).
        Use --fulloutput to display everything from the API (can flood).
        """
        
        # check for API key before we can do anything.
        apiKey = self.registryValue('apiKey')
        if not apiKey or apiKey == "Not set":
            irc.reply("Wolfram Alpha API key not set. see 'config help supybot.plugins.WolframAlpha.apiKey'.")
            return
            
        # first, url arguments, some of which getopts and config variables can manipulate.
        urlArgs = { 'input':optinput, 'appid':apiKey, 'reinterpret':'false', 'format':'plaintext', 'units':'nonmetric' }
        
        # check for config variables to manipulate URL arguments.
        if not self.registryValue('useImperial'):
            urlArgs['units'] = 'metric'
        if self.registryValue('reinterpretInput'):
            urlArgs['reinterpret'] = 'true' 
        
        # args we use internally to control output.                          
        args = { 'maxoutput': self.registryValue('maxOutput'), 'shortest':None, 'fulloutput':None }
        
        # handle getopts.
        if optlist:
            for (key, value) in optlist:
                if key == 'shortest':
                    args['shortest'] = True
                if key == 'fulloutput':
                    args['fulloutput'] = True
                if key == 'num':
                    args['maxoutput'] = value
                if key == 'usemetric':
                    urlArgs['units'] = 'metric'
                if key == 'reinterpret':
                    urlArgs['reinterpret'] = 'true'
                
        # build url.
        url = 'http://api.wolframalpha.com/v2/query?' + urllib.urlencode(urlArgs)
        self.log.info(url)
                    
        # try and query.                        
        try: 
            request = urllib2.Request(url)
            u = urllib2.urlopen(request)
        except:
            irc.reply("Failed to load url: %s" % url)
            return

        # now try to process XML.
        try:
            tree = ElementTree.parse(u)
            document = tree.getroot()
        except:
            irc.reply("Something broke processing the XML.")
            return
            
        # check if we have an error. reports to irc but more detailed in the logs.
        if document.attrib['success'] == 'false' and document.attrib['error'] == 'true':
            errormsgs = []  
            for error in document.findall('.//error'):
                errorcode = error.find('code').text
                errormsg = error.find('msg').text
                errormsgs.append("{0} - {1}".format(errorcode, errormsg))
            
            self.log.debug("ERROR processing request for: {0} message: {1}".format(optinput, errormsgs))
            irc.reply("Something went wrong processing request for: {0} ERROR: {1}".format(optinput, errormsgs))
            return
        elif document.attrib['success'] == 'false' and document.attrib['error'] == 'false': # no success but no error.
            errormsgs = []
            for error in document.findall('.//futuretopic'):
                errormsg = error.attrib['msg']
                errormsgs.append("FUTURE TOPIC: {0}".format(errormsg))

            for error in document.findall('.//didyoumeans'):
                errormsg = error.find('didyoumean').text
                errormsgs.append("Did you mean? {0}".format(errormsg))
            
            for error in document.findall('.//tips'):
                errormsg = error.find('tip').attrib['text'].text
                errormsgs.append("TIPS: {0}".format(errormsg))

            self.log.debug("ERROR with input: {0} API returned: {1}".format(optinput, errormsgs))
            irc.reply("ERROR with input: {0} API returned: {1}".format(optinput, errormsgs))
            return
        else: # this means we have success and no error messages.
            # each pod has a title, position and a number of subtexts. output contains the plaintext.
            # outputlist is used in sorting since defaultdict does not remember order/position.
            output = defaultdict(list)
            outputlist = {}
            
            for pod in document.findall('.//pod'):
                title = pod.attrib['title'].encode('utf-8')
                position = pod.attrib['position'].encode('utf-8')
                outputlist[position] = title
                for plaintext in pod.findall('.//plaintext'):
                    if plaintext.text:
                        output[title].append(plaintext.text.encode('utf-8').replace('\n',' '))
        
        # done processing the XML so lets work on the output.
        if len(output) < 1:
            irc.reply("Something went wrong looking up: {0}".format(optinput))
            return
        else: # rarely, output doesn't have things. validated so now output.
            if args['shortest']: # just show the question and answer.
                # outputlist has pod titles, sort, get the first and second title, string, fetch key.
                # other approach would be to use the keys above, which can be unreliable. Not every q/a has a set podtitle.
                question = output.get(str("".join(sorted(outputlist.values())[0])), None)
                answer = output.get(str("".join(sorted(outputlist.values())[1])), None)

                irc.reply("{0} :: {1}".format(string.join([item for item in question]), string.join([item for item in answer])))
                
            elif args['fulloutput']: # show everything. no limits.
                for k, v in sorted(outputlist.items()): # grab all values, sorted via the position number. output one per line.
                    itemout = output.get(v, None) # output contains lists, so we need to join prior to going out.
                    if itemout and itemout is not None:
                        irc.reply("{0} :: {1}".format(v, "".join(itemout)))
                        
            else: # regular output, dictated by --lines or maxoutput.
                for q, k in enumerate(sorted(outputlist.keys())):
                    if q < args['maxoutput']:
                        itemout = output.get(outputlist[k], None) # have the key, get the value, use for output.
                        if itemout and itemout is not None:
                            irc.reply("{0} :: {1}".format(outputlist[k], "".join(itemout)))
                    
    wolframalpha = wrap(wolframalpha, [getopts({'num':'int',
                                                'reinterpret':'',
                                                'usemetric':'',
                                                'shortest':'',
                                                'fulloutput':''}), 'text'])


Class = WolframAlpha


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=250:
