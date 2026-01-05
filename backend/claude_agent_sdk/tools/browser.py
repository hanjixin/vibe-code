from claude_agent_sdk import tool
from playwright.async_api import async_playwright
import base64

# Global browser instance management (simplified for demo)
class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    async def get_page(self):
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.page = await self.browser.new_page()
        return self.page

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

browser_manager = BrowserManager()

@tool("open_url", "Opens a URL in the headless browser", {"url": str})
async def open_url(args) -> dict:
    """Opens a URL in the headless browser."""
    url = args["url"]
    try:
        page = await browser_manager.get_page()
        await page.goto(url)
        title = await page.title()
        return {"content": [{"type": "text", "text": f"Navigated to {url}. Page Title: {title}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error navigating to {url}: {str(e)}"}]}

@tool("click_element", "Clicks an element on the current page", {"selector": str})
async def click_element(args) -> dict:
    """Clicks an element on the current page."""
    selector = args["selector"]
    try:
        page = await browser_manager.get_page()
        await page.click(selector)
        return {"content": [{"type": "text", "text": f"Clicked element matching '{selector}'."}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error clicking '{selector}': {str(e)}"}]}

@tool("fill_form", "Fills a form input", {"selector": str, "value": str})
async def fill_form(args) -> dict:
    """Fills a form input."""
    selector = args["selector"]
    value = args["value"]
    try:
        page = await browser_manager.get_page()
        await page.fill(selector, value)
        return {"content": [{"type": "text", "text": f"Filled '{selector}' with '{value}'."}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error filling '{selector}': {str(e)}"}]}

@tool("take_screenshot", "Takes a screenshot of the current page", {"filename": str})
async def take_screenshot(args) -> dict:
    """Takes a screenshot of the current page."""
    filename = args["filename"]
    try:
        page = await browser_manager.get_page()
        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)
        
        await page.screenshot(path=filename)
        return {"content": [{"type": "text", "text": f"Screenshot saved to {filename}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error taking screenshot: {str(e)}"}]}

@tool("get_page_content", "Gets the text content of the current page", {})
async def get_page_content(args) -> dict:
    """Gets the text content of the current page."""
    try:
        page = await browser_manager.get_page()
        content = await page.content()
        # Simple text extraction, in real app might use BeautifulSoup or similar
        return {"content": [{"type": "text", "text": content[:2000] + "... (truncated)"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error getting content: {str(e)}"}]}
