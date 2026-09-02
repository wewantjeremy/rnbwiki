import Playwright
import pytest
def test_every_artist_renders(page):
    page.goto("http://localhost:5173")

    buttons = page.locator("YOUR_ARTIST_BUTTON_SELECTOR")
    count = buttons.count()

    failures = []

    for i in range(count):
        button = buttons.nth(i)
        name = button.inner_text()

        try:
            button.click()
            page.wait_for_timeout(100)

            assert page.locator("YOUR_ARTIST_PAGE_SELECTOR").is_visible()

        except Exception as e:
            failures.append((name, str(e)))

    assert not failures, failures