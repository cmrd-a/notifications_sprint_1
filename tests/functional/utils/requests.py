from dataclasses import dataclass

from aiohttp import ClientSession
from multidict import CIMultiDictProxy


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


async def http_request(http_session: ClientSession, method: str, url: str, **kwargs) -> HTTPResponse:
    async with http_session.request(method, url, **kwargs) as response:
        return HTTPResponse(
            body=await response.json(),
            headers=response.headers,
            status=response.status,
        )
