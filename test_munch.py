import json
import pickle
import pytest
from munch import DefaultMunch, Munch, munchify, unmunchify


def test_base():
    b = Munch()
    b.hello = 'world'
    assert b.hello == 'world'
    b['hello'] += "!"
    assert b.hello == 'world!'
    b.foo = Munch(lol=True)
    assert b.foo.lol is True
    assert b.foo is b['foo']

    assert sorted(b.keys()) == ['foo', 'hello']

    b.update({'ponies': 'are pretty!'}, hello=42)
    assert b == Munch({'ponies': 'are pretty!', 'foo': Munch({'lol': True}), 'hello': 42})

    assert sorted([(k, b[k]) for k in b]) == [('foo', Munch({'lol': True})), ('hello', 42), ('ponies', 'are pretty!')]

    assert "The {knights} who say {ni}!".format(**Munch(knights='lolcats', ni='can haz')) == 'The lolcats who say can haz!'


def test_contains():
    b = Munch(ponies='are pretty!')
    assert 'ponies' in b
    assert ('foo' in b) is False

    b['foo'] = 42
    assert 'foo' in b

    b.hello = 'hai'
    assert 'hello' in b

    b[None] = 123
    assert None in b

    b[False] = 456
    assert False in b


def test_getattr():
    b = Munch(bar='baz', lol={})

    with pytest.raises(AttributeError):
        b.foo

    assert b.bar == 'baz'
    assert getattr(b, 'bar') == 'baz'
    assert b['bar'] == 'baz'
    assert b.lol is b['lol']
    assert b.lol is getattr(b, 'lol')


def test_setattr():
    b = Munch(foo='bar', this_is='useful when subclassing')
    assert hasattr(b.values, '__call__')

    b.values = 'uh oh'
    assert b.values == 'uh oh'

    with pytest.raises(KeyError):
        b['values']


def test_pickle():
    b = DefaultMunch.fromDict({"a": "b"})
    assert pickle.loads(pickle.dumps(b)) == b


def test_delattr():
    b = Munch(lol=42)
    del b.lol

    with pytest.raises(KeyError):
        b['lol']

    with pytest.raises(AttributeError):
        b.lol


def test_toDict():
    b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
    assert sorted(b.toDict().items()) == [('foo', {'lol': True}), ('hello', 42), ('ponies', 'are pretty!')]

def test_dict_property():
    b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
    assert sorted(b.__dict__.items()) == [('foo', {'lol': True}), ('hello', 42), ('ponies', 'are pretty!')]

def test_repr():
    b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
    assert repr(b).startswith("Munch({'")
    assert "'ponies': 'are pretty!'" in repr(b)
    assert "'hello': 42" in repr(b)
    assert "'foo': Munch({'lol': True})" in repr(b)
    assert "'hello': 42" in repr(b)

    with_spaces = Munch({1: 2, 'a b': 9, 'c': Munch({'simple': 5})})
    assert repr(with_spaces).startswith("Munch({")
    assert "'a b': 9" in repr(with_spaces)
    assert "1: 2" in repr(with_spaces)
    assert "'c': Munch({'simple': 5})" in repr(with_spaces)

    assert eval(repr(with_spaces)) == Munch({'a b': 9, 1: 2, 'c': Munch({'simple': 5})})


def test_dir():
    m = Munch(a=1, b=2)
    assert dir(m) == ['a', 'b']


def test_fromDict():
    b = Munch.fromDict({'urmom': {'sez': {'what': 'what'}}})
    assert b.urmom.sez.what == 'what'


def test_copy():
    m = Munch(urmom=Munch(sez=Munch(what='what')))
    c = m.copy()
    assert c is not m
    assert c.urmom is not m.urmom
    assert c.urmom.sez is not m.urmom.sez
    assert c.urmom.sez.what == 'what'
    assert c == m


def test_munchify():
    b = munchify({'urmom': {'sez': {'what': 'what'}}})
    assert b.urmom.sez.what == 'what'

    b = munchify({'lol': ('cats', {'hah': 'i win again'}), 'hello': [{'french': 'salut', 'german': 'hallo'}]})
    assert b.hello[0].french == 'salut'
    assert b.lol[1].hah == 'i win again'


def test_unmunchify():
    b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
    assert sorted(unmunchify(b).items()) == [('foo', {'lol': True}), ('hello', 42), ('ponies', 'are pretty!')]

    b = Munch(foo=['bar', Munch(lol=True)], hello=42, ponies=('are pretty!', Munch(lies='are trouble!')))
    assert sorted(unmunchify(b).items()) == [('foo', ['bar', {'lol': True}]), ('hello', 42), ('ponies', ('are pretty!', {'lies': 'are trouble!'}))]


def test_toJSON():
    b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
    assert json.dumps(b) == b.toJSON()


@pytest.mark.parametrize("attrname", dir(Munch))
def test_reserved_attributes(attrname):
    # Make sure that the default attributes on the Munch instance are
    # accessible.

    taken_munch = Munch(**{attrname: 'abc123'})

    # Make sure that the attribute is determined as in the filled collection...
    assert attrname in taken_munch

    # ...and that it is available using key access...
    assert taken_munch[attrname] == 'abc123'

    # ...but that it is not available using attribute access.
    attr = getattr(taken_munch, attrname)
    assert attr != 'abc123'

    empty_munch = Munch()

    # Make sure that the attribute is not seen contained in the empty
    # collection...
    assert attrname not in empty_munch

    # ...and that the attr is of the correct original type.
    attr = getattr(empty_munch, attrname)
    if attrname == '__doc__':
        assert isinstance(attr, str)
    elif attrname in ('__hash__', '__weakref__'):
        assert attr is None
    elif attrname == '__module__':
        assert attr == 'munch'
    elif attrname == '__dict__':
        assert attr == {}
    else:
        assert callable(attr)


def test_getattr_default():
    b = DefaultMunch(bar='baz', lol={})
    assert b.foo is None
    assert b['foo'] is None

    assert b.bar == 'baz'
    assert getattr(b, 'bar') == 'baz'
    assert b['bar'] == 'baz'
    assert b.lol is b['lol']
    assert b.lol is getattr(b, 'lol')

    undefined = object()
    b = DefaultMunch(undefined, bar='baz', lol={})
    assert b.foo is undefined
    assert b['foo'] is undefined


def test_setattr_default():
    b = DefaultMunch(foo='bar', this_is='useful when subclassing')
    assert hasattr(b.values, '__call__')

    b.values = 'uh oh'
    assert b.values == 'uh oh'
    assert b['values'] is None

    assert b.__default__ is None
    assert '__default__' not in b


def test_delattr_default():
    b = DefaultMunch(lol=42)
    del b.lol

    assert b.lol is None
    assert b['lol'] is None


def test_pickle_default():
    b = DefaultMunch.fromDict({"a": "b"})
    assert pickle.loads(pickle.dumps(b)) == b


def test_fromDict_default():
    undefined = object()
    b = DefaultMunch.fromDict({'urmom': {'sez': {'what': 'what'}}}, undefined)
    assert b.urmom.sez.what == 'what'
    assert b.urmom.sez.foo is undefined


def test_copy_default():
    undefined = object()
    m = DefaultMunch.fromDict({'urmom': {'sez': {'what': 'what'}}}, undefined)
    c = m.copy()
    assert c is not m
    assert c.urmom is not m.urmom
    assert c.urmom.sez is not m.urmom.sez
    assert c.urmom.sez.what == 'what'
    assert c == m
    assert c.urmom.sez.foo is undefined
    assert c.urmom.sez.__undefined__ is undefined


def test_munchify_default():
    undefined = object()
    b = munchify(
        {'urmom': {'sez': {'what': 'what'}}},
        lambda d: DefaultMunch(undefined, d))
    assert b.urmom.sez.what == 'what'
    assert b.urdad is undefined
    assert b.urmom.sez.ni is undefined


def test_repr_default():
    b = DefaultMunch(foo=DefaultMunch(lol=True), ponies='are pretty!')
    assert repr(b).startswith("DefaultMunch(None, {'")
    assert "'ponies': 'are pretty!'" in repr(b)
