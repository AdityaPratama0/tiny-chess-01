#!/usr/bin/env python3
import ast,hashlib,lzma,pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
src=(ROOT/'engine.py').read_bytes()
filters=[{'id':lzma.FILTER_LZMA1,'dict_size':1<<16,'lc':2,'lp':0,'pb':0,
          'mode':lzma.MODE_NORMAL,'nice_len':273,'mf':lzma.MF_BT4}]
packed=lzma.compress(src,format=lzma.FORMAT_ALONE,filters=filters)

# A triple-quoted Latin-1 literal can carry newlines and quotes directly. XOR
# chooses a byte alphabet with few NUL/CR/backslash escapes.
candidates=[]
for key in range(256):
    body=bytearray()
    for x in packed:
        x^=key
        if x==92:body+=b'\\\\'
        elif x in (0,13):body+=f'\\x{x:02x}'.encode()
        else:body.append(x)
    body=body.replace(b"'''",b"\\'\\'\\'")
    out=(b"#coding:l1\nimport lzma;exec(lzma.decompress(bytes(x^"+str(key).encode()+
         b" for x in '''"+body+b"'''.encode('l1'))))\n")
    try:compile(out.decode('latin1'),'main.py','exec')
    except SyntaxError:continue
    candidates.append(out)
out=min(candidates,key=len)
if len(out)>4096: raise SystemExit(f'packed file is {len(out)} bytes (limit 4096)')
(ROOT/'main.py').write_bytes(out)

# Parse exactly what main.py executes, rather than merely trusting `packed`.
tree=ast.parse(out.decode('latin1'))
arg=tree.body[1].value.args[0]
roundtrip=eval(compile(ast.Expression(arg),'roundtrip','eval'),{'lzma':lzma})
assert roundtrip==src
sha=hashlib.sha256(src).hexdigest()
print(f'{len(out)} bytes sha256 engine={sha} roundtrip={hashlib.sha256(roundtrip).hexdigest()}')
