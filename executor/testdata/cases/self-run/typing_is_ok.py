# { "Depends": "py-genlayer:test" }

# from __future__ import annotations

import typing
import types


class Foo[X]:
	a: X


def tst(x):
	print(f'=== {x.__name__}')
	print(type(x))
	print(x)
	if isinstance(x, types.GenericAlias):
		print(f'origin={x.__origin__}')
		print(f'args={x.__args__}')
	elif isinstance(x, typing._GenericAlias):  # type: ignore
		print(f'origin={x.__origin__}')
		print(f'args={x.__args__}')
	if not isinstance(x, types.GenericAlias):
		for k, v in typing.get_type_hints(x).items():
			if isinstance(v, typing.TypeVar):
				v = v.__name__
			print(f'\t{k}: {v}')


tst(Foo)

tst(list[str])


class Test:
	foo: Foo[str]


tst(Test)
exit(0)
