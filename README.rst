==================================
Django support for Sublime Text 2
==================================
Overview
--------

Installation
------------

1. Clone this repo
2. Put the contents of this repo directly inside:

 - OS X: ~/Library/Application Support/Sublime Text 2/Packages/
 - Windows: %APPDATA%/Sublime Text 2/Packages/
 - Linux: ~/.Sublime Text 2/Packages/

Snippets for Django templates
------------------------------
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

Snippets for Django model fields
---------------------------------
=============== ======================================================
 Abbreviation                        Tag
=============== ======================================================
 m_auto          ``models.AutoField()``
 m_bigint        ``models.BigIntegerField()``
 m_bool          ``models.BooleanField()``
 m_char          ``models.CharField()``
 m_coseint       ``models.CommaSeparatedIntegerField()``
 m_date          ``models.DateField()``
 m_datetime      ``models.DateTimeField()``
 m_decimal       ``models.DecimalField()``
 m_email         ``models.EmailField()``
 m_file          ``models.FileField()``
 m_filepath      ``models.FilePathField()``
 m_float         ``models.FloatField()``
 m_img           ``models.ImageField()``
 m_int           ``models.IntegerField()``
 m_ip            ``models.IPAddressField()``
 m_nullbool      ``models.NullBooleanField()``
 m_phone         ``models.PhoneNumberField()``
 m_posint        ``models.PositiveIntegerField()``
 m_possmallint   ``models.PositiveSmallIntegerField()``
 m_slug          ``models.SlugField()``
 m_smallint      ``models.SmallIntegerFiled()``
 m_text          ``models.TextField()``
 m_time          ``models.TimeField()``
 m_url           ``models.URLField()``
 m_usstate       ``models.USStateField()``
 m_xml           ``models.XMLField()``
 fk              ``models.ForeignKey()``
 m2m             ``models.ManyToManyField()``
 o2o             ``models.OneToOneField()``
=============== ======================================================

Snippets for Django form fields
--------------------------------
=============== ======================================================
 Abbreviation                        Tag
=============== ======================================================
 f_char          ``forms.CharField()``
 f_choice        ``forms.ChoiceField()``
 f_combo         ``forms.ComboField()``
 f_date          ``forms.DateField()``
 f_datetime      ``forms.DateTime()``
 f_decimal       ``forms.DecimalField()``
 f_email         ``forms.EmailField()``
 f_file          ``forms.FileField()``
 f_filepath      ``forms.FilePathField()``
 f_float         ``forms.FloatField()``
 f_img           ``forms.ImageField()``
 f_int           ``forms.IntegerField()``
 f_ip            ``forms.IPAddressField()``
 f_mochoice      ``forms.ModelChoiceField()``
 f_momuchoice    ``forms.ModelMultipleChoiceField()``
 f_muchoice      ``forms.MultipleChoiceField()``
 f_muval         ``forms.MultipleValueField()``
 f_nullbool      ``forms.NullBooleanField()``
 f_regex         ``forms.RegexField()``
 f_slug          ``forms.SlugField()``
 f_sdatetime     ``forms.SplitDateTime()``
 f_time          ``forms.TimeField()``
 f_tchoice       ``forms.TypedChoiceField()``
 f_tmuchoice     ``forms.TypedMultipleChoiceField()``
 f_url           ``forms.URLField()``
=============== ======================================================

Completions
------------

    Full list of all available settings

- null
- blank
- choices
- db_column
- db_index
- db_tablespace
- default
- related_name
- editable
- error_message
- help_message
- primary_key
- unique
- unique_together
- unique_for_date
- unique_for_month
- unique_for_year
- verbose_name
- verbose_name_plural
- validators
- auto_now_add
- auto_now

- required
- label
- initial
- widget
- localized

- return
- RequestContext
- context_instance
- render_to_response
- render
- redirect
- get_object_or_404
- get_list_or_404