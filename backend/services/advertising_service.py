from typing import List

from backend.config import settings
from backend.services.base_parse_service import BaseService


class AdvertisingService(BaseService):
    model_settings = settings.advertising_api

    @staticmethod
    def get_domain_from_str(domain: List[str]) -> str:
        return domain[0].split()[0]


async def main():
    import socket

    serv = AdvertisingService()
    res = await serv.get_all_domains()
    for item in res:
        print(item)


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(main()))
