#!/usr/bin/env python3
import ast,base64,hashlib,io,lzma,pathlib,tokenize
ROOT=pathlib.Path(__file__).resolve().parents[1]
def minify(source):
    tokens=list(tokenize.generate_tokens(io.StringIO(source).readline));docs=set()
    for node in ast.walk(ast.parse(source)):
        body=getattr(node,'body',None)
        if body and isinstance(body,list) and isinstance(body[0],ast.Expr):
            value=body[0].value
            if isinstance(value,ast.Constant) and isinstance(value.value,str):docs.add((value.lineno,value.col_offset,value.end_lineno,value.end_col_offset))
    out=[]
    for token in tokens:
        pos=token.start+token.end
        if token.type!=tokenize.COMMENT and pos not in docs:out.append(token)
    text=tokenize.untokenize(out)
    return '\n'.join(x.rstrip() for x in text.splitlines() if x.strip())+'\n'
def build(source):
    mini=minify(source)
    packed=lzma.compress(mini.encode(),format=lzma.FORMAT_ALONE,filters=[{'id':lzma.FILTER_LZMA1,'dict_size':1<<23,'lc':2,'lp':0,'pb':0,'mode':lzma.MODE_NORMAL,'nice_len':273,'mf':lzma.MF_BT4}])
    payload=base64.b64encode(packed).decode()
    output=f"import lzma,base64;exec(lzma.decompress(base64.b64decode('{payload}')))\n"
    return mini,payload,output
def main():
    mini,payload,output=build((ROOT/'engine.py').read_text(encoding='utf-8'))
    size=len(output.encode())
    if size>4096:raise SystemExit(f'packed file is {size} bytes (limit 4096); base64 {len(payload)}')
    (ROOT/'main.py').write_text(output,encoding='ascii',newline='\n')
    decoded=lzma.decompress(base64.b64decode(payload));assert decoded==mini.encode()
    sha=hashlib.sha256(mini.encode()).hexdigest()
    print(f'{size} bytes; base64 {len(payload)}; minified sha256={sha}; roundtrip sha256={hashlib.sha256(decoded).hexdigest()}')
if __name__=='__main__':main()
