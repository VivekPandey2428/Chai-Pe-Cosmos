// Converts the npm-installed Fredoka woff into a three.js typeface JSON (digits, comma, plus only).
import fs from 'node:fs';
import opentype from 'opentype.js';
const [src, out] = process.argv.slice(2);
const buf = fs.readFileSync(src);
const font = opentype.parse(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
const scale = 1000 / font.unitsPerEm;
const glyphs = {};
for (const ch of '0123456789,+. kmh/') {
  const g = font.charToGlyph(ch);
  const o = [];
  for (const c of g.path.commands) {
    const m = (v) => Math.round(v * scale);
    if (c.type === 'M') o.push('m', m(c.x), m(c.y));
    else if (c.type === 'L') o.push('l', m(c.x), m(c.y));
    else if (c.type === 'Q') o.push('q', m(c.x), m(c.y), m(c.x1), m(c.y1));
    else if (c.type === 'C') o.push('b', m(c.x), m(c.y), m(c.x1), m(c.y1), m(c.x2), m(c.y2));
  }
  glyphs[ch] = { ha: Math.round(g.advanceWidth * scale), x_min: 0, x_max: 0, o: o.join(' ') };
}
fs.writeFileSync(out, JSON.stringify({
  glyphs, familyName: 'Fredoka', ascender: Math.round(font.ascender * scale),
  descender: Math.round(font.descender * scale), underlinePosition: -100, underlineThickness: 50,
  boundingBox: { yMin: -300, xMin: 0, yMax: 1000, xMax: 1000 }, resolution: 1000,
  original_font_information: { format: 0, fontFamily: 'Fredoka' }, cssFontWeight: 'bold', cssFontStyle: 'normal',
}));
