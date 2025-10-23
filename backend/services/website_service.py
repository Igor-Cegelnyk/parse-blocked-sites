from typing import List

from backend.config import settings
from backend.services.base_parse_service import BaseService


class WebsiteService(BaseService):
    model_settings = settings.website_api

    @staticmethod
    def get_domain_from_str(domain: List[str]) -> str:
        return domain[1].split()[0]


# async def main():
#     import socket
#
#     ip_address = socket.gethostbyname("wazamba.hu")
#     return ip_address
#     # serv = WebsiteService()
#     # res = await serv.get_all_domains()
#     # async for item in res:
#     #     print(item)
#
#
# if __name__ == "__main__":
#     import asyncio
#
#     print(asyncio.run(main()))
