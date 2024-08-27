# { "lang": "python" }
import genlayer.sdk as gsdk

@gsdk.public
def pub():
    eval("print('init from pub!')")

@gsdk.public
def rback():
    gsdk.rollback("nah, I won't execute")

def priv():
    eval("print('init from priv!')")

@gsdk.public
def retn():
    return {"x": 10}

@gsdk.public
def retn_ser():
    return gsdk.AlreadySerializedResult("123")

gsdk.run(__import__(__name__))
