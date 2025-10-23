import asyncio
from typing import TYPE_CHECKING
import httpx

from bs4 import BeautifulSoup
from httpx import Timeout, ConnectError

if TYPE_CHECKING:
    from backend.config.config import Settings


class DataParser:
    def __init__(self, settings_model: "Settings"):
        self.settings_model = settings_model
        self.data = self.settings_model.default_post_data
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

    async def get_wdt_nonce(self, client: httpx.AsyncClient) -> str:
        html = await self.safe_get(client, self.settings_model.page_url)
        soup = BeautifulSoup(html, "html.parser")
        wdt_nonce = soup.find(
            "input",
            {"id": f"wdtNonceFrontendServerSide_{self.settings_model.table_id}"},
        )["value"]
        if not wdt_nonce:
            raise ValueError("Не вдалося знайти wdtNonce")
        return wdt_nonce

    async def post_json(
        self,
        client: httpx.AsyncClient,
    ) -> dict:
        resp = await client.post(
            self.settings_model.api_url,
            params=self.settings_model.request_params,
            data=self.data,
            headers=self.settings_model.default_headers,
        )
        resp.raise_for_status()
        return resp.json()

    async def fetch_data(self) -> list:
        async with httpx.AsyncClient(
            headers=self.settings_model.default_headers,
            timeout=self.timeout,
        ) as client:
            wdt_nonce = await self.get_wdt_nonce(client)
            self.data["wdtNonce"] = wdt_nonce

            first_response = await self.post_json(client)
            self.data["length"] = str(first_response["recordsTotal"])

            full_response = await self.post_json(client)
            return full_response["data"]
