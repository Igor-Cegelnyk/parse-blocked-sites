import asyncio
from abc import ABC
from typing import TYPE_CHECKING, List, AsyncGenerator

import aiodns

from backend.parses.parse_ban_site import DataParser
from backend.schemas.domain import DomainCreate

if TYPE_CHECKING:
    from backend.config.config import Settings


class BaseService(ABC):
    model_settings: "Settings"

    def process_item(self, item: list) -> DomainCreate:
        pass

    async def fetch_domains(self) -> List[List[str]]:
        """Імітація асинхронного отримання списку доменів (зовнішній парсер)."""
        parser = DataParser(self.model_settings)
        domains = await parser.fetch_data()
        return domains

    @staticmethod
    def get_domain_from_str(domain: List[str]) -> str:
        pass

    async def resolve_domain(
        self,
        domain: List[str],
        resolver: aiodns.DNSResolver,
    ) -> DomainCreate:
        """Повертає перший знайдений IP або порожній рядок, якщо не знайдено"""
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
            block_list=self.model_settings.name,
        )

    async def generate_domains(
        self,
        domains: List[List[str]],
        concurrency: int = 100,
    ) -> AsyncGenerator[DomainCreate, None]:
        """Асинхронно повертає Domain об'єкти (стрімінгом)."""
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
        results = [item async for item in self.generate_domains(domains)]
        return results
