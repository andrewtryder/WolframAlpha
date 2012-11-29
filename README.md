Documentation for the WolframAlpha plugin for Supybot

  Purpose

    Queries WolframAlpha and displays textual results.

  Usage

    Set the apikey configuration variable in order for queries to work.

  Commands

    * wolf <input>

      Query WolframAlpha and display results.

  Configuration

    * supybot.plugins.WolframAlpha.public

      This config variable defaults to True and is not channel specific.

      Determines whether this plugin is publicly visible.

    * supybot.plugins.WolframAlpha.apikey

      This config variable defaults to "" and is not channel specific.

      The API key to use in queries.

