#!/usr/bin/env python3
import base64,hashlib,lzma,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def minify(source):
    return '\n'.join(x.rstrip() for x in source.splitlines() if x.strip())+'\n'
def build(source):
    mini=minify(source)
    packed=lzma.compress(mini.encode(),preset=9|lzma.PRESET_EXTREME)
    payload=base64.b85encode(packed).decode()
    output=f"x=2\nimport lzma,base64;exec(lzma.decompress(base64.b85decode('{payload}')))\n"
    return mini,payload,output
def main():
    mini,payload,output=build((ROOT/'engine.py').read_text(encoding='utf-8'))
    size=len(output.encode())
    if size>4096:raise SystemExit(f'packed file is {size} bytes (limit 4096); base64 {len(payload)}')
    (ROOT/'main.py').write_text(output,encoding='ascii',newline='\n')
    output.encode('utf-8').decode('utf-8');decoded=lzma.decompress(base64.b85decode(payload));assert decoded==mini.encode()
    sha=hashlib.sha256(mini.encode()).hexdigest()
    packed=base64.b85decode(payload);print(f'{size} bytes; source chars {len(mini)}; lzma {len(packed)}; base85 {len(payload)}; minified sha256={sha}; roundtrip sha256={hashlib.sha256(decoded).hexdigest()}')
if __name__=='__main__':main()
