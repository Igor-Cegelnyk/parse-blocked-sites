import asyncio
from datetime import datetime
from typing import TYPE_CHECKING, Union
import httpx

from bs4 import BeautifulSoup
from httpx import Timeout, ConnectError

if TYPE_CHECKING:
    from backend.config.config import Settings


class DataParser:
    def __init__(
        self,
        api_settings: "Settings",
        exist_date: Union[datetime, None],
    ):
        self.api_settings = api_settings
        self.exist_date = exist_date
        self.data = self.api_settings.default_post_data
        self.timeout = Timeout(connect=60.0, read=60.0, write=30.0, pool=60.0)
        self.max_retries = 3  # кількість спроб при помилках з'єднання
        self.retry_delay = 5  # пауза між спробами

    async def safe_get(self, client: httpx.AsyncClient, url: str):
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                return resp.text
            except (ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                if attempt == self.max_retries:
                    raise
                await asyncio.sleep(self.retry_delay)

    @staticmethod
    def get_update_date(soup: BeautifulSoup):
        date_text = soup.find("em").find("span")
        return datetime.strptime(date_text.get_text(strip=True), "%Y.%m.%d. %H:%M")

    def get_wdt_nonce(self, soup: BeautifulSoup):
        wdt_nonce = soup.find(
            "input",
            {"id": f"wdtNonceFrontendServerSide_{self.api_settings.table_id}"},
        )["value"]
        if not wdt_nonce:
            raise ValueError("Не вдалося знайти wdtNonce")
        return wdt_nonce

    async def post_json(
        self,
        client: httpx.AsyncClient,
    ) -> dict:
        resp = await client.post(
            self.api_settings.api_url,
            params=self.api_settings.request_params,
            data=self.data,
            headers=self.api_settings.default_headers,
        )
        resp.raise_for_status()
        return resp.json()

    async def fetch_data(self) -> list:
        async with httpx.AsyncClient(
            headers=self.api_settings.default_headers,
            timeout=self.timeout,
        ) as client:
            html = await self.safe_get(client, self.api_settings.page_url)
            soup = BeautifulSoup(html, "html.parser")

            update_date = self.get_update_date(soup)
            if self.exist_date and update_date < self.exist_date:
                return []

            wdt_nonce = self.get_wdt_nonce(soup)
            self.data["wdtNonce"] = wdt_nonce

            first_response = await self.post_json(client)
            self.data["length"] = first_response["recordsTotal"]

            full_response = await self.post_json(client)
            return full_response["data"]
