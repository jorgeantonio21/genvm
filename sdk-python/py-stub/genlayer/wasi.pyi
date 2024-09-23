import typing
import collections.abc

def rollback(s: str) -> typing.NoReturn: ...

def contract_return(s: bytes) -> typing.NoReturn: ...

# returns fd
def run_nondet(eq_principle: str, calldata: bytes) -> int: ...

# returns fd
def call_contract(address: bytes, calldata: bytes) -> int: ...

def get_message_data() -> str: ...

def get_entrypoint() -> bytes: ...

# returns fd
def get_webpage(config: str, url: str) -> int: ...

# returns fd
def call_llm(config: str, prompt: str) -> int: ...

def storage_read(slot: bytes, off: int, len: int) -> bytes: ...
def storage_write(slot: bytes, off: int, what: collections.abc.Buffer) -> bytes: ...
