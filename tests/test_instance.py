import asyncio
import sys
from typing import cast

import aiohttp
from aiohttp import ClientSession

from genesisenergy_api.api import GenesisEnergyApi
from genesisenergy_api.auth import AbstractAuth


class ApiAuthImpl(AbstractAuth):
    """Authentication implementation for google calendar api library."""

    def __init__(
        self,
        websession: aiohttp.ClientSession,
        token,
    ) -> None:
        """Init the Google Calendar client library auth implementation."""
        super().__init__(websession, None)
        self._token = token

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        """Authorization: Basic [client_id:client_secret]"""
        return cast(str, self._token)


async def test():
    async with ClientSession() as session:
        api = GenesisEnergyApi(ApiAuthImpl(session, ""))
        await api.set_account()
        await api.get_selected_billing_account()
        await api.get_powershout_balance()
        print("Success", file=sys.stdout)


async def main():
    print("start\n", file=sys.stdout)
    await test()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
