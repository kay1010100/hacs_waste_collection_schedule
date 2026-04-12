import logging
from datetime import datetime

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Mijn Afval Zaken"
DESCRIPTION = "Source for Mijn Afval Zaken waste management."
URL = "https://www.mijnafvalzaken.nl/"


def EXTRA_INFO():
    return [
        {
            "title": s["title"],
            "url": get_main_url(s["api_url"]),
            "default_params": {"service": extract_service_name(s["api_url"])},
        }
        for s in SERVICE_MAP
    ]


TEST_CASES = {
    "Uitgeest": {
        "postal_code": "1911LB",
        "house_number": "14",
    },
    "Castricum": {
        "postal_code": "1902HJ",
        "house_number": "35",
    },
}

_LOGGER = logging.getLogger(__name__)

SERVICE_MAP = [
    {
        "title": "mijnafvalzaken",
        "api_url": "https://www.mijnafvalzaken.nl",
        "icons": {
            "plastic-blik-drinkpak": "mdi:recycle",
            "gft": "mdi:leaf",
            "papier-en-karton": "mdi:archive",
            "restafval": "mdi:trash-can",
        },
    },
]


def extract_service_name(api_url):
    name = api_url.split(".")[-2]
    name = name.split("/")[-1]
    return name


def get_service_name_map():
    return {
        extract_service_name(s["api_url"]): (s["api_url"], s["icons"])
        for s in SERVICE_MAP
    }


def get_main_url(url):
    x = url.split(".")[-2:]
    x[0] = x[0].removeprefix("https://")
    return "https://" + ".".join(x)


class Source:
    def __init__(
        self, postal_code, house_number, house_letter="", suffix="", service="mijnafvalzaken"
    ):
        self.postal_code = postal_code
        self.house_number = house_number
        self.house_letter = house_letter
        self.suffix = suffix
        self._url, self._icons = get_service_name_map()[service]

    def fetch(self):
        # Retrieve bagid (unique waste management identifier)
        r = requests.get(
            f"{self._url}/adressen/{self.postal_code}:{self.house_number}")
        r.raise_for_status()
        data = r.json()

        # Something must be wrong, maybe the address isn't valid? No need to do the extra requests so just return here.
        if len(data) == 0:
            raise Exception("no data found for this address")

        bag_id = data[0]["bagid"]
        if len(data) > 1 and self.house_letter and self.suffix:
            _LOGGER.info(f"Checking {self.house_letter} {self.suffix}")
            for address in data:
                if (
                    address["huisletter"].lower() == self.house_letter.lower()
                    and address["toevoeging"] == self.suffix
                ):
                    bag_id = address["bagid"]
                    break

        # Retrieve the details about different waste management flows (for example, paper, plastic etc.)
        r = requests.get(f"{self._url}/rest/adressen/{bag_id}/afvalstromen")
        r.raise_for_status()
        waste_flows = r.json()

        # Retrieve the pickup calendar for waste.
        r = requests.get(
            f"{self._url}/rest/adressen/{bag_id}/kalender/{datetime.today().year}"
        )
        r.raise_for_status()
        data = r.json()

        entries = []

        for item in data:
            waste_details = [
                x for x in waste_flows if x["id"] == item["afvalstroom_id"]
            ]
            entries.append(
                Collection(
                    date=datetime.strptime(
                        item["ophaaldatum"], "%Y-%m-%d").date(),
                    t=waste_details[0]["title"],
                    icon=self._icons.get(waste_details[0]["icon"]),
                )
            )

        return entries
