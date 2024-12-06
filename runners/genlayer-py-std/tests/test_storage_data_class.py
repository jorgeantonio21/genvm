from genlayer.py.storage import DynArray
from genlayer.py.storage._internal.generate import storage
from dataclasses import dataclass


@dataclass
class A:
	x: str

	def __init__(self, x: str):
		self.x = x


@storage
@dataclass
class B:
	x: A
	y: A


def test_assignments_depth_1():
	b = B(A('x'), A('y'))

	assert b.y.x == 'y'
	assert b.x.x == 'x'
