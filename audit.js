/**
 * QA Auditor — toma screenshots sección por sección de cada sitio
 * Uso: node audit.js sitiopro | node audit.js fern-private-care
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const client = process.argv[2] || 'sitiopro';
const htmlPath = path.resolve(`projects/${client}/output/index.html`);
const screenshotsDir = path.resolve(`projects/${client}/audit-screenshots`);

if (!fs.existsSync(htmlPath)) {
  console.error(`ERROR: ${htmlPath} not found`);
  process.exit(1);
}

fs.mkdirSync(screenshotsDir, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  const url = `file:///${htmlPath.replace(/\\/g, '/')}`;
  console.log(`Opening: ${url}`);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

  // Trigger scroll animations visible
  await page.evaluate(() => {
    document.querySelectorAll('.reveal, .reveal-element').forEach(el => {
      el.classList.add('visible');
    });
  });
  await page.waitForTimeout(500);

  // ── Full page screenshot
  await page.screenshot({
    path: `${screenshotsDir}/00-full-page.png`,
    fullPage: true
  });
  console.log('✓ 00-full-page.png');

  // ── Screenshot each section by ID
  const sections = [
    'main-header', 'hero', 'services',
    'trust', 'trust-metrics', 'metrics',           // trust band variants
    'benefits', 'how-it-works', 'comparison',
    'testimonials', 'pricing', 'faq',
    'cta-final', 'contact'
  ];

  for (const id of sections) {
    try {
      const el = await page.$(`#${id}`);
      if (el) {
        await el.scrollIntoViewIfNeeded();
        await page.waitForTimeout(300);
        await el.screenshot({ path: `${screenshotsDir}/${id}.png` });
        const box = await el.boundingBox();
        const textContent = await el.evaluate(e => e.innerText.slice(0, 200).replace(/\n+/g, ' | '));
        console.log(`✓ ${id}.png | ${Math.round(box.height)}px | "${textContent.slice(0, 100)}..."`);
      } else {
        console.log(`✗ #${id} — NOT FOUND in page`);
      }
    } catch (e) {
      console.log(`✗ #${id} — ERROR: ${e.message}`);
    }
  }

  // ── Mobile viewport
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.evaluate(() => {
    document.querySelectorAll('.reveal, .reveal-element').forEach(el => el.classList.add('visible'));
  });
  await page.waitForTimeout(500);
  await page.screenshot({
    path: `${screenshotsDir}/mobile-full.png`,
    fullPage: true
  });
  console.log('✓ mobile-full.png');

  await browser.close();
  console.log(`\nDone. Screenshots saved to: projects/${client}/audit-screenshots/`);
})();
