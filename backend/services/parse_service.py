import asyncio
from typing import TYPE_CHECKING, List, AsyncGenerator, Union

import aiodns

from backend.parses.parse_ban_site import DataParser
from backend.schemas.domain import DomainCreate

if TYPE_CHECKING:
    from backend.config.config import Settings
    from datetime import datetime


class ParseService:

    def __init__(
        self,
        api_settings: "Settings",
        exist_date: Union["datetime", None],
    ) -> None:
        self.api_settings = api_settings
        self.exist_date = exist_date

    async def fetch_domains(self) -> List[List[str]]:
        parser = DataParser(self.api_settings, self.exist_date)
        domains = await parser.fetch_data()
        return domains

    def get_domain_from_str(self, domain: List[str]) -> str:
        if self.api_settings.name == "honlapok":
            return domain[1].split()[0]
        return domain[0].split()[0]

    async def resolve_domain(
        self,
        domain: List[str],
        resolver: aiodns.DNSResolver,
    ) -> DomainCreate:
        domain = self.get_domain_from_str(domain)
        ip_address = None
        try:
            answers = await resolver.query(domain, "A")
            if answers:
                ip_address = answers[0].host
            else:
                answers = await resolver.query(domain, "AAAA")
                if answers:
                    ip_address = answers[0].host
        except aiodns.error.DNSError as e:
            pass
        except Exception as e:
            pass
        return DomainCreate(
            domain_name=domain,
            ip_address=ip_address,
            block_list=self.api_settings.name,
        )

    async def generate_domains(
        self,
        domains: List[List[str]],
        concurrency: int = 100,
    ) -> AsyncGenerator[DomainCreate, None]:
        resolver = aiodns.DNSResolver(nameservers=["8.8.8.8", "1.1.1.1"], timeout=7)
        semaphore = asyncio.Semaphore(concurrency)

        async def worker(domain_row: List[str]) -> DomainCreate:
            async with semaphore:
                return await self.resolve_domain(domain_row, resolver)

        tasks = [asyncio.create_task(worker(d)) for d in domains]

        for task in asyncio.as_completed(tasks):
            domain = await task
            yield domain

    async def get_all_domains(self):
        domains = await self.fetch_domains()
        if domains:
            results = [item async for item in self.generate_domains(domains)]
            return results
        return []
