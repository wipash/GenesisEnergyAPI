from genesisenergy_api.auth import AbstractAuth
from genesisenergy_api.exceptions import ApiException, AuthException
from genesisenergy_api.model import (
    BillingAccount,
    PowerShoutBalance,
    PowerShoutBooking,
    PowerShoutBookingSubmission,
)


class GenesisEnergyEndpoint:
    powershout_bookings = "/powershoutcurrency/bookings"
    powershout_balance = "/powershoutcurrency/balance"
    powershout_booking_add = "/powershoutcurrency/booking/add"
    accounts = "/billing/accounts"


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
        self.supply_point_id: str = ""
        self.loyalty_account_id: str = ""
        self.supply_agreement_id: str = ""

    async def get_selected_billing_account(self) -> BillingAccount:
        accounts = await self.auth.request("get", GenesisEnergyEndpoint.accounts)
        check_status(accounts.status)
        accounts = await accounts.json()
        selected_billing_account = accounts["selectedBillingAccount"]
        return BillingAccount.from_dict(selected_billing_account)

    async def set_account(self) -> None:
        accounts = await self.auth.request("get", GenesisEnergyEndpoint.accounts)
        check_status(accounts.status)
        accounts = await accounts.json()

        electricity_supply_point_id = next(
            (
                sp["id"]
                for agreement in accounts["selectedBillingAccount"]["supplyAgreements"]
                for sp in agreement["supplyPoints"]
                if sp["type"] == "electricity"
            ),
            None,
        )
        if electricity_supply_point_id is None:
            msg = "No electricity supply point found"
            raise ApiException(msg)
        self.supply_point_id = electricity_supply_point_id
        self.loyalty_account_id = accounts["selectedBillingAccount"]["accountId"]
        self.supply_agreement_id = accounts["selectedBillingAccount"]["id"]

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

    async def add_powershout_booking(
        self, start_date: str, duration: int
    ) -> PowerShoutBookingSubmission:
        data = {
            "startDate": start_date,
            "duration": duration,
            "ecoHours": [],
            "supplyPointId": self.supply_point_id,
            "loyaltyAccountId": self.loyalty_account_id,
            "supplyAgreementId": self.supply_agreement_id,
        }
        powershout_bookings = await self.auth.request(
            "post", GenesisEnergyEndpoint.powershout_booking_add, data=data
        )
        check_status(powershout_bookings.status)
        return PowerShoutBookingSubmission.from_dict(await powershout_bookings.json())
