// Screenshots of the showcase. Usage: node shots.mjs <baseUrl> <outDir>
const { chromium } = require('playwright');
(async () => {
const [base, out] = process.argv.slice(2);
const browser = await chromium.launch();
const cases = [
  { name: 'runs-1440-light', path: '/#/runs', w: 1440, h: 900 },
  { name: 'runs-1440-dark', path: '/#/runs', w: 1440, h: 900, dark: true },
  { name: 'components-1440-light', path: '/#/components', w: 1440, h: 900, full: true },
  { name: 'components-1440-dark', path: '/#/components', w: 1440, h: 900, full: true, dark: true },
  { name: 'runs-900-rail', path: '/#/runs', w: 900, h: 800 },
  { name: 'runs-390-phone', path: '/#/runs', w: 390, h: 844 },
];
const errors = [];
for (const c of cases) {
  const page = await browser.newPage({ viewport: { width: c.w, height: c.h } });
  page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') errors.push(`${c.name}: ${m.type()}: ${m.text()}`); });
  page.on('pageerror', (e) => errors.push(`${c.name}: pageerror: ${e.message}`));
  await page.goto(base + c.path, { waitUntil: 'networkidle' }).catch(() => page.goto(base + c.path));
  if (c.dark) await page.evaluate(() => { document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark'); });
  await page.waitForTimeout(1200);
  if (c.full) {
    // The page scrolls inside mat-sidenav-content: expand it so the full page is captured.
    await page.addStyleTag({ content: 'ait-app-shell{height:auto!important} .mat-drawer-container,.mat-drawer-content{height:auto!important;overflow:visible!important} .mat-mdc-tab-body-wrapper{overflow:hidden!important}' });
    await page.waitForTimeout(300);
  }
  await page.screenshot({ path: `${out}/${c.name}.png`, fullPage: !!c.full });
  await page.close();
}
// Interaction checks: snackbar and confirm dialog on the Runs page.
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto(base + '/#/runs', { waitUntil: 'networkidle' }).catch(() => {});
await page.waitForTimeout(800);
await page.getByRole('button', { name: 'Request Run' }).click();
await page.waitForTimeout(600);
await page.screenshot({ path: `${out}/snackbar.png` });
await page.getByRole('button', { name: 'Cancel' }).first().click();
await page.waitForTimeout(800);
await page.screenshot({ path: `${out}/confirm.png` });
await page.keyboard.press('Escape');
await page.waitForTimeout(400);
// Keyboard focus ring on the Run button.
await page.keyboard.press('Tab'); await page.keyboard.press('Tab');
await page.waitForTimeout(200);
await browser.close();
console.log(errors.length ? errors.join('\n') : 'no console errors');
})();
