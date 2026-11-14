import {Hct, argbFromHex, hexFromArgb, TonalPalette} from '../lab3/node_modules/@material/material-color-utilities/index.js';
const pal=h=>{const c=Hct.fromInt(argbFromHex(h));return TonalPalette.fromHueAndChroma(c.hue,c.chroma)};
const tones=[0,10,20,25,30,35,40,50,60,70,80,85,90,95,98,99,100];
const out={};
for (const [n,h] of [['secondary','#DED7EB'],['tertiary','#DCEAB4']]) { const p=pal(h); out[n]=Object.fromEntries(tones.map(t=>[t,hexFromArgb(p.tone(t))])); }
console.log(JSON.stringify(out));
