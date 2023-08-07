from genesisenergy_api.auth import AbstractAuth
from genesisenergy_api.exceptions import ApiException, AuthException
from genesisenergy_api.model import PowerShoutBalance, PowerShoutBooking


class GenesisEnergyEndpoint:
    powershout_bookings = "/powershoutcurrency/bookings"
    powershout_balance = "/powershoutcurrency/balance"


def check_status(status):
    if status == 401:  # noqa: PLR2004
        msg = f"Authorization failed: {status}"
        raise AuthException(msg)
    if status != 200:  # noqa: PLR2004
        msg = f"Error request failed: {status}"
        raise ApiException(msg)


class GenesisEnergyApi:
    """Genesis Energy API."""

    def __init__(self, auth: AbstractAuth) -> None:
        self.auth = auth

    async def get_powershout_balance(self) -> PowerShoutBalance:
        powershout_balance = await self.auth.request(
            "get", GenesisEnergyEndpoint.powershout_balance
        )
        check_status(powershout_balance.status)
        return PowerShoutBalance.from_dict(await powershout_balance.json())

    async def get_powershout_bookings(self) -> list[PowerShoutBooking]:
        powershout_bookings = await self.auth.request(
            "get", GenesisEnergyEndpoint.powershout_bookings
        )
        check_status(powershout_bookings.status)
        bookings = await powershout_bookings.json()
        return [
            PowerShoutBooking.from_dict(booking) for booking in bookings["bookings"]
        ]
