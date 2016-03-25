# PmWiki -> Mediawiki parser

A parser to convert PmWiki markup to Mediawiki markup for when migrating from pw to mw.

Note that the target installation that this is written for is in swedish and so might give strange results if that is not your language of choice.

## Todo

* Options is a PITA.
* Tables?
* A simple script using the parser.

## What works

* [++ bigger ++]
* [-- smaller --]
* [[ links | link test ]]
* even [[ Profile/Links ]] are translated to [[ Användare:Links ]] *again because of swedish*.
* unformatted text
