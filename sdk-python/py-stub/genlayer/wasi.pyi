import typing

def rollback(s: str) -> typing.NoReturn: ...

def contract_return(s: str) -> typing.NoReturn: ...

def run_nondet(eq_principle: str, calldata: bytes) -> str: ...

def call_contract(address: bytes, calldata: str) -> str: ...

def get_message_data() -> str: ...

def get_entrypoint() -> bytes: ...

def get_webpage(url: str) -> str: ...
def call_llm(prompt: str) -> str: ...
