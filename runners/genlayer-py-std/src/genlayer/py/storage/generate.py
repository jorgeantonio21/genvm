"""
Module that uses reflections that generates python-friendly views to GenVM storage format (mapping from slot addresses to linear memories)
"""

__all__ = ('storage',)

from genlayer.py.types import *

import typing

from .core import *
from .core import _FakeStorageMan

from .desc_base_types import (
	_AddrDesc,
	_IntDesc,
	_StrDesc,
	_BytesDesc,
	_u32_desc,
	_BoolDesc,
	_NoneDesc,
	_BigIntDesc,
)
from .desc_record import _RecordDesc, WithRecordStorageSlot
from .vec import DynArray, _DynArrayDesc, Array, _ArrayDesc


def storage[T: type](cls: T) -> T:
	_storage_build(cls, {})
	return cls


class Lit:
	pass


class LitPy(Lit):
	def __init__(self, alts: tuple):
		self.alts = alts

	def __repr__(self):
		return f'LitPy[{" | ".join(repr(a) for a in self.alts)}]'


class LitTuple(Lit):
	def __init__(self, args: tuple[Lit]):
		self.args = args

	def __repr__(self):
		return f'LitTuple[{" * ".join(repr(a) for a in self.args)}]'


class _Instantiation:
	origin: type
	args: tuple[TypeDesc | Lit, ...]

	def __init__(self, origin: type, args: tuple[TypeDesc | Lit, ...]):
		self.origin = origin
		self.args = args

	def __eq__(self, r):
		if not isinstance(r, _Instantiation):
			return False
		return self.origin == r.origin and self.args == r.args

	def __hash__(self):
		return hash(('_Instantiation', self.origin, self.args))

	def __repr__(self):
		return f"{self.origin.__name__}[{', '.join(map(repr, self.args))}]"


_none_desc = _NoneDesc()

_known_descs: dict[type | _Instantiation, TypeDesc] = {
	Address: _AddrDesc(),
	str: _StrDesc(),
	bytes: _BytesDesc(),
	bool: _BoolDesc(),
	type(None): _none_desc,
	None: _none_desc,  # type: ignore
	u8: _IntDesc(1, signed=False),
	u16: _IntDesc(2, signed=False),
	u24: _IntDesc(3, signed=False),
	u32: _IntDesc(4, signed=False),
	u40: _IntDesc(5, signed=False),
	u48: _IntDesc(6, signed=False),
	u56: _IntDesc(7, signed=False),
	u64: _IntDesc(8, signed=False),
	u72: _IntDesc(9, signed=False),
	u80: _IntDesc(10, signed=False),
	u88: _IntDesc(11, signed=False),
	u96: _IntDesc(12, signed=False),
	u104: _IntDesc(13, signed=False),
	u112: _IntDesc(14, signed=False),
	u120: _IntDesc(15, signed=False),
	u128: _IntDesc(16, signed=False),
	u136: _IntDesc(17, signed=False),
	u144: _IntDesc(18, signed=False),
	u152: _IntDesc(19, signed=False),
	u160: _IntDesc(20, signed=False),
	u168: _IntDesc(21, signed=False),
	u176: _IntDesc(22, signed=False),
	u184: _IntDesc(23, signed=False),
	u192: _IntDesc(24, signed=False),
	u200: _IntDesc(25, signed=False),
	u208: _IntDesc(26, signed=False),
	u216: _IntDesc(27, signed=False),
	u224: _IntDesc(28, signed=False),
	u232: _IntDesc(29, signed=False),
	u240: _IntDesc(30, signed=False),
	u248: _IntDesc(31, signed=False),
	u256: _IntDesc(32, signed=False),
	i8: _IntDesc(1),
	i16: _IntDesc(2),
	i24: _IntDesc(3),
	i32: _IntDesc(4),
	i40: _IntDesc(5),
	i48: _IntDesc(6),
	i56: _IntDesc(7),
	i64: _IntDesc(8),
	i72: _IntDesc(9),
	i80: _IntDesc(10),
	i88: _IntDesc(11),
	i96: _IntDesc(12),
	i104: _IntDesc(13),
	i112: _IntDesc(14),
	i120: _IntDesc(15),
	i128: _IntDesc(16),
	i136: _IntDesc(17),
	i144: _IntDesc(18),
	i152: _IntDesc(19),
	i160: _IntDesc(20),
	i168: _IntDesc(21),
	i176: _IntDesc(22),
	i184: _IntDesc(23),
	i192: _IntDesc(24),
	i200: _IntDesc(25),
	i208: _IntDesc(26),
	i216: _IntDesc(27),
	i224: _IntDesc(28),
	i232: _IntDesc(29),
	i240: _IntDesc(30),
	i248: _IntDesc(31),
	i256: _IntDesc(32),
	bigint: _BigIntDesc(),
}

try:
	import numpy as np
	import numpy.typing as npt
except:
	if not typing.TYPE_CHECKING:
		np = None
		npt = None

if np is not None:

	class _NumpyNDDesc(TypeDesc[np.ndarray]):
		def __init__(self, typ: TypeDesc, shape: tuple[int, ...]):
			assert isinstance(typ, _NumpyDesc)
			type = typ._type
			dims = 1
			self.shape = shape
			for i in shape:
				dims *= i
			TypeDesc.__init__(self, type.itemsize * dims, [type.itemsize * dims])
			self._type = type

		def get(self, slot: StorageSlot, off: int) -> np.ndarray:
			dat = slot.read(off, self.size)
			return np.frombuffer(dat, self._type).reshape(self.shape).copy()

		def set(self, slot: StorageSlot, off: int, val: np.ndarray):
			assert val.dtype == self._type
			mv = memoryview(val).cast('B')
			assert len(mv) == self.size, f'invalid len {len(mv)} vs expected {self.size}'
			slot.write(off, mv)

	class _NumpyDesc(TypeDesc):
		def __init__(self, typ: np.number):
			type = np.dtype(typ)
			TypeDesc.__init__(self, type.itemsize, [type.itemsize])
			self._type = type

		def get(self, slot: StorageSlot, off: int):
			dat = slot.read(off, self.size)
			return np.frombuffer(dat, self._type).reshape(()).copy()

		def set(self, slot: StorageSlot, off: int, val):
			slot.write(off, self._type.tobytes(val))  # type: ignore

	_all_np_types: list[type[np.number]] = [
		np.uint8,
		np.uint16,
		np.uint32,
		np.uint64,
		np.int8,
		np.int16,
		np.int32,
		np.int64,
		np.float32,
		np.float64,
	]
	_known_descs.update({k: _NumpyDesc(k) for k in _all_np_types})  # type: ignore


def _storage_build_handle_special(
	origin: typing.Any,
	cls: type | _Instantiation,
	generics_map: dict[str, TypeDesc | Lit],
) -> tuple[bool, type | _Instantiation | Lit | TypeDesc]:
	if np is not None and origin is np.dtype:
		args = typing.get_args(cls)
		assert len(args) == 1
		return True, _storage_build(args[0], generics_map)
	if origin is typing.Literal:
		return True, LitPy(typing.get_args(cls))
	if origin is tuple:
		args = tuple(_storage_build(c, generics_map) for c in typing.get_args(cls))
		if all(isinstance(a, Lit) for a in args):
			return True, LitTuple(args)  # type: ignore
	if origin is Array:
		args = typing.get_args(cls)
		assert len(args) == 2
		assert typing.get_origin(args[1]) is typing.Literal
		lit_args = typing.get_args(args[1])
		assert len(lit_args) == 1
		assert isinstance(lit_args[0], int)
		res = _Instantiation(origin, (_storage_build(args[0], generics_map), lit_args[0]))  # type: ignore
		return True, res
	return False, cls


def _storage_build(
	cls: type | _Instantiation,
	generics_map: dict[str, TypeDesc | Lit],
) -> TypeDesc | Lit:
	assert cls is not int, 'use `bigint` please'
	if isinstance(cls, typing.TypeVar):
		return generics_map[cls.__name__]

	origin = typing.get_origin(cls)
	special, new_cls_special = _storage_build_handle_special(origin, cls, generics_map)
	if special:
		if isinstance(new_cls_special, TypeDesc):
			return new_cls_special
		if isinstance(new_cls_special, Lit):
			return new_cls_special
		new_cls = new_cls_special
	elif origin is not None:
		args = [_storage_build(c, generics_map) for c in typing.get_args(cls)]
		new_cls = _Instantiation(origin, tuple(args))
	else:
		new_cls = cls

	old = _known_descs.get(new_cls, None)
	if old is not None:
		return old
	if isinstance(new_cls, _Instantiation):
		description = _storage_build_generic(new_cls, generics_map)
	else:
		description = _storage_build_struct(new_cls, generics_map)
	_known_descs[new_cls] = description
	return description


def _storage_build_generic(
	cls: _Instantiation, generics_map: dict[str, TypeDesc | Lit]
) -> TypeDesc:
	# here args are resolved but not instantiated
	generic_params = cls.origin.__type_params__

	assert cls.origin is not list, 'use DynArray'
	assert cls.origin is not dict, 'use TreeMap'

	if np is not None and cls.origin is np.ndarray:
		assert len(cls.args) == 2
		shape = cls.args[0]
		assert isinstance(shape, LitTuple)
		assert all(
			isinstance(a, LitPy) and len(a.alts) == 1 and isinstance(a.alts[0], int)
			for a in shape.args
		)
		typ = cls.args[1]
		assert isinstance(typ, TypeDesc)
		return _NumpyNDDesc(
			typ, tuple(a.alts[0] for a in typing.cast(tuple[LitPy], shape.args))
		)
	if len(generic_params) != len(cls.args):
		raise Exception(
			f'incorrect number of generic arguments for {cls.origin} parameters={generic_params}, args={cls.args}'
		)
	if cls.origin is DynArray:
		arg0 = cls.args[0]
		assert not isinstance(arg0, Lit)
		return _DynArrayDesc(arg0)
	elif cls.origin is Array:
		arg0 = cls.args[0]
		assert not isinstance(arg0, Lit)
		return _ArrayDesc(arg0, typing.cast(int, cls.args[1]))
	else:
		gen = {k.__name__: v for k, v in zip(generic_params, cls.args)}
		res = _storage_build_struct(cls.origin, gen)
		res.alias_to = cls
		return res


def _storage_build_struct(
	cls: type, generics_map: dict[str, TypeDesc | Lit]
) -> TypeDesc:
	if cls is DynArray:
		raise Exception('invalid builder')
	size: int = 0
	copy_actions: list[CopyAction] = []
	props: dict[str, tuple[TypeDesc, int]] = {}

	was_generic = False

	for prop_name, prop_value in typing.get_type_hints(cls).items():
		cur_offset: int = size
		prop_desc = _storage_build(prop_value, generics_map)
		assert isinstance(prop_desc, TypeDesc)
		props[prop_name] = (prop_desc, cur_offset)

		if isinstance(prop_value, typing.TypeVar):
			was_generic = True

		if not getattr(cls, '__storage_patched__', False):

			def getter(s: WithRecordStorageSlot, prop_name=prop_name):
				prop_desc, off = s.__type_desc__.props[prop_name]
				return prop_desc.get(s._storage_slot, s._off + off)

			def setter(s: WithRecordStorageSlot, v, prop_name=prop_name):
				prop_desc, off = s.__type_desc__.props[prop_name]
				prop_desc.set(s._storage_slot, s._off + off, v)

			setattr(cls, prop_name, property(getter, setter))

		size += prop_desc.size
		actions_append(copy_actions, prop_desc.copy_actions)

	def view_at(desc: _RecordDesc, slot: StorageSlot, off: int, cls=cls):
		slf: WithRecordStorageSlot = cls.__new__(cls)  # type: ignore
		slf._storage_slot = slot
		slf._off = off
		slf.__type_desc__ = desc
		return slf

	description = _RecordDesc(view_at, size, copy_actions, props)

	old_init = cls.__init__

	def new_init(self, *args, **kwargs):
		if not hasattr(self, '_storage_slot'):
			assert not was_generic
			self._storage_slot = _FakeStorageMan().get_store_slot(ROOT_STORAGE_ADDRESS)
			self._off = 0
			self.__type_desc__ = description
		old_init(self, *args, **kwargs)

	new_init.__storage_patched__ = True

	if not hasattr(cls, '__contract__') and not getattr(
		old_init, '__storage_patched__', False
	):
		cls.__init__ = new_init
	return description


@storage
class _DateTime:
	seconds: u64
	micros: u32
	has_tz: bool
	off_days: i32
	off_seconds: i32
	off_micros: i32


from functools import partial
import datetime, time

_dt_desc: TypeDesc[_DateTime] = _known_descs[_DateTime]


class _DateTimeDesc(TypeDesc[datetime.datetime]):
	def __init__(self):
		super().__init__(_dt_desc.size, _dt_desc.copy_actions)

	def get(self, slot: StorageSlot, off: int) -> datetime.datetime:
		dt = _dt_desc.get(slot, off)

		def make_date(dt_tuple: time.struct_time, tzinfo):
			return datetime.datetime(
				year=dt_tuple.tm_year,
				month=dt_tuple.tm_mon,
				day=dt_tuple.tm_mday,
				hour=dt_tuple.tm_hour,
				minute=dt_tuple.tm_min,
				second=dt_tuple.tm_sec,
				microsecond=dt.micros,
				tzinfo=tzinfo,
			)

		if dt.has_tz:
			tz = datetime.timezone(
				datetime.timedelta(
					days=dt.off_days, seconds=dt.off_seconds, microseconds=dt.off_micros
				)
			)
			dt_tuple = time.gmtime(dt.seconds)
			return make_date(dt_tuple, datetime.UTC).astimezone(tz)
		else:
			tz = None
			dt_tuple = time.localtime(dt.seconds)
			return make_date(dt_tuple, tzinfo=tz)

	def set(self, slot: StorageSlot, off: int, val: datetime.datetime) -> None:
		dt = _dt_desc.get(slot, off)
		tz = val.tzinfo
		dt.seconds = u64(int(val.timestamp()))
		dt.micros = u32(val.microsecond)
		if tz is None:
			dt.has_tz = False
		else:
			dt.has_tz = True
			tz_off = tz.utcoffset(None)
			assert tz_off is not None

			dt.off_days = i32(tz_off.days)
			dt.off_seconds = i32(tz_off.seconds)
			dt.off_micros = i32(tz_off.microseconds)


_known_descs[datetime.datetime] = _DateTimeDesc()
