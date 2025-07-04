# Configuration file for the Sphinx documentation builder.

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Project information
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import re
import sys
from datetime import datetime

import sphinx_autosummary_accessors
from sphinx_gallery.sorting import ExplicitOrder

from opti_extensions import __version__

sys.path.insert(0, os.path.abspath('..'))

project = 'opti-extensions'
copyright = f'{datetime.now().year}, Samarth Mistry'
author = 'Samarth Mistry'
release = version = __version__

# General configuration
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_autosummary_accessors',
    'sphinx_design',
    'sphinx_gallery.gen_gallery',
    'sphinx_copybutton',
    'notfound.extension',
    'numpydoc',
]

autodoc_typehints = 'none'
add_module_names = False
numpydoc_show_class_members = False

html_css_files = ['css/custom.css']
templates_path = ['_templates', sphinx_autosummary_accessors.templates_path]
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# Options for Sphinx-gallery
# https://github.com/sphinx-gallery/sphinx-gallery

sphinx_gallery_conf = {
    'examples_dirs': '../../examples',  # path to your example scripts
    'filename_pattern': f'{re.escape(os.sep)}example_',
    'gallery_dirs': 'auto_examples',  # path to where to save gallery generated output
    'subsection_order': ExplicitOrder(
        [
            '../../examples/data_structures_overview',
            '../../examples/model_building',
            '../../examples/cplex_tuner',
            '../../examples/cplex_runseeds',
        ]
    ),  # sorting gallery subsections
    'within_subsection_order': 'FileNameSortKey',
    'thumbnail_size': (1, 1),
    'download_all_examples': False,
}

# Options for HTML output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# https://sphinxdocs.ansys.com/version/stable/user-guide/options.html

html_short_title = html_title = 'opti-extensions documentation'
html_theme = 'ansys_sphinx_theme'
html_static_path = ['_static']
html_favicon = os.path.abspath('_static/favicon.png')
html_sidebars = {'installation/*': []}
html_context = {
    'github_user': 'samarthmistry',
    'github_repo': 'opti-extensions',
    'github_version': 'main',
    'doc_path': 'docs/src',
}
html_theme_options = {
    'logo': {
        'image_light': '_static/logo-light.jpg',
        'image_dark': '_static/logo-dark.jpg',
    },
    'github_url': 'https://github.com/samarthmistry/opti-extensions',
    'navbar_align': 'left',
    'show_breadcrumbs': True,
    'collapse_navigation': False,
    'show_prev_next': False,
    'footer_start': [],  # ['sphinx-version', 'copyright'],
    'footer_end': [],  # ['theme-version'],
}
html_show_sourcelink = False
suppress_warnings = ['misc.copy_overwrite']


# Docstring validation with numpydoc
# https://numpydoc.readthedocs.io/en/latest/validation.html

numpydoc_validation_checks = {
    'all',  # All checks except those below:
    'GL01',  # Summary should start in the line immediately
    'ES01',  # Extended summary not found
    'SA01',  # 'See Also' section not found
    'EX01',  # 'Examples' section not found
    'PR07',  # Parameter has no description
    'RT03',  # Return value has no description
}
numpydoc_validation_exclude = {
    '.name',  # property
    '.names',  # property
    '.key_name',  # property
    '.key_names',  # property
    '.value_name',  # property
}
numpydoc_validation_overrides = {
    'PR01': [
        '^Not supported by ',  # _param_dicts.ParamDictBase.update, .fromkeys
        #                      # _var_dicts.VarDictBase.pop, setdefault, .update, .fromkeys
        '^Solve a DOcplex model ',  # _model_funcs.solve
    ],
    'PR02': [
        '^Not supported by ',  # _param_dicts.ParamDictBase.update, .fromkeys
        #                      # _var_dicts.VarDictBase.pop, setdefault, .update, .fromkeys
        '^Solve a DOcplex model ',  # _model_funcs.solve
    ],
    'SS05': [
        '^Preprocess ',  # _var_funcs._preprocess_bound
    ],
}

# autodoc configuration
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html


def autodoc_skip_member(app, what, name, obj, skip, options):
    # Ref: https://stackoverflow.com/a/21449475/
    to_skip = (
        ('dict', 'keys'),
        ('dict', 'values'),
        ('dict', 'items'),
        ('ParamDictBase', 'copy'),
        ('ParamDictBase', 'update'),
        ('ParamDictBase', 'fromkeys'),
        ('VarDictBase', 'clear'),
        ('VarDictBase', 'copy'),
        ('VarDictBase', 'pop'),
        ('VarDictBase', 'popitem'),
        ('VarDictBase', 'setdefault'),
        ('VarDictBase', 'update'),
        ('VarDictBase', 'fromkeys'),
    )

    skip = False
    if what == 'method':
        cls_name = obj.__qualname__.split('.')[0]
        if (cls_name, name) in to_skip:
            skip = True

    return True if skip else None


def autodoc_process_signature(app, what, name, obj, options, signature, return_annotation):
    # Override constructor signature for VarDict classes to show up as blank as they are not exposed
    # in the public API
    if what == 'class':
        if obj.__name__ in ('VarDict1D', 'VarDictND'):
            signature = ''
    return (signature, return_annotation)


def autodoc_override_docstring(app, what, name, obj, options, lines):
    # Override constructor docstring for VarDict classes with a message as they are not exposed in
    # the public API
    if what == 'class':
        if obj.__name__ in ('VarDict1D', 'VarDictND'):
            # Modify `lines` inplace
            module = obj.__module__.rsplit('.', 1)[0]
            if module.endswith('docplex'):
                func = 'add_variables'
            elif module.endswith('gurobipy'):
                func = 'addVars'
            else:  # xpress
                func = 'addVariables'
            lines[:] = [
                f'This class is not meant to be instantiated; {obj.__name__} is built through the '
                f'``{module}.{func}`` function.',
            ]


def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip_member)
    app.connect('autodoc-process-signature', autodoc_process_signature)
    app.connect('autodoc-process-docstring', autodoc_override_docstring)
