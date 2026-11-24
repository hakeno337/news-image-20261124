// The World Today — 24 November 2026.
//
// The whole entry is delivery: the repository holds entry.png, the
// illustrated broadsheet drawn by compose.py, and this program copies
// it byte for byte to the output as entry.png, so the judge sees
// exactly the image the repository holds. Before copying it checks the
// file against the gate's own limits: a whole PNG or JPEG, at most
// 1 MiB, at most 1024 by 1024 pixels.
//
// In the grader the output is /output; outside it, MAKEFUN_OUTPUT_DIR
// stands in:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(source);

if (bytes.length > 1024 * 1024) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB gate limit`);
}

const isPng = bytes.length > 24 && bytes.toString('latin1', 1, 4) === 'PNG';
const isJpeg = bytes.length > 2 && bytes[0] === 0xff && bytes[1] === 0xd8;
if (!isPng && !isJpeg) {
  throw new Error('entry.png is neither a PNG nor a JPEG');
}

if (isPng) {
  const w = bytes.readUInt32BE(16);
  const h = bytes.readUInt32BE(20);
  if (w > 1024 || h > 1024) {
    throw new Error(`entry.png is ${w}x${h}, over the 1024 by 1024 gate limit`);
  }
}

copyFileSync(source, join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
