<p>To install the user created importable python modules they should be copied to this location:</p>

<pre>
~/.local/lib/python2.7/site-packages/
</pre>

<p>If this doesn't exist yet, create as follows:</p>

<pre>
$ mkdir -p "`python -m site --user-site`"
</pre>

<p>You should also place: __init__.py in the same folder so that it will be treated as a Python package</p>

