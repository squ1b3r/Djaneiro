===============================
Sublime Text 2 Django Snippets
===============================
Overview
--------

This is the first part of a set of snippets for
`Sublime Text 2 <http://www.sublimetext.com/>`_ to use in Django
templates. At the moment it includes snippets for all standard Django templates tags.

Installation
------------

1. Clone this repo
2. Put the contents of this repo directly inside:

 - OS X: ~/Library/Application Support/Sublime Text 2/Packages/HTML (Django)/
 - Windows: %APPDATA%/Sublime Text 2/Packages/HTML (Django)/
 - Linux: ~/.Sublime Text 2/Packages/HTML (Django)/

3. Don't forget to turn on django mode View → Syntax → HTML (Django)
4. That's it, you can use the snippets now.

Snippets list
-------------
=============== ======================================================
 Abbreviation                        Tag
=============== ======================================================
 autoescape      ``{% autoescape %} {% autoescape %}``
 block           ``{% block %} {% endblock %}``
 comment         ``{% comment %} {% endcomment %}``
 csrf_token      ``{% csrf_token %}``
 cycle           ``{% cycle %}``
 debug           ``{% debug %}``
 ext             ``{% extends "" %}``
 extends         ``{% extends "" %}``
 filter          ``{% filter %} {% endfilter %}``
 firstof         ``{% firstof %}``
 for             ``{% for in %} {% endfor %}``
 fore            ``{% for in %} {% empty %} {% endfor %}``
 if              ``{% if %} {% endif %}``
 ifchanged       ``{% ifchanged %} {% endifchanged %}``
 ife             ``{% if %} {% else %} {% endif %}``
 ifelse          ``{% if %} {% else %} {% endif %}``
 ifeq            ``{% ifequal %} {% endifequal %}``
 ifequal         ``{% ifequal %} {% endifequal %}``
 ifnotequal      ``{% ifnotequal %} {% endifnotequal %}``
 inc             ``{% include %}``
 include         ``{% include %}``
 load            ``{% load %}``
 now             ``{% now "" %}``
 regroup         ``{% regroup by as %}``
 spaceless       ``{% spaceless %} {% endspaceless %}``
 ssi             ``{% ssi %}``
 templatetag     ``{% templatetag %}``
 url             ``{% url %}``
 widthratio      ``{% widthratio %}``
 with            ``{% with as %} {% endwith %}``
 trans           ``{% trans %}``
 blocktrans		 ``{% blocktrans with as %} {% endblocktrans %}``
=============== ======================================================

...and some non-official stuff:

=============== ======================================================
 Abbreviation                        Tag
=============== ======================================================
 super           ``{{ block.super }}``
 extrahead       ``{% block extrahead %} {% endblock extrahead %}``
 extrastyle      ``{% block extrastyle %} {% endblock extrastyle %}``
 var		     ``{{ }}``	
=============== ======================================================


Hints
-----

You can use the *Tab* key to move the cursor to next logical position. For example use the ``for``
snippet and hit *Tab* to see how the cursor moves.