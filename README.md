# PmWiki -> Mediawiki parser

A parser to convert PmWiki markup to Mediawiki markup for when migrating from pw to mw.

Note that the target installation that this is written for is in swedish and so might give strange results if that is not your language of choice.

## Todo

* Tables?
* A simple script using the parser.
* Script for inserting converted markup into the mediawiki specified

## What works

* [++ bigger ++]
* [-- smaller --]
* [[ links | link test ]]
* even [[ Profile/Links ]] are translated to [[ Användare:Links ]] *again because of swedish*.
* unformatted text
* options
