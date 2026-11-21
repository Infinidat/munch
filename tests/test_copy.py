from copy import deepcopy

from munch import Munch


def test_copy_is_shallow(munch_obj):
    nested = {'values': []}
    munch_obj['nested'] = nested
    munch_obj['sequence'] = [nested]
    copied = munch_obj.copy()

    assert type(copied) is type(munch_obj)
    assert copied is not munch_obj
    assert copied['nested'] is nested
    assert copied['sequence'] is munch_obj['sequence']
    copied['extra'] = True
    assert 'extra' not in munch_obj
    copied['nested']['values'].append('shared')
    assert munch_obj['nested']['values'] == ['shared']


def test_shallow_copy_keeps_references_to_original(munch_obj):
    munch_obj['self'] = munch_obj
    copied = munch_obj.copy()
    assert copied is not munch_obj
    assert copied['self'] is munch_obj


def test_explicit_deepcopy_still_copies_nested_values():
    original = Munch(nested=Munch(values=[]))
    original['self'] = original
    copied = deepcopy(original)
    assert copied is not original
    assert copied['self'] is copied
    assert copied.nested is not original.nested
    assert copied.nested['values'] is not original.nested['values']
