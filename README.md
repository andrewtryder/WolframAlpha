[![Build Status](https://travis-ci.org/reticulatingspline/Supybot-WolframAlpha.svg?branch=master)](https://travis-ci.org/reticulatingspline/Supybot-WolframAlpha)

# Limnoria plugin for WolframAlpha.

## Purpose

There are at least 3 plugins floating around for WA. One of the big differences with each variant from users
is the differences in output due to the verbosity from how WA answers questions. Some answers can be
10+ lines and easily flood a channel, either having the bot flood off or getting it banned from a channel.
WA's API also has some input options that can be handy, along with some verbose "error" messages that can help
the user, which the other plugins do not utilize. I wanted to use the getopts power and make some configuration
options to display the data in a more friendly manner.

## Instructions

First, you will need to fetch an API key for WA at http://products.wolframalpha.com/developers/
It is free. Once getting this key, you will need to set it on your bot before things will work.
Reload once you perform this operation to start using it.

> /msg bot config plugins.WolframAlpha.apiKey APIKEY

- Optional: There are some config variables that can be set for the bot. They mainly control output stuff.

> /msg bot config search WolframAlpha

- Optional: I also suggest you make some aliases via the Alias plugin to make life easier. The main command is: wolframalpha.

> /msg bot Alias add wa wolframalpha
> /msg bot Alias add wolfram wolframalpha
> /msg bot Alias add alpha wolframalpha

## Commands

* wolframalpha <query/question>
* wolframalpha 2+2
* wolframalpha 25USD to EUR
* wolframalpha meaning of life

## Notes

All of my plugins are free and opensource. When I first started out, one of the main reasons I was
able to learn was due to other code out there. If you find a bug or would like an improvement, feel
free to give me a message on IRC or fork and submit a pull request. Many hours do go into each plugin,
so, if you're feeling generous, I do accept donations via Amazon. I'm always looking for future work,
so if you are in need of a custom feature or plugin, contact me via GitHub or IRC.

    
