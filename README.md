[![Build Status](https://travis-ci.org/Infinidat/munch.svg?branch=master)](https://travis-ci.org/Infinidat/munch)
[![Latest Version](https://img.shields.io/pypi/v/munch.svg)](https://pypi.python.org/pypi/munch/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/munch.svg)](https://pypi.python.org/pypi/munch/)
[![Downloads](https://img.shields.io/pypi/dm/munch.svg)](https://pypi.python.org/pypi/munch/)

munch
==========

munch is a fork of David Schoonover's **Bunch** package, providing similar functionality. 99% of the work was done by him, and the fork was made mainly for lack of responsiveness for fixes and maintenance on the original code.

Munch is a dictionary that supports attribute-style access, a la JavaScript.

````py
>>> b = Munch()
>>> b.hello = 'world'
>>> b.hello
'world'
>>> b['hello'] += "!"
>>> b.hello
'world!'
>>> b.foo = Munch(lol=True)
>>> b.foo.lol
True
>>> b.foo is b['foo']
True
````


Dictionary Methods
------------------

A Munch is a subclass of ``dict``; it supports all the methods a ``dict`` does:

````py
>>> b.keys()
['foo', 'hello']
````

Including ``update()``:

````py
>>> b.update({ 'ponies': 'are pretty!' }, hello=42)
>>> print repr(b)
Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
````

As well as iteration:

````py
>>> [ (k,b[k]) for k in b ]
[('ponies', 'are pretty!'), ('foo', Munch(lol=True)), ('hello', 42)]
````

And "splats":

````py
>>> "The {knights} who say {ni}!".format(**Munch(knights='lolcats', ni='can haz'))
'The lolcats who say can haz!'
````


Serialization
-------------

Munches happily and transparently serialize to JSON and YAML.

````py
>>> b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
>>> import json
>>> json.dumps(b)
'{"ponies": "are pretty!", "foo": {"lol": true}, "hello": 42}'
````

If JSON support is present (``json`` or ``simplejson``), ``Munch`` will have a ``toJSON()`` method which returns the object as a JSON string.

If you have [PyYAML](http://pyyaml.org/wiki/PyYAML) installed, Munch attempts to register itself with the various YAML Representers so that Munches can be transparently dumped and loaded.

````py
>>> b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
>>> import yaml
>>> yaml.dump(b)
'!munch.Munch\nfoo: !munch.Munch {lol: true}\nhello: 42\nponies: are pretty!\n'
>>> yaml.safe_dump(b)
'foo: {lol: true}\nhello: 42\nponies: are pretty!\n'
````

In addition, Munch instances will have a ``toYAML()`` method that returns the YAML string using ``yaml.safe_dump()``. This method also replaces ``__str__`` if present, as I find it far more readable. You can revert back to Python's default use of ``__repr__`` with a simple assignment: ``Munch.__str__ = Munch.__repr__``. The Munch class will also have a static method ``Munch.fromYAML()``, which loads a Munch out of a YAML string.

Finally, Munch converts easily and recursively to (``unmunchify()``, ``Munch.toDict()``) and from (``munchify()``, ``Munch.fromDict()``) a normal ``dict``, making it easy to cleanly serialize them in other formats.


Undefined
---------

If you want something that behaves more closely to JavaScript with regards to
missing keys, you can use ``UMunch``. It returns the special object
``undefined`` for any attributes that are missing.

````py
>>> b = UMunch({'hello': 'world!'})
>>> b.hello
'world!'
>>> b.foo
undefined
>>> b.foo == None
True
>>> b.foo is None
False
````


Miscellaneous
-------------

* It is safe to ``import *`` from this module. You'll get: ``Munch``, ``UMunch``, ``munchify``, ``unmunchify`` and ``undefined``.
* Ample Tests. Just run ``pip install tox && tox`` from the project root.

Feedback
--------

Open a ticket / fork the project on [GitHub](http://github.com/Infinidat/munch).
