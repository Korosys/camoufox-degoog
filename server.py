import asyncio
import json
from aiohttp import web
from camoufox.async_api import AsyncCamoufox

_browser = None
_camoufox = None

async def get_browser():
    global _browser, _camoufox
    if _browser:
        return _browser
    _camoufox = AsyncCamoufox(headless=True)
    _browser = await _camoufox.__aenter__()
    return _browser

async def handle_content(request):
    try:
        body = await request.json()
    except Exception:
        return web.Response(status=400, text='{"error":"invalid json"}', content_type="application/json")

    url = body.get("url")
    if not url:
        return web.Response(status=400, text='{"error":"url is required"}', content_type="application/json")

    goto_options = body.get("gotoOptions", {})
    cookies = body.get("cookies", [])

    browser = await get_browser()
    context = await browser.new_context()
    try:
        if cookies:
            await context.add_cookies(cookies)
        page = await context.new_page()
        await page.goto(
            url,
            wait_until=goto_options.get("waitUntil", "networkidle"),
            timeout=goto_options.get("timeout", 15000),
        )
        html = await page.content()
        return web.Response(text=html, content_type="text/html")
    finally:
        await context.close()

app = web.Application()
app.router.add_post("/content", handle_content)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=3000)