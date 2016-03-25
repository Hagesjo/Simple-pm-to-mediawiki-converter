#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import sub, findall, search
from collections import defaultdict

# TODO: code cleanup, and a few rewrites

def main(text):
	"""Test function for longer texts"""
	inputs = text.split('\n\n')
	outp = ""
	for i in inputs:
		i = '\n' + i
		outp += '\n' + parse(i)
	return outp

def parse(text, *args, **kwargs):
	"""For each character, try to look it up in a dict if it
        matches with any tag, else continue with next character.

        Note, this parser does not consume any characters on a match, it simply
        forwards the string from the matched character."""

	outp = ""
	for index, t in enumerate(text):
		if t in spec:
			if args or kwargs:
				return outp + spec[t](text[index:], *args, **kwargs)
			else:
				return outp + spec[t](text[index:])
		else:
			outp += t
	return outp

def separat(text):
	"""Converts headers (separators)

	Arguments:
	text	-- n*! + tag/text

	output	-- n*= tag/text n*=
	"""

	text = text.split('\n', 1)
	num = 0
	for index, c in enumerate(text[0]):
		if c == '!':
			num += 1
			index += 1
		else:
			break

	if num <= 1 or index == len(text[0]):
		return text[0] + '\n' +  parse(text[1])

	outp = '=' * num

	text[0] = text[0][index:]
	for index, c in enumerate(text[0]):
		if c in spec:
			outp += spec[c](text[0][index:])
			break
		else:
			outp += c
	outp += '=' * num + '\n'

	if len(text) == 1:
		return outp
	else:
		return outp + parse('\n' + text[1])

def comment(text, *args):
	"""Converts inline comment.

	Arguments:
	text	--	%comment% tag/text\n

	output	--	<!--tag/text--!>
	"""

	text = text.split('\n', 1)
	outp = ""
	for index, c in enumerate(text[0]):
		if c in spec:
			outp += spec[c](text[0][index:])
			break
		else:
			outp += c
	outp = "<!--" + outp + "-->\n" 

	if len(text) == 1:
		return outp
	else:
		return outp + parse(text[1])

def revident():
	pass

def writer(text):
	"""Ignoring all monospaced syntax and converts it to normal text

	Arguments:
	text	--	@@text@@

	output	--	text
	"""

	if text[1] == "@":
		inside, outside = text[2:].split("@@", 2)
		return inside + parse(outside)
	else:
		return text[0] + parse(text[1])

def bracket(text):
	"""Pass-through function which has matched with '[', and tries to match with
	corresponding tags including the second and third letter as well.
	E.g tags such as [[links]]
	"""

	if len(text) == 1:
		return text

	if text[1] in inbracket:
		return inbracket[text[1]](text[1:])

        # If the first character does not contain a valid bracket character
        # it is simply returned and the string after it is parsed.
	else:
		return text[0] + parse(text[1:])

def expo():
	pass

def down():
	pass

def line(text):
	"""Pass-through function which has matched with '{', and tries to match with
	corresponding tags including the second letter as well.
	E.g tags such as {+underline+}
	"""

	if len(text) == 1:
		return text[0]
	if text[1] in inline:
		return inline[text[1]](text[2:])

def attach(text, *single_options, **dict_options):
	"""Converts attachment tag

	Argument:
	text	--	attach:image.png
	options	--	hashmap with options for the attachement

	output	--	[[File:image.png|option|optionvalue]]
	"""

	if text[1:6] == "ttach":
		text = text[7:].split(None, 1) # Remove "Attach:"
		outp = "\n"
		outp += "[[File:%s" % text[0] # pls no spaces in files
		for option in single_options:
			outp += '|%s' % option_translate[option]
		for option in dict_options:
			outp += '|%s%s' % (option_translate[option], dict_options[option])
		outp += "]]\n\n"

		if len(text) == 1:
			return outp
		else:
			return outp + parse(text[1])
	else:
		return text[0] + parse(text[1:])

option_translate = {
	'width' : '',
	'height' : 'x',
	'center' : 'center'
}

def option(text, *single_options, **dict_options):
	"""Adds option parsed to the tag that follows this option

	Arguments:
	text			--	Either %option% or %option=value%, followed by the rest of the text
	single_option	--	A list of previous options to be sent to the next tag
	dict_options	--	A list of previous options + values to be sent to the next tag
	"""

	single_options = list(single_options)

	text = text[1:].split('%', 1)
	option = text[0].split('=')

	if len(option) == 2:
		dict_options[option[0]] = option[1]
	else:
		single_options.append(option[0])

	return parse(text[1], *single_options, **dict_options)

def mident(text):
	"""Pass-through function which matches with "-" and tries to match with
	corresponding tags including the second letter as well.
	E.g tags such as "->"
	"""

	if len(text) == 1:
		return text

	if text[1] in indents:
		return indents[text[1]]
	else:
		return "-" + parse(text[1:])

def ident():
	pass

def revident():
	pass

def link(text):
	"""Links are pretty similar syntax in pm/mediawiki.
	so all this function does is to remove any "Main/." which exists
	in the path, since this is not needed in mediawiki"""
	text = text.split(']]',1)

	# Readd the striped away bracket
	outp = "[" + text[0]

	# Strip away Main
	outp = outp.replace("Main/", "")
	outp = outp.replace("Main.", "")

	# Rewrite profile links (yes our mediawiki is configured to swedish)
	outp = outp.replace("~", "Användare:")
	outp = outp.replace("Profiles/", "Användare:")

	outp = outp + "]]" 
	if len(text) == 1:
		return outp
	else:
		return outp + parse(text[1])
	pass

def bigger(text):
	"""Treat big as binary. I.e [++++ is the same as [+, since only <big> exists
	(If you don't want to use font size and stuff, but that's not needed in our case"""
	text = text.split(']', 1)
	for num, c in enumerate(text[0]):
		if c != '+':
			break

	text[0] = text[0][num:-num]
	outp = ""

	for index, c in enumerate(text[0]):
		if c in spec:
			outp += spec[c](text[0][index:])
			break
		else:
			outp += c

	outp = "<big>" + outp + "</big>"

	if len(text) == 1:
		return outp
	else:
		return outp + parse(text[1])


def lesser(text):
	"""Treat small as binary. I.e [++++ is the same as [+, since only <small> exists
	(If you don't want to use font size and stuff, but that's not needed in our case"""
	text = text.split(']', 1)
	for num, c in enumerate(text[0]):
		if c != '-':
			break

	text[0] = text[0][num:-num]
	outp = ""

	for index, c in enumerate(text[0]):
		if c in spec:
			outp += spec[c](text[0][index:])
			break
		else:
			outp += c

	outp = "<small>" + outp + "</small>"

	if len(text) == 1:
		return outp
	else:
		return outp + parse(text[1])

def uline(text):
	text = text.split('+}', 1)
	outp = "<u>" + text[0] + "</u>" 
	if len(text) == 1:
		return outp
	else:
		return outp + parse(text[1])
def strike(text):
	text = text.split('-}', 1)
	return "<strike>" + text[0] + "</strike>" + parse(text[1])

def fil(text):
	for i in range(2,4): # TODO: one letter at a time.
		if text[1:i] in fils:
			return text[0] + fils[text[1:i]](text[1:])
	return text[0] + parse(text[1:])

def table(text):
	outp = ""
	text = text.split('\n')
	attributes = dict(map(lambda x: x.split('='), text.pop(0)[2:].split())) # If we want to do anything with this

	for i, line in enumerate(text):
		if line[:2] != "||" or line == "||": #This might look like a weird if
			return '{| class="wikitable"\n' + outp + '|}\n' + parse('\n'.join(text[i + 1:]))
		else:
			cols = line.split('||')[1:-1]
			for j, col in enumerate(cols):
				if col[:1] == '!': # Cool way to avoid index out of bounds
					outp += col + '\n'
				else:
					outp += '|%s\n' % parse(col)
			outp += '|-\n'
	return outp

def parant(text):
	if text[1] in inparant:
		inside, outside = text.split(':)', 1)
	#  might implement later
	#	if inside in parant_vars: 
	#		parant_vars[inside](outside)
		return parse(outside)
	else:
		return "(" + parse(text[1:])

def mextbox(text):
	"""Checks if boxtag is valid for parsing, and then calls the corresponding parse function

	Arguments:
	text -- >>boxtag<<
			Boxtagsyntax
			>><< 
	 """
	if text[1] == ">":
		whole = text[2:].split("<<", 2)
		if whole[0] in boxtags:
			return boxtags[whole[0]](whole[1:])
		else:
			return parse(whole[2]) if len(whole) == 3 else  ''
	else:
		return text[0] + parse(text[1:])


def categories(text):
	""" Convert comment tag

	Arguments:
	text -- ["Kategorier: [[!list]] | [[!of]] | [[!categories]]>>", MAYBE text after the tag]

	Converts to:
	[[Category:list]]
	[[Category:of]]
	[[Category:categories]]
	"""
	outp = ""
	cats = text[0].split(":")[1]
	cats = cats.replace("[[!","").replace("]]","")
	cats = cats.replace("||", "|") # Sometimes, the separator is || instead of | because people
	cats = cats[:-2].split("|") # Remove trailing <<

	for c in cats:
		outp += "[[Category:%s]]\n" % c.strip()

	return outp + (parse(text[1]) if len(text) == 2 else '')

boxtags = {"kategorier" : categories}

def vars(text):
	""":foo:bar\n
	to
	foo
	:bar
	"""
	text = text.split('\n', 1)
	varname, context = findall(":(.*?):(.*)", text[0])[0] #Meh
	outp = "%s\n:%s%s" % (varname, parse(context), (parse(text[1]) if len(text) == 2 else ''))
	return outp

parant_vars = {} # add if we find useful parameters later on...

inparant = {
	":" : parant }

spec = {
	"@" : writer,
	"[" : bracket,
	"^" : expo,
	"_" : down,
	"{" : line,
	"A" : attach,
	"a" : attach,
	"%" : option,
	"-" : mident,
	"\n": fil, #first in line
	"(" : parant,
	">" : mextbox
}

inbracket = {
	"[" : link,
	"+" : bigger, 
	"-" : lesser 
}

indents = {
	">" : ident,
	"<" : revident 
}

inline = {
	"+" : uline,
	"-" : strike 
}

fils = {
        "!" : separat,
	"||" : table,
	":" : vars
}

inoption = {
	"comment" : comment,
}
