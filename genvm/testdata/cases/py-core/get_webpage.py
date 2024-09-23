# { "depends": ["genvm-rustpython:test"] }
import genlayer.sdk as gsdk
import json

class NonDetInit(gsdk.Runner):
    def __init__(self, mode):
        self.mode = mode
    async def run(self):
        return await gsdk.get_webpage({"mode": self.mode}, "http://127.0.0.1:4242/hello.html")

@gsdk.public
async def main(mode: str):
    print(await gsdk.run_nondet({"mode": "refl"}, NonDetInit(mode)))
