import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LabToolkit'
copyright = '2023, David Lutton'
author = 'David Lutton'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = ["myst_parser"]
# extensions = []
extensions = [
    'sphinx.ext.autodoc',  # Core library for html generation from docstrings
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',  # Create neat summary tables

]
autosummary_generate = True  # Turn on sphinx.ext.autosummary


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


import labtoolkit
class stubinst:
    ...
    def query(self, *args, **kwargs):
        ...
        return ''
    def close(self, *args, **kwargs):
        ...

class stubrm:
    ...
    def open_resource(self, *args, **kwargs):
        return stubinst()

em = labtoolkit.Enumerate(resourcemanager=stubrm(), resources=[''])
em.driver_load_all()
