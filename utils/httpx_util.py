from typing import Tuple
import httpx
from httpx import RequestError
from tenacity import retry, stop_after_attempt, wait_fixed


class FetchRequestError(RequestError):
    ...


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def request(method: str,
                  url: str,
                  cookies: dict = None,
                  headers: dict = None,
                  json_data: dict = None,
                  timeout: int = 30,
                  **kwargs) -> Tuple[int, dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method,
                url,
                cookies=cookies,
                headers=headers,
                json=json_data,
                timeout=timeout,
                **kwargs
            )
            return response.status_code, response.json()
        except Exception as e:
            raise FetchRequestError(f"{e}, {response.text} -> {response.status_code}")
    
        
@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def request_img(method: str,
                      url: str,
                      timeout: int = 30,
                      **kwargs) -> Tuple[str, int, bytes]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method,
                url,
                timeout=timeout,
                **kwargs
            )
            return url, response.status_code, response.content
        except Exception as e:
            raise FetchRequestError(f"{e}, {response.text} -> {response.status_code}")

