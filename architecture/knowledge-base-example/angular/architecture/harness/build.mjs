// Visual harness: ngc (AOT) compiles harness/main.ts with the library sources; esbuild bundles it and runs the
// Angular linker on @angular/* packages (they ship partially compiled). `node harness/build.mjs`
import * as esbuild from 'esbuild';
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire(import.meta.url);
const babel = require('@babel/core');
const { createEs2015LinkerPlugin } = require('@angular/compiler-cli/linker/babel');
const linker = {
  name: 'angular-linker',
  setup(build) {
    build.onLoad({ filter: /node_modules[\\/]@angular[\\/].*\.mjs$/ }, async args => {
      const src = fs.readFileSync(args.path, 'utf8');
      if (!src.includes('ɵɵngDeclare')) return { contents: src, loader: 'js' };
      const out = await babel.transformAsync(src, {
        filename: args.path, compact: false, babelrc: false, configFile: false,
        plugins: [createEs2015LinkerPlugin({ linkerJitMode: false, fileSystem: { readFile: p => fs.readFileSync(p, 'utf8'), resolve: (...s) => path.resolve(...s) },
          logger: { level: 1, debug() {}, info() {}, warn: console.warn, error: console.error } })],
      });
      return { contents: out.code, loader: 'js' };
    });
  },
};
await esbuild.build({ entryPoints: ['harness/out/harness/main.js'], bundle: true, format: 'esm', outfile: 'harness/app.js', target: 'es2022', logLevel: 'error', plugins: [linker] });
console.log('bundled');
