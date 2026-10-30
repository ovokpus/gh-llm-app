"""Headless Playwright screenshots of the running app (docker compose up) -> docs/screenshots/.

    uv run --no-project --with playwright python scripts/screenshots.py <name-prefix>

The README shots were taken with no key ("no-key") and with an obviously fake key ("rejected-key"),
so they show the app's real messages and no model output."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / 'docs' / 'screenshots'
UI = 'http://localhost:7860'


def main(prefix: str):
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1366, 'height': 860}, device_scale_factor=2)
        pg.goto(UI, wait_until='networkidle'); pg.wait_for_timeout(2500)
        if prefix == 'no-key':
            pg.screenshot(path=OUT / 'welcome.png')
        box = pg.locator('textarea').first
        box.fill('Explain what a context window is in two sentences.')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(8000)
        pg.screenshot(path=OUT / f'chat-{prefix}.png')
        b.close()


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'no-key')
