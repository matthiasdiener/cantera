# -*- coding: utf-8 -*-
#
# Cantera documentation build configuration file, created by
# sphinx-quickstart on Mon Mar 12 11:43:09 2012.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os, re
from pathlib import Path

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../../python'))

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('./exts'))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '2.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.

# sphinxcontrib.matlab has been added to add the MATLAB domain for the
# documentation of the MATLAB functions. It is a new requirement to build the
# documentation in 2.2. It should be loaded before sphinx.ext.autodoc because
# loading it after gives errors when autodocumenting the Python interface.
extensions = [
              'sphinxcontrib.matlab',
              'sphinx.ext.autodoc',
              'sphinx.ext.todo',
              'sphinx.ext.autosummary',
              'sphinxarg.ext',
              'sphinxcontrib.doxylink',
              'sphinx.ext.intersphinx',
              'sphinx_gallery.gen_gallery',
              'sphinx_tags',
              'sphinx_design',
              ]

sphinx_gallery_conf = {
    'filename_pattern': '\.py',
    'image_srcset': ["2x"],
    'examples_dirs': [
       '../samples/python/',
    ],
    'gallery_dirs': [
       'examples/python',
    ],
    'reference_url': {
        'cantera': None,  # 'None' means the locally-documented module
    }
}

# Override sphinx-gallery's method for determining which examples should be executed.
# There's really no way to achieve this with the `filename_pattern` option, and
# `ignore_pattern` excludes the example entirely.
skip_run = {
    # multiprocessing can't see functions defined in __main__ when run by
    # sphinx-gallery, at least on macOS.
    "multiprocessing_viscosity.py",
    # __file__ deliberately not available when run by sphinx-gallery
    "flame_fixed_T.py",
}

def executable_script(src_file, gallery_conf):
    """Validate if script has to be run according to gallery configuration.

    Parameters
    ----------
    src_file : str
        path to python script

    gallery_conf : dict
        Contains the configuration of Sphinx-Gallery

    Returns
    -------
    bool
        True if script has to be executed
    """
    filename = Path(src_file).name
    if filename in skip_run:
        return False
    filename_pattern = gallery_conf["filename_pattern"]
    execute = re.search(filename_pattern, src_file) and gallery_conf["plot_gallery"]
    return execute

import sphinx_gallery.gen_rst
sphinx_gallery.gen_rst.executable_script = executable_script

header_prefix = """
:html_theme.sidebar_secondary.remove:

.. py:currentmodule:: cantera

"""

sphinx_gallery.gen_rst.EXAMPLE_HEADER = header_prefix + sphinx_gallery.gen_rst.EXAMPLE_HEADER

# Options for sphinx_tags extension
tags_create_tags = True
tags_create_badges = True
tags_overview_title = "Index of example tags"
tags_page_title = "Tag"
tags_page_header = "Examples with this tag:"
tags_badge_colors = {
    "Python": "secondary",
}

autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
    'undoc-members': True,
}


def setup(app):
    """Set up an event handler to escape splat characters (*) in docstrings
    when they appear in the introspected function signature.

    This can happen when the ``*args``, ``**kwargs``, or keyword-only marker
    (a plain ``*``) are used in a function signature. The only examples in
    Cantera for which Sphinx issues warnings are __init__ functions, so it
    may be related to the autoclass_content variable below, although I
    didn't investigate.

    This fixes warnings such as "Inline emphasis start marker without end" and
    "Inline strong start marker without end" that Sphinx issues. I'm not sure
    why autodoc doesn't handle this appropriately, but this seems pretty
    effective and not all that fragile.
    """
    def escape_splats(app, what, name, obj, options, lines):
        """This event handler is called each time the autodoc function
        issues a ``process-docstring`` event. The ``lines`` argument
        contains the lines of text that make up the docstring and must
        be modified in place.
        See: https://www.sphinx-doc.org/en/3.x/usage/extensions/autodoc.html#event-autodoc-process-docstring
        """
        splats = re.compile(r"\*args|\*\*kwargs|\s\*[,)]")
        # Since the warnings for Cantera are only issued for classes,
        # scope this replacement to as small a subset as possible. This
        # conditional could be removed if other functions are found to
        # cause this warning.
        if what == "class":
            for i, l in enumerate(lines):
                if splats.search(l) is not None:
                    lines[i] = l.replace("*", r"\*")
    app.connect('autodoc-process-docstring', escape_splats)

autoclass_content = 'both'

doxylink = {
    'ct': (os.path.abspath('../../doc/Cantera.tag'),
            '../../doxygen/html/')
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pint': ('https://pint.readthedocs.io/en/stable/', None),
}

# Ensure that the primary domain is the Python domain, since we've added the
# MATLAB domain with sphinxcontrib.matlab
primary_domain = 'py'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Cantera'
copyright = "2001-2023, Cantera Developers"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

configh = Path('../../../include/cantera/base/config.h').read_text()
# The short X.Y version.
version = re.search('CANTERA_SHORT_VERSION "(.*?)"', configh).group(1)
# The full version, including alpha/beta/rc tags.
release = re.search('CANTERA_VERSION "(.*?)"', configh).group(1)

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all documents.
default_role = 'py:obj'

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'pydata_sphinx_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

html_theme_options = {
    "show_toc_level": 2,
    "navbar_center": ["cantera-org-links"],
    "navbar_end": ["version-switcher", "theme-switcher", "navbar-icon-links"],
    "logo": {
        "link": "/index.html",
        "alt_text": "Cantera",
    },
    "primary_sidebar_end": ["numfocus"],
    "switcher": {
        "json_url": "/documentation/dev/sphinx/html/_static/doc-versions.json",
        # "json_url": "https://cantera.org/doc-versions.json",
        "version_match": version,
    },
    "check_switcher": False,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Cantera/cantera",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        }
   ],
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['.']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "Cantera"

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/images/cantera-logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = "_static/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'custom.css',
]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'Canteradoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'Cantera.tex', 'Cantera Documentation',
   'Cantera Developers', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'cantera', 'Cantera Documentation',
     ['Cantera Developers'], 1)
]
