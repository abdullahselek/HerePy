#!/usr/bin/env python
"""Base classes shared by HERE API clients."""

import httpx2


class HEREApi:
    """Base class from which all wrappers inherit."""

    def __init__(self, api_key: str = None, timeout: int = None):
        """
        Initialize the API client.

        Args:
          api_key (str):
            API key taken from HERE Developer Portal.
          timeout (int):
            Timeout limit for requests.

        """
        self.__set_credentials(api_key)
        if timeout:
            self._timeout = timeout
        else:
            self._timeout = 20
        self._async_client: httpx2.AsyncClient | None = None

    async def __aenter__(self):
        """Open a shared async HTTP client for use by async API methods."""
        if self._async_client is not None:
            raise RuntimeError("This API client is already open.")
        self._async_client = httpx2.AsyncClient(timeout=self._timeout)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Close the shared async HTTP client."""
        await self.aclose()

    async def aclose(self):
        """Close the shared async HTTP client."""
        if self._async_client is not None:
            client = self._async_client
            self._async_client = None
            await client.aclose()

    def _get_async_client(self) -> httpx2.AsyncClient:
        if self._async_client is None:
            raise RuntimeError("Use this API client with 'async with' before calling async methods.")
        return self._async_client

    def __set_credentials(self, api_key):
        """
        Setter for credentials.

        Args:
          api_key (str):
            API key taken from HERE Developer Portal.

        """
        self._api_key = api_key
