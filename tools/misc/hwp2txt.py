import olefile, zlib, struct, sys
def recs(data):
    i=0
    while i+4<=len(data):
        h=struct.unpack('<I',data[i:i+4])[0]; i+=4
        tag=h&0x3ff; lvl=(h>>10)&0x3ff; size=h>>20
        if size==0xfff: size=struct.unpack('<I',data[i:i+4])[0]; i+=4
        yield tag,lvl,data[i:i+size]; i+=size
def para_text(b):
    out=[];i=0;n=len(b)//2
    while i<n:
        c=struct.unpack('<H',b[i*2:i*2+2])[0]
        if c in (1,2,3,11,12,14,15,16,17,18,21,22,23):
            out.append('\x00' if c==11 else ''); i+=8; continue
        if c in (4,5,6,7,8,19,20): i+=8; continue
        if c==9: out.append('\t')
        elif c in (10,13): out.append('\n')
        elif c==24 or c==30 or c==31: out.append(' ')
        elif c>=32: out.append(chr(c))
        i+=1
    return ''.join(out)
def decrypt(d):
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    h=struct.unpack('<I',d[:4])[0]; size=h>>20; assert (h&0x3ff)==28 and size==256, (h&0x3ff,size)
    blk=bytearray(d[4:260])
    seed=struct.unpack('<I',blk[:4])[0]
    st=seed
    def rnd():
        nonlocal st
        st=(st*214013+2531011)&0xffffffff
        return (st>>16)&0x7fff
    i=0;
    while i<256:
        a=rnd()&0xff; n=(rnd()&0xf)+1
        for _ in range(n):
            if i<256 and i>=4: blk[i]^=a
            i+=1
    off=(seed&0xf)+4
    key=bytes(blk[off:off+16])
    body=d[260:]; body=body[:len(body)//16*16]
    dec=Cipher(algorithms.AES(key),modes.ECB()).decryptor()
    return dec.update(body)+dec.finalize()
def main(fn):
    ole=olefile.OleFileIO(fn)
    hdr=ole.openstream('FileHeader').read(); comp=hdr[36]&1
    dist=bool(hdr[36]&4)
    top='ViewText' if dist else 'BodyText'
    secs=sorted([s for s in ole.listdir() if s[0]==top],key=lambda s:int(s[1][7:]))
    res=[]
    for s in secs:
        d=ole.openstream(s).read()
        if dist: d=decrypt(d)
        if comp: d=zlib.decompress(d,-15)
        paras=[]; stack={}
        for tag,lvl,b in recs(d):
            if tag==66:
                p={'t':'','ctrls':[],'lvl':lvl}; paras.append(p); stack[lvl]=p
            elif tag==67:
                p=stack.get(lvl-1)
                if p is not None: p['t']=para_text(b)
            elif tag==71:
                p=stack.get(lvl-1)
                cid=b[:4][::-1].decode('latin1')
                c={'id':cid,'eq':None,'lvl':lvl}
                if p is not None: p['ctrls'].append(c)
                stack[('c',lvl)]=c
            elif tag==88:
                c=stack.get(('c',lvl-1))
                if c is not None:
                    ln=struct.unpack('<H',b[4:6])[0]
                    c['eq']=b[6:6+ln*2].decode('utf-16le','replace').strip()
        for p in paras:
            t=p['t']; cs=[c for c in p['ctrls'] if c['id'] in ('tbl ','gso ','eqed','$pic','$rec','$lin')]
            out=[];k=0
            for ch in t:
                if ch=='\x00':
                    c=cs[k] if k<len(cs) else None; k+=1
                    if c and c['id']=='eqed': out.append('⟦'+(c['eq'] or '')+'⟧')
                    elif c and c['id']=='tbl ': out.append('[표]')
                    else: out.append('[그림]')
                else: out.append(ch)
            res.append(''.join(out))
    print('\n'.join(r.replace('\x00','[그림]') for r in res))
main(sys.argv[1])
