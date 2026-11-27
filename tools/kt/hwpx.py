import olefile, zlib, sys, os
f=sys.argv[1]; out=sys.argv[2]; os.makedirs(out,exist_ok=True)
o=olefile.OleFileIO(f)
for e in o.listdir():
    p='/'.join(e)
    if p.startswith('BinData/'):
        d=o.openstream(e).read()
        try: d=zlib.decompress(d,-15)
        except Exception: pass
        open(os.path.join(out,e[-1]),'wb').write(d); print(e[-1],len(d))
