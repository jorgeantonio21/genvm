import typing

def rollback(s: str) -> typing.NoReturn: ...

def contract_return(s: bytes) -> typing.NoReturn: ...

def run_nondet(eq_principle: str, calldata: bytes) -> bytes: ...

def call_contract(address: bytes, calldata: bytes) -> bytes: ...

def get_message_data() -> str: ...

def get_entrypoint() -> bytes: ...

def get_webpage(config: str, url: str) -> str: ...
def call_llm(config: str, prompt: str) -> str: ...
