#!/usr/bin/env python3
"""
RESTCONF GitHub Deployment Script
Fetches configuration from GitHub and deploys to Cisco IOS-XE via RESTCONF
"""

import json
import requests
import logging
from datetime import datetime

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'deployment_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

# Configuration
GITHUB_RAW_URL = "https://raw.githubusercontent.com/IanTerrynPXL/Networks-Expert-Lab3/refs/heads/main/cisco-config.json"
DEVICE_IP = "192.168.127.130"
USERNAME = "cisco"
PASSWORD = "cisco123!"

# RESTCONF endpoints
BASE_URL = f"https://{DEVICE_IP}/restconf/data"
HOSTNAME_URL = f"{BASE_URL}/Cisco-IOS-XE-native:native/hostname"
INTERFACE_URL = f"{BASE_URL}/ietf-interfaces:interfaces"
OSPF_URL = f"{BASE_URL}/Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospf:ospf"

# Headers
HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

AUTH = (USERNAME, PASSWORD)


def fetch_config_from_github():
    """Fetch configuration from GitHub repository"""
    logging.info(f"Fetching configuration from GitHub: {GITHUB_RAW_URL}")
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        response.raise_for_status()
        config = response.json()
        logging.info("✓ Successfully fetched configuration from GitHub")
        return config
    except requests.exceptions.RequestException as e:
        logging.error(f"✗ Failed to fetch from GitHub: {e}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"✗ Invalid JSON in GitHub file: {e}")
        raise


def configure_hostname(hostname):
    """Configure device hostname via RESTCONF"""
    logging.info(f"Configuring hostname: {hostname}")

    payload = {
        "Cisco-IOS-XE-native:hostname": hostname
    }

    try:
        response = requests.put(
            HOSTNAME_URL,
            auth=AUTH,
            headers=HEADERS,
            data=json.dumps(payload),
            verify=False
        )

        if 200 <= response.status_code <= 299:
            logging.info(f"✓ Hostname configured successfully (Status: {response.status_code})")
            return True
        else:
            logging.error(f"✗ Failed to configure hostname (Status: {response.status_code})")
            logging.error(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        logging.error(f"✗ Error configuring hostname: {e}")
        return False


def configure_interface(interface_config):
    """Configure a single interface via RESTCONF"""
    interface_name = interface_config['name']
    logging.info(f"Configuring interface: {interface_name}")

    # Build YANG-compliant interface configuration
    payload = {
        "ietf-interfaces:interface": {
            "name": interface_name,
            "description": interface_config.get('description', ''),
            "type": interface_config['type'],
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": interface_config['ip'],
                        "netmask": interface_config['netmask']
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    url = f"{INTERFACE_URL}/interface={interface_name}"

    try:
        response = requests.put(
            url,
            auth=AUTH,
            headers=HEADERS,
            data=json.dumps(payload),
            verify=False
        )

        if 200 <= response.status_code <= 299:
            logging.info(f"✓ Interface {interface_name} configured (Status: {response.status_code})")
            return True
        else:
            logging.error(f"✗ Failed to configure {interface_name} (Status: {response.status_code})")
            logging.error(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        logging.error(f"✗ Error configuring interface {interface_name}: {e}")
        return False


def configure_ospf(ospf_config):
    """Configure OSPF via RESTCONF"""
    logging.info(f"Configuring OSPF process {ospf_config['process_id']}")

    networks = []
    for net in ospf_config['networks']:
        networks.append({
            "ip": net['ip'],
            "mask": net['wildcard'],  # YANG model calls it "mask"
            "area": int(net['area'])
        })

    payload = {
        "Cisco-IOS-XE-native:router": {
            "Cisco-IOS-XE-ospf:ospf": [
                {
                    "id": int(ospf_config['process_id']),
                    "router-id": ospf_config['router_id'],
                    "network": networks
                }
            ]
        }
    }

    url = f"{BASE_URL}/Cisco-IOS-XE-native:native/router"

    try:
        response = requests.patch(
            url,
            auth=AUTH,
            headers=HEADERS,
            data=json.dumps(payload),
            verify=False
        )

        if 200 <= response.status_code <= 299:
            logging.info(f"✓ OSPF configured successfully (Status: {response.status_code})")
            return True
        else:
            logging.error(f"✗ Failed to configure OSPF (Status: {response.status_code})")
            logging.error(f"Response: {response.text}")
            return False

    except Exception as e:
        logging.error(f"✗ Error configuring OSPF: {e}")
        return False


def verify_configuration():
    """Verify configuration was applied"""
    logging.info("Verifying configuration...")

    try:
        # Verify hostname
        response = requests.get(
            HOSTNAME_URL,
            auth=AUTH,
            headers=HEADERS,
            verify=False
        )

        if response.status_code == 200:
            hostname = response.json().get('Cisco-IOS-XE-native:hostname', 'Unknown')
            logging.info(f"✓ Current hostname: {hostname}")

        # Verify interfaces
        response = requests.get(
            INTERFACE_URL,
            auth=AUTH,
            headers=HEADERS,
            verify=False
        )

        if response.status_code == 200:
            interfaces = response.json().get('ietf-interfaces:interfaces', {}).get('interface', [])
            logging.info(f"✓ Total interfaces configured: {len(interfaces)}")
            for intf in interfaces:
                logging.info(f"  - {intf['name']}: {intf.get('description', 'No description')}")

        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"✗ Verification failed: {e}")
        return False


def main():
    """Main deployment function"""
    logging.info("=" * 60)
    logging.info("RESTCONF GitHub Deployment Started")
    logging.info("=" * 60)

    success_count = 0
    failure_count = 0

    try:
        # Step 1: Fetch configuration from GitHub
        config = fetch_config_from_github()

        # Step 2: Configure hostname
        if configure_hostname(config['hostname']):
            success_count += 1
        else:
            failure_count += 1

        # Step 3: Configure interfaces
        for interface in config['interfaces']:
            if configure_interface(interface):
                success_count += 1
            else:
                failure_count += 1

        # Step 4: Configure OSPF
        if configure_ospf(config['ospf']):
            success_count += 1
        else:
            failure_count += 1

        # Step 5: Verify configuration
        verify_configuration()

        # Summary
        logging.info("=" * 60)
        logging.info("Deployment Summary:")
        logging.info(f"  Successful operations: {success_count}")
        logging.info(f"  Failed operations: {failure_count}")

        if failure_count == 0:
            logging.info("✓ Deployment completed successfully!")
        else:
            logging.warning("⚠ Deployment completed with errors")

        logging.info("=" * 60)

    except Exception as e:
        logging.error(f"✗ Deployment failed: {e}")
        raise


if __name__ == "__main__":
    main()
