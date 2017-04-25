.. Networks and Game Theory documentation master file, created by
   sphinx-quickstart on Thu Apr 20 11:49:17 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Networks and Game Theory's documentation!
====================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



#################
About the project
#################

* Game API
* GUI to play the game
* Analysis tools


For subtitles, switch to another punctuation mark
-------------------------------------------------

*Italic* **bold** ``name`` ``function()`` ``expression = 3 + 3``

`Hyperlink <http://en.wikipedia.org/wiki/Hyperlink>`_ `Link`_

.. _Link: http://en.wikipedia.org/wiki/Link_(The_Legend_of_Zelda)

.. image:: _img/figure_1-1.png

.. A comment block starts with two periods, can continue indented.

A paragraph is one or more lines of un-indented text, separated
from the material above and below by blank lines.

	“Block quotes look like paragraphs, but are indented with
	one or more spaces.”

| Because of the pipe characters, this will become one line,
| And this will become another line, like in poetry.

term
	Definition for the “term”, indented beneath it.
another term
	And its definition; any of these definitions can continue on for
	several lines by -- you guessed it! -- being similarly indented.

* Each item in a list starts with an asterisk (or “1.”, “a.”, etc).
* List items can go on for several lines as long as you remember to
  keep the rest of the list item indented.

Code blocks are introduced by a double-colon and are indented::

	import docutils
	print help(docutils)

>>> print 'But doctests start with ">>>" and need no indentation.'


.. note::

	Your note should consist of one or more paragraphs, all indented
	so that they clearly belong to the note and not to the text or
	directive that follows.

	Many other directives are also supported, including: warning,
	versionadded, versionchanged, seealso, deprecated, rubric,
	centered, hlist, glossary, productionlist.

.. code-block:: c
   :linenos:

	/* Or say "highlight::" once to set the language for all of the
	   code blocks that follow it. Options include ":linenos:",
	   ":linenothreshold:", and ":emphasize-lines: 1,2,3". */

	char s[] = "You can also say 'python', 'ruby', ..., or 'guess'!";

.. literalinclude:: example.py
	:lines: 10-20
	:emphasize-lines: 15,16

.. module:: httplib

.. class:: Request

	Zero or more paragraphs of introductory material for the class.

	.. method:: send()

		Description of the send() method.

	.. attribute:: url

		Description of the url attribute.

	Many more members are possible than just method and attribute,
	and non-Python languages are supported too; see the Sphinx docs
	for more possibilities!

.. testcode::

	print 'The doctest extension supports code without >>> prompts!'

.. testoutput::

	The doctest extension supports code without >>> prompts!

.. _custom-label:

.. index:: single: paragraph, targeted paragraph, indexed paragraph

This paragraph can be targeted with :ref:`Lourd <custom-label>`, and will also
be the :index:`target` of several index entries!

This paragraph will be listed in the index under both “wire, copper”
and “copper, wire.” See the Sphinx documentation for even more complex
ways of building index entries.

Many kinds of cross-reference can be used inside of a paragraph:



