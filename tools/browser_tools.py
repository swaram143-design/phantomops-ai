import random
import asyncio

from playwright.async_api import (
    async_playwright
)

from playwright_stealth import (
    Stealth
)

from fake_useragent import (
    UserAgent
)


class BrowserTools:

    def __init__(self):

        self.user_agent = (
            UserAgent()
        )

        self.stealth = (
            Stealth()
        )

    async def create_browser_context(
        self,
        playwright
    ):

        browser = await (
            playwright.chromium.launch(
                headless=False,
                slow_mo=50
            )
        )

        context = await (
            browser.new_context(
                user_agent=(
                    self.user_agent.random
                ),

                viewport={
                    "width": 1366,
                    "height": 768
                },

                locale="en-US"
            )
        )

        return browser, context

    async def human_delay(self):

        await asyncio.sleep(
            random.uniform(
                2,
                5
            )
        )

    async def prepare_page(
        self,
        page
    ):

        await self.stealth.apply_stealth_async(
            page
        )

    async def extract_page_content(
        self,
        url
    ):

        async with (
            async_playwright()
        ) as playwright:

            browser, context = (
                await self.create_browser_context(
                    playwright
                )
            )

            page = await (
                context.new_page()
            )

            try:

                await self.prepare_page(
                    page
                )

                await page.goto(
                    url,
                    timeout=90000
                )

                await self.human_delay()

                await page.mouse.move(
                    random.randint(100, 500),
                    random.randint(100, 500)
                )

                await self.human_delay()

                await page.evaluate(
                    """
                    window.scrollBy(
                        0,
                        document.body.scrollHeight / 2
                    )
                    """
                )

                await self.human_delay()

                title = await (
                    page.title()
                )

                text = await (
                    page.locator(
                        "body"
                    ).inner_text()
                )

                await browser.close()

                return {

                    "success": True,

                    "url":
                        url,

                    "title":
                        title,

                    "content":
                        text[:15000]
                }

            except Exception as error:

                await browser.close()

                return {

                    "success": False,

                    "error":
                        str(error)
                }

    async def search_duckduckgo(
        self,
        query
    ):

        async with (
            async_playwright()
        ) as playwright:

            browser, context = (
                await self.create_browser_context(
                    playwright
                )
            )

            page = await (
                context.new_page()
            )

            try:

                await self.prepare_page(
                    page
                )

                search_url = (
                    "https://duckduckgo.com/"
                    f"?q={query}"
                )

                await page.goto(
                    search_url,
                    timeout=90000
                )

                await self.human_delay()

                await page.evaluate(
                    """
                    window.scrollBy(
                        0,
                        document.body.scrollHeight / 3
                    )
                    """
                )

                await self.human_delay()

                links = await (
                    page.locator(
                        "a[data-testid='result-title-a']"
                    ).all()
                )

                results = []

                for link in links[:10]:

                    try:

                        title = await (
                            link.inner_text()
                        )

                        url = await (
                            link.get_attribute(
                                "href"
                            )
                        )

                        if (
                            title
                            and url
                        ):

                            results.append(
                                {
                                    "title":
                                        title,

                                    "url":
                                        url
                                }
                            )

                    except:

                        pass

                await browser.close()

                return {

                    "success": True,

                    "results":
                        results
                }

            except Exception as error:

                await browser.close()

                return {

                    "success": False,

                    "error":
                        str(error),

                    "results":
                        []
                }

    async def extract_contact_info(
        self,
        url
    ):

        async with (
            async_playwright()
        ) as playwright:

            browser, context = (
                await self.create_browser_context(
                    playwright
                )
            )

            page = await (
                context.new_page()
            )

            try:

                await self.prepare_page(
                    page
                )

                await page.goto(
                    url,
                    timeout=90000
                )

                await self.human_delay()

                text = await (
                    page.locator(
                        "body"
                    ).inner_text()
                )

                words = text.split()

                emails = []

                for word in words:

                    if (
                        "@"
                        in word
                        and "."
                        in word
                    ):

                        cleaned = (
                            word.strip()
                            .replace(
                                ",",
                                ""
                            )
                            .replace(
                                ";",
                                ""
                            )
                            .replace(
                                "(",
                                ""
                            )
                            .replace(
                                ")",
                                ""
                            )
                        )

                        emails.append(
                            cleaned
                        )

                await browser.close()

                return {

                    "success": True,

                    "emails":
                        list(
                            set(emails)
                        )
                }

            except Exception as error:

                await browser.close()

                return {

                    "success": False,

                    "error":
                        str(error),

                    "emails":
                        []
                }

    async def extract_links(
        self,
        url
    ):

        async with (
            async_playwright()
        ) as playwright:

            browser, context = (
                await self.create_browser_context(
                    playwright
                )
            )

            page = await (
                context.new_page()
            )

            try:

                await self.prepare_page(
                    page
                )

                await page.goto(
                    url,
                    timeout=90000
                )

                await self.human_delay()

                links = await (
                    page.locator(
                        "a"
                    ).all()
                )

                extracted_links = []

                for link in links[:50]:

                    try:

                        href = await (
                            link.get_attribute(
                                "href"
                            )
                        )

                        text = await (
                            link.inner_text()
                        )

                        if href:

                            extracted_links.append(
                                {
                                    "text":
                                        text,

                                    "href":
                                        href
                                }
                            )

                    except:

                        pass

                await browser.close()

                return {

                    "success": True,

                    "links":
                        extracted_links
                }

            except Exception as error:

                await browser.close()

                return {

                    "success": False,

                    "error":
                        str(error),

                    "links":
                        []
                }


browser_tools = (
    BrowserTools()
)