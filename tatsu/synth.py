from collections.abc import Mapping
from typing import Any

__REGISTRY: Mapping[str, Any] = vars()


class _Synthetic:
    def __reduce__(self):
        return (
            synthesize(type(self).__name__, type(self).__bases__),
            (),
            vars(self),
        )


def synthesize(name, bases):
    # Use plain name as registry key, fallback to type's name if needed
    typename = str(name)
    if not isinstance(bases, tuple):
        bases = (bases,)
    # Only add _Synthetic if not present
    if _Synthetic not in bases:
        bases += (_Synthetic,)
    constructor = __REGISTRY.get(typename)
    if not constructor:
        constructor = type(name, bases, {})
        typename = constructor.__name__  # update registry key if unique type name
        __REGISTRY[typename] = constructor
    return constructor
