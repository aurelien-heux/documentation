import * as esbuild from 'esbuild';
await esbuild.build({
  entryPoints: ['/tmp/claude-0/-home-claude/d439c99e-fcff-51e8-8efa-adabcf0e8c5e/scratchpad/harness/main.ts'],
  bundle: true, format: 'esm', outfile: '/tmp/claude-0/-home-claude/d439c99e-fcff-51e8-8efa-adabcf0e8c5e/scratchpad/harness/app.js',
  absWorkingDir: '/home/claude/ea-example/angular/architecture', target: 'es2022', logLevel: 'error',
  inject: ['/tmp/claude-0/-home-claude/d439c99e-fcff-51e8-8efa-adabcf0e8c5e/scratchpad/harness/compiler.ts'],
  tsconfigRaw: { compilerOptions: { experimentalDecorators: true, useDefineForClassFields: false } },
});
console.log('bundled');
