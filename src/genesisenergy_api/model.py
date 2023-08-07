from dataclasses import dataclass


@dataclass
class PowerShoutBalance:
    balance: int

    @staticmethod
    def from_dict(obj: dict) -> "PowerShoutBalance":
        balance = int(obj.get("balance") or 0)
        return PowerShoutBalance(balance)


@dataclass
class PowerShoutBooking:
    booking_id: str
    icp: str
    address: str
    nickame: str | None
    start_time: str
    end_time: str
    day: str
    date: str
    duration: int
    is_in_progress: bool
    eco_friendly: bool

    @staticmethod
    def from_dict(obj: dict) -> "PowerShoutBooking":
        _booking_id = str(obj.get("id"))
        _icp = str(obj.get("icp"))
        _address = str(obj.get("address"))
        _nickame = str(obj.get("nickame"))
        _start_time = str(obj.get("startTime"))
        _end_time = str(obj.get("endTime"))
        _day = str(obj.get("day"))
        _date = str(obj.get("date"))
        _duration = int(obj.get("duration") or 0)
        _is_in_progress = bool(obj.get("isInProgress"))
        _eco_friendly = bool(obj.get("ecoFriendly"))
        return PowerShoutBooking(
            _booking_id,
            _icp,
            _address,
            _nickame,
            _start_time,
            _end_time,
            _day,
            _date,
            _duration,
            _is_in_progress,
            _eco_friendly,
        )


@dataclass
class PowerShoutBookings:
    bookings: list[PowerShoutBooking]

    @staticmethod
    def from_dict(obj: dict) -> "PowerShoutBookings":
        _bookings = [PowerShoutBooking.from_dict(x) for x in obj.get("bookings") or []]
        return PowerShoutBookings(_bookings)
