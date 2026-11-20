// main.ts — the entrypoint for the gta6-meme-x-01 entry.
//
// The entry itself is a GTA 6 meme posted on X from a public account. This
// program does not make or judge the meme; it only carries the post's address
// to the grader. POST.json holds that address (the X status URL), and this
// script copies the file byte-for-byte from the bot directory into the
// output directory, where the gate reads it.
//
// Byte-for-byte matters: the file is moved as raw bytes on purpose. Parsing
// it as JSON and writing it back out could reformat whitespace or drop the
// trailing newline, which would change what the grader sees. Reading with no
// encoding returns a Buffer, and writing that Buffer back reproduces the
// exact same bytes, newline included.
//
// Run it locally (outside the grader's container) like this:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';

// Where the entry lives, and where the grader expects the copy. The env
// vars stand in for /bot and /output when run outside the grader container.
const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

function main(): void {
  const sourcePath = `${botDir}/POST.json`;
  const targetPath = `${outputDir}/POST.json`;

  try {
    mkdirSync(outputDir, { recursive: true });
    const bytes = readFileSync(sourcePath);
    writeFileSync(targetPath, bytes);
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    console.error(`Failed to deliver POST.json to ${outputDir}: ${reason}`);
    process.exitCode = 1;
  }
}

main();
