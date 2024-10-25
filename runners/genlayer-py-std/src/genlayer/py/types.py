import base64
import typing
import collections.abc


class Address:
	SIZE = 20
	_as_bytes: bytes

	def __init__(self, val: str | collections.abc.Buffer):
		if isinstance(val, str):
			if len(val) == 2 + Address.SIZE * 2 and val.startswith('0x'):
				val = bytes.fromhex(val[2:])
			elif len(val) > Address.SIZE:
				val = base64.b64decode(val)
		else:
			val = bytes(val)
		if not isinstance(val, bytes) or len(val) != Address.SIZE:
			raise Exception(f'invalid address {val}')
		self._as_bytes = val

	@property
	def as_bytes(self) -> bytes:
		return self._as_bytes

	@property
	def as_hex(self) -> str:
		return '0x' + self._as_bytes.hex()

	@property
	def as_b64(self) -> str:
		return str(base64.b64encode(self.as_bytes), encoding='ascii')

	@property
	def as_int(self) -> int:
		return int.from_bytes(self._as_bytes, 'little', signed=False)

	def __hash__(self):
		return hash(self._as_bytes)

	def __lt__(self, r):
		assert isinstance(r, Address)
		return self._as_bytes < r._as_bytes

	def __le__(self, r):
		assert isinstance(r, Address)
		return self._as_bytes <= r._as_bytes

	def __eq__(self, r):
		if not isinstance(r, Address):
			return False
		return self._as_bytes == r._as_bytes

	def __ge__(self, r):
		assert isinstance(r, Address)
		return self._as_bytes >= r._as_bytes

	def __gt__(self, r):
		assert isinstance(r, Address)
		return self._as_bytes > r._as_bytes

	def __repr__(self) -> str:
		return 'addr#' + ''.join(['{:02x}'.format(x) for x in self._as_bytes])


i8 = typing.NewType('i8', int)
i64 = typing.NewType('i64', int)
u32 = typing.NewType('u32', int)
u64 = typing.NewType('u64', int)
u256 = typing.NewType('u256', int)


class Rollback(Exception):
	def __init__(self, msg: str):
		self.msg = msg
		super()


class Lazy[T]:
	_eval: typing.Callable[[], T] | None
	_exc: Exception | None
	_res: T | None

	def __init__(self, _eval: typing.Callable[[], T]):
		self._eval = _eval
		self._exc = None
		self._res = None

	def get(self) -> T:
		if self._eval is not None:
			ev = self._eval
			self._eval = None
			try:
				self._res = ev()
			except Exception as e:
				self._exc = e
		if self._exc is not None:
			raise self._exc
		return self._res  # type: ignore
