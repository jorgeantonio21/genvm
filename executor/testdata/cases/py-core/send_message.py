# { "Depends": "py-genlayer:test" }
from genlayer import *


@gl.contract
class Contract:
	def __init__(self):
		gl.ContractAt(gl.Address(b'\x30' * 20)).emit(gas=100).foo(1, 2)
