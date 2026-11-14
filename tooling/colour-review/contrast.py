import json
O=json.load(open('options.json'))
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    if a=='transparent' or b=='transparent': return None
    x,y=sorted([lum(a),lum(b)],reverse=True); return round((x+0.05)/(y+0.05),1)
PAIRS=[('on-primary','primary','t','Filled button label'),
('primary','surface','t','Primary text, links, Re-run label'),
('on-secondary-container','secondary-container','t','Tonal button, selected chip'),
('run-fg','run-bg','t','Run button label'),
('run-bg','surface','i','Run fill against the page'),
('nav-pill','nav-bg','i','Active nav pill against the frame'),
('focus','surface','n','Focus ring'),
('ai-mark','surface','n','AI dots and pen'),
('dots','surface','n','Running dots'),
('outline','surface','n','Field and chip border'),
('on-surface-variant','surface','t','Secondary text'),
('inverse-primary','inverse-surface','t','Snackbar action'),
('on-ai-container','ai-container','t','AI card text'),
('on-success-container','success-container','t','Healthy chip'),
('on-warning-container','warning-container','t','Degraded chip'),
('on-error-container','error-container','t','Failed chip')]
res=[]
for fg,bg,k,lab in PAIRS:
    row={'label':lab,'kind':k,'pair':f'{fg} / {bg}','v':{}}
    for o in 'ABCD':
        s=O[o]['slots']; row['v'][o]=[cr(s[fg][i],s[bg][i]) for i in (0,1)]
    res.append(row)
json.dump(res,open('contrast.json','w'),indent=1)
for r in res: print(r['label'].ljust(36), '  '.join(f"{o}:{r['v'][o][0]}/{r['v'][o][1]}" for o in 'ABCD'))
