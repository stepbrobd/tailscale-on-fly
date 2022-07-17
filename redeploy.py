#!/usr/bin/env python3


import subprocess
import json
import os
import requests

from dotenv import load_dotenv
load_dotenv()


# Environment variables.
API_KEY = os.getenv("API_KEY")
API_DOMAIN = os.getenv("API_DOMAIN")

# Endponts.
API_ENDPOINT = f"https://api.tailscale.com/api/v2"
API_DEVICE_ENDPOINT = f"{API_ENDPOINT}/device"
API_TAILNET_ENDPOINT = f"{API_ENDPOINT}/tailnet/{API_DOMAIN}"

# Fly.io Regions <https://fly.io/docs/reference/regions/#fly-io-regions>.
# Region ID: (Region Location, WireGuard Gateway)
FLY_IO_REGIONS = {
    "ams": ("Amsterdam, Netherlands", True),
    "cdg": ("Paris, France", True),
    "dfw": ("Dallas, TX, USA", True),
    "ewr": ("Secaucus, NJ, USA", False),
    "fra": ("Frankfurt, Germany", True),
    "gru": ("Sao Paulo, Brazil", False),
    "hkg": ("Hong Kong, China", True),
    "iad": ("Ashburn, VA, USA", False),
    "lax": ("Los Angeles, CA, USA", True),
    "lhr": ("London, United Kingdom", True),
    "maa": ("Chennai, India", True),
    "mad": ("Madrid, Spain", False),
    "mia": ("Miami, FL, USA", False),
    "nrt": ("Tokyo, Japan", True),
    "ord": ("Chicago, IL, USA", True),
    "scl": ("Santiago, Chile", True),
    "sea": ("Seattle, WA, USA", True),
    "sin": ("Singapore, Singapore", True),
    "sjc": ("Sunnyvale, CA, USA", True),
    "syd": ("Sydney, Australia", True),
    "yul": ("Montreal, Canada", False),
    "yyz": ("Toronto, Canada", True),
}


def check_flyctl_auth_status() -> bool:
    """
    :return: status.
    """
    stdout, stderr = subprocess.Popen(
        ["flyctl", "auth", "whoami"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()

    return "error" not in stdout.decode("utf-8").strip().lower() and "error" not in stderr.decode("utf-8").strip().lower()


def get_vpn_machines() -> dict:
    """
    :return: dict{"device-name": "device-id"}.
    """
    response = requests.get(f"{API_TAILNET_ENDPOINT}/devices",
                            auth=requests.auth.HTTPBasicAuth(API_KEY, "")).json()

    devices = {}

    for device in response["devices"]:
        if "com-stepbrobd-vpn" in device["name"] and device["name"][18:21] in FLY_IO_REGIONS:
            devices[device["name"]] = device["id"]

    return devices


def get_device_details(device_id: str) -> json:
    """
    :return: dict{}.
    """
    response = requests.get(f"{API_DEVICE_ENDPOINT}/{device_id}",
                            auth=requests.auth.HTTPBasicAuth(API_KEY, "")).json()

    return response


def delete_device(device_id: str) -> int:
    """
    :return: status.
    """
    return requests.delete(f"{API_DEVICE_ENDPOINT}/{device_id}",
                           auth=requests.auth.HTTPBasicAuth(API_KEY, "")).status_code


def main() -> int:
    """
    :return: status.
    """
    if not check_flyctl_auth_status():
        print("Either flyctl is not installed or it's not logged in.\n")
        return 1
    else:
        print("Your flyctl is ready to launch.\n")

    print("Checking existing VPN machines on Tailnet...\n")
    devices = get_vpn_machines()
    print(f"Found {len(devices)} VPN machines.\n")

    print("Deleting existing VPN machines...\n")
    for name, id in devices.items():
        print(f"\tDeleting {name} ({id}):")
        print(f"\t\t\"DELETE {API_DEVICE_ENDPOINT}/{id}\"")
        print(f"\t\tReturned: {delete_device(id)}.\n")

    if len(get_vpn_machines()) != 0:
        print(
            "Something went wrong, existing VPN machines were not deleted successfully.\n")
        return 1
    else:
        print("All existing VPN machines were deleted successfully.\n")

    print("Redeploying VPN machines...\n")
    with subprocess.Popen(["flyctl", "deploy", "-c", "fly.toml"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        for line in process.stdout:
            print(line.decode("utf-8"))

    print("Verifying deployment...\n")
    devices = get_vpn_machines()
    print(f"{len(devices)} VPN machines successfully redeployed.\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
