# Project Information
project = "RSVP"
version = "v6"
author = "ManEatingApe"
copyright = "2020, ManEatingApe"

# Exclude RST source files from output
html_copy_source = False

# Warn about references where target cannot be found
nitpicky = True

# Add logo to sidebar
html_logo = "images/rsvp_logo_white_small.png"

# Import extensions
import sys
import os
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath("."))

extensions = [
    "sphinx_rtd_theme",
    "kerboscript_lexer"
]

# Use ReadTheDocs theme
html_theme = "sphinx_rtd_theme"

# Customize Theme
html_theme_options = {
    "logo_only": True
}

# Highlight source blocks
highlight_language = "kerboscript"