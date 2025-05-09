from bitcoin.wallet import CBitcoinAddress
from bitcoin.core import CScript, x
from bitcoin.core.script import OP_CHECKSIG, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_EQUAL, OP_RETURN, OP_TRUE

def is_p2pkh(script):
    ops = list(script)
    return (
        len(ops) == 5 and
        ops[0] == OP_DUP and
        ops[1] == OP_HASH160 and
        isinstance(ops[2], bytes) and len(ops[2]) == 20 and
        ops[3] == OP_EQUALVERIFY and
        ops[4] == OP_CHECKSIG
    )

def is_p2sh(script):
    ops = list(script)
    return (
        len(ops) == 3 and
        ops[0] == OP_HASH160 and
        isinstance(ops[1], bytes) and len(ops[1]) == 20 and
        ops[2] == OP_EQUAL
    )

def is_op_return(script):
    try:
        ops = list(script)
        return (
            len(ops) >= 1 and
            ops[0] == OP_RETURN and
            all(isinstance(op, (bytes, int)) for op in ops[1:])
        )
    except Exception as e:
        print(f"Error parsing script: {e}")
        return False

def test_script(address_str):
    addr = CBitcoinAddress(address_str)
    script = addr.to_scriptPubKey()

    print("Script:", script)
    print("Hex:", script.hex())

    if is_p2pkh(script):
        print("This is a P2PKH script.")
    elif is_p2sh(script):
        print("This is a P2SH script.")
    else:
        print("This is not a P2PKH script.")

    print("---------------------------")

def test_op_return_script(address_str):
    script = CScript([OP_RETURN, address_str.encode()])

    print("Script:", script)
    print("Hex:", script.hex())

    if is_op_return(script):
        print("This is an OP_RETURN script.")
    else:
        print("This is not an OP_RETURN script.")
    
    print("---------------------------")

def test_nonstandard_script(address_str):
    script = CScript([OP_TRUE, address_str.encode()])
    
    print("Script:", script)
    print("Hex:", script.hex())

    if is_p2pkh(script):
        print("This is a P2PKH script.")
    elif is_p2sh(script):
        print("This is a P2SH script.")
    else:
        print("This is a non-standard script.")

    print("---------------------------")

test_script("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
test_script("3AdD7ZaJQw9m1maN39CeJ1zVyXQLn2MEHR")
test_op_return_script("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
test_nonstandard_script("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")