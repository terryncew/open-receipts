#!/usr/bin/env python3
import json, sys, os, glob

def check(path):
    data = json.load(open(path,'r',encoding='utf-8'))
    s = json.dumps(data, separators=(',',':')).encode('utf-8')
    size = len(s)
    status = (data.get('attrs') or {}).get('status','').lower()
    ok = True
    errs = []
    if status == 'green':
        if 'telem' in data and 'dials' in (data['telem'] or {}):
            ok = False; errs.append('green receipt must not carry telem.dials')
        if size > 640:
            ok = False; errs.append(f'green size {size} > 640B')
    else:
        if size > 800:
            ok = False; errs.append(f'non-green size {size} > 800B')
        d = (((data.get('telem') or {}).get('dials')) or {})
        for k in ('dphi_dk_q8','d2phi_dt2_q8','fresh_ratio_q8'):
            if k not in d:
                ok = False; errs.append(f'missing dials.{k}')
    pol = data.get('policy') or {}
    if not pol.get('policy_id') or not pol.get('policy_hash'):
        ok = False; errs.append('policy_id/policy_hash required')
    return ok, size, errs

def main():
    paths = []
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            paths.extend(glob.glob(a))
    else:
        for root,_,files in os.walk('docs'):
            for f in files:
                if f.endswith('.json') and 'issuer.pub' not in f:
                    paths.append(os.path.join(root,f))
    bad = 0
    for p in sorted(paths):
        ok, size, errs = check(p)
        flag = 'OK' if ok else 'FAIL'
        print(f'[{flag}] {p} ({size} bytes)')
        for e in errs: print('  -', e)
        if not ok: bad += 1
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
