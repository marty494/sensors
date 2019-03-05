User created importable python modules should be placed here:

~/.local/lib/python2.7/site-packages/

If this doesn't exist yet, create as follows:

$ mkdir -p "`python -m site --user-site`"

You should also place: __init__.py in the same folder so that it will be treated as a Python package

