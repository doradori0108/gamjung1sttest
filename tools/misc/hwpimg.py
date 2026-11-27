import olefile,zlib,sys,os
f,pre=sys.argv[1],sys.argv[2]
o=olefile.OleFileIO(f)
for e in o.listdir():
    if e[0]=='BinData':
        d=o.openstream(e).read()
        try: d=zlib.decompress(d,-15)
        except Exception: pass
        open(pre+'_'+e[1],'wb').write(d); print(pre+'_'+e[1],len(d))
