#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2020 Cecil Curry.
# See "LICENSE" for further details.

'''
**Beartype PEP-agnostic type hint getter utilities** (i.e., callables querying
arbitrary objects for attributes specific to PEP-agnostic type hints).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                           }....................
from beartype.roar import BeartypeDecorHintException
from beartype._util.hint.pep.utilhintpepdata import (
    TYPING_ATTR_TO_TYPE_GET)

# See the "beartype.__init__" submodule for further commentary.
__all__ = ['STAR_IMPORTS_CONSIDERED_HARMFUL']

# ....................{ IMPORTS                           }....................
def get_hint_type_origin(hint: object) -> type:
    '''
    **Origin type** (i.e., non-:mod:`typing` superclass suitable for shallowly
    type-checking all parameters and return values annotated by the passed
    PEP-agnostic type hint by calling the :func:`isinstance` builtin with those
    parameters or return values and that superclass) of this hint if this hint
    originates from such a superclass *or* raise an exception otherwise (i.e.,
    if this hint originates from *no* such superclass).

    This getter is intentionally *not* memoized (e.g., by the
    :func:`callable_cached` decorator), as the implementation trivially reduces
    to an efficient test.

    Parameters
    ----------
    hint : object
        Object to be inspected.

    Returns
    ----------
    type
        If this object is:

        * A non-:mod:`typing` class (e.g., :class:`str`), this object as is.
        * An argumentless :mod:`typing` object originating from a
          non-:mod:`typing` superclass (e.g., :attr:`typing.Dict`, associated
          with :class:`dict`), that superclass.

    Raises
    ----------
    TypeError
        If this object is **unhashable** (i.e., *not* hashable by the builtin
        :func:`hash` function and thus unusable in hash-based containers like
        dictionaries and sets). All supported type hints are hashable.
    BeartypeDecorHintPepException
        If this object does *not* originate from a non-:mod:`typing`
        superclass.
    '''

    # Non-"typing" superclass from which this object originates if any *OR*
    # "None" otherwise.
    hint_type_origin = get_hint_type_origin_or_none(hint)

    # If this superclass exists, return this superclass.
    if hint_type_origin is not None:
        return hint_type_origin

    # Else, no such superclass exists. In this case, raise an exception.
    raise BeartypeDecorHintException(
        'PEP-agnostic type hint {!r} '
        'originates from no non-"typing" type.'.format(hint))


def get_hint_type_origin_or_none(hint: object) -> 'NoneTypeOr[type]':
    '''
    **Origin type** (i.e., non-:mod:`typing` superclass suitable for shallowly
    type-checking all parameters and return values annotated by the passed
    PEP-agnostic type hint by calling the :func:`isinstance` builtin with those
    parameters or return values and that superclass) of this hint if this hint
    originates from such a superclass *or* ``None`` otherwise (i.e., if this
    hint originates from *no* such superclass).

    This getter is intentionally *not* memoized (e.g., by the
    :func:`callable_cached` decorator), as the implementation trivially reduces
    to an efficient series of simple tests.

    Parameters
    ----------
    hint : object
        Object to be inspected.

    Returns
    ----------
    (type, None)
        Either:

        * If this object is:

          * A non-:mod:`typing` class (e.g., :class:`str`), this object as is.
          * An argumentless :mod:`typing` object originating from a
            non-:mod:`typing` superclass (e.g., :attr:`typing.Dict`, associated
            with :class:`dict`), that superclass.

        * Else, ``None``.

    Raises
    ----------
    TypeError
        If this object is **unhashable** (i.e., *not* hashable by the builtin
        :func:`hash` function and thus unusable in hash-based containers like
        dictionaries and sets). All supported type hints are hashable.
    '''

    # Return either...
    return (
        # If this hint is a non-"typing" class, this class as is;
        hint if isinstance(hint, type) else
        TYPING_ATTR_TO_TYPE_GET(
            # Else if this hint is an argumentless "typing" attribute
            # originating from a non-"typing" superclass, that superclass;
            hint,
            # Else, "None".
            None
        )
    )