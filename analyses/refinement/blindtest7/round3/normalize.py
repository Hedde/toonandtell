import sys, re
TRANS = {'‘':"'",'’':"'",'‚':"'",'‛':"'",'“':'"','”':'"','„':'"','‟':'"',
         '–':'-','—':'-','‒':'-','−':'-','…':'...',
         ' ':' ',' ':' ',' ':' ',' ':' ',' ':' ',' ':' ',
         'ﬁ':'fi','ﬂ':'fl','ﬀ':'ff','ﬃ':'ffi','ﬄ':'ffl'}
def norm_chars(t):
    for k,v in TRANS.items(): t=t.replace(k,v)
    return t
TERM = re.compile(r"""([.!?]['"]?$)|(\.\.\.['"]?$)""")
def cap_first(t):
    m=re.search(r'[A-Za-z]',t)
    if m and t[m.start()].islower():
        i=m.start(); t=t[:i]+t[i].upper()+t[i+1:]
    return t
def reflow_real(text):
    text=norm_chars(text)
    lines=[ln.strip() for ln in text.split('\n')]
    lines=[ln for ln in lines if ln and not re.fullmatch(r'#+',ln)]
    maxlen=max(len(ln) for ln in lines)
    paras=[]; cur=''
    for i,ln in enumerate(lines):
        cur = ln if not cur else cur+' '+ln
        nxt = lines[i+1] if i+1<len(lines) else ''
        ends_term = bool(TERM.search(ln))
        not_full = len(ln) < maxlen-4
        qend = ln.endswith("'") or ln.endswith('"')
        nextq = nxt[:1] in ("'", '"')
        if ends_term and (not_full or qend or nextq):
            paras.append(cur); cur=''
    if cur: paras.append(cur)
    paras=[re.sub(r'[ \t]+',' ',p).strip() for p in paras]
    return cap_first('\n\n'.join(paras)+'\n')
def reflow_canonical(text):
    text=norm_chars(text)
    blocks=re.split(r'\n[ \t]*\n', text)
    paras=[]
    for b in blocks:
        joined=' '.join(ln.strip() for ln in b.split('\n') if ln.strip())
        if joined: paras.append(re.sub(r'[ \t]+',' ',joined).strip())
    return cap_first('\n\n'.join(paras)+'\n')
if __name__=='__main__':
    mode,src,dst=sys.argv[1],sys.argv[2],sys.argv[3]
    fn=reflow_real if mode=='real' else reflow_canonical
    open(dst,'w',encoding='utf-8').write(fn(open(src,encoding='utf-8').read()))
