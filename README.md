Purpose

    There are at least 3 plugins floating around for WA. One of the big differences with each variant from users
    is the differences in output due to the verbosity from how WA answers questions. Some answers can be
    10+ lines and easily flood a channel, either having the bot flood off or getting it banned from a channel.
    I wanted to use the getopts power and make some configuration options to display the data in a more friendly
    manner. Otherwise, the functionality is the same. 

Instructions

    First, you will need to fetch an API key for WA at http://products.wolframalpha.com/developers/
    It is free. Once getting this key, you will need to set it on your bot before things will work:

    /msg bot config plugins.WolframAlpha.apiKey APIKEY
    
    (Optional) I also suggest you make some aliases via the Alias plugin to make life easier. The main command is: wolframalpha.
    
    /msg bot Alias add wa wolframalpha
    /msg bot Alias add wolfram wolframalpha
    /msg bot Alias add alpha wolframalpha
 
Commands

    * wolframalpha <input>
