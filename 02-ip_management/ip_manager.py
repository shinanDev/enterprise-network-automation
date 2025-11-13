"""
IP Management System - Core Logic Module
Enterprise Network Automation Suite

Author: Philipp Prinzen
Project: IHK Fachinformatiker Abschlussprojekt
Date: 2025-11-13

This module handles all IP management operations:
- YAML device inventory parsing
- IP address calculations
- Free IP detection
- Device CRUD operations
"""

import yaml
import ipaddress
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IPManager:
    """Main IP Management class - handles all device and IP operations"""

    def __init__(self, config_path: str = "data/devices.yaml"):
        """
        Initialize IPManager with device inventory

        Args:
            config_path: Path to devices.yaml config file
        """
        self.config_path = Path(config_path)
        self.inventory = None
        self.load_inventory()

    def load_inventory(self) -> None:
        """Load device inventory from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.inventory = yaml.safe_load(f)
            logger.info(f"Loaded inventory from {self.config_path}")
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            raise

    def save_inventory(self) -> None:
        """Save current inventory back to YAML file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.inventory, f, default_flow_style=False, sort_keys=False)
            logger.info(f"Saved inventory to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save inventory: {e}")
            raise

    def get_all_sites(self) -> List[str]:
        """Get list of all site names"""
        return list(self.inventory['sites'].keys())

    def get_site_info(self, site_name: str) -> Dict:
        """
        Get complete information for a site

        Args:
            site_name: Name of the site (e.g., 'hq', 'branch')

        Returns:
            Dictionary with site information
        """
        if site_name not in self.inventory['sites']:
            raise ValueError(f"Site '{site_name}' not found")
        return self.inventory['sites'][site_name]

    def get_all_devices(self, site_name: Optional[str] = None) -> List[Dict]:
        """
        Get all devices, optionally filtered by site

        Args:
            site_name: Filter by site name (optional)

        Returns:
            List of device dictionaries
        """
        devices = []

        if site_name:
            # Get devices from specific site
            site = self.get_site_info(site_name)
            for device in site['devices']:
                device['site'] = site_name  # Add site info to device
                devices.append(device)
        else:
            # Get devices from all sites
            for site_key, site_data in self.inventory['sites'].items():
                for device in site_data['devices']:
                    device['site'] = site_key
                    devices.append(device)

        return devices

    def get_devices_by_vlan(self, vlan_id: int, site_name: Optional[str] = None) -> List[Dict]:
        """
        Get all devices in a specific VLAN

        Args:
            vlan_id: VLAN ID to filter by
            site_name: Optional site filter

        Returns:
            List of devices in the VLAN
        """
        all_devices = self.get_all_devices(site_name)
        return [d for d in all_devices if d.get('vlan') == vlan_id]

    def get_devices_by_type(self, device_type: str, site_name: Optional[str] = None) -> List[Dict]:
        """
        Get all devices of a specific type

        Args:
            device_type: Type of device (e.g., 'server', 'client', 'printer')
            site_name: Optional site filter

        Returns:
            List of devices of the specified type
        """
        all_devices = self.get_all_devices(site_name)
        return [d for d in all_devices if d.get('type') == device_type]

    def get_device_by_name(self, device_name: str, site_name: Optional[str] = None) -> Optional[Dict]:
        """
        Find a device by its name

        Args:
            device_name: Name of the device
            site_name: Optional site filter

        Returns:
            Device dictionary or None if not found
        """
        all_devices = self.get_all_devices(site_name)
        for device in all_devices:
            if device.get('name') == device_name:
                return device
        return None

    def get_vlan_info(self, vlan_id: int, site_name: str) -> Optional[Dict]:
        """
        Get VLAN information for a specific site

        Args:
            vlan_id: VLAN ID
            site_name: Site name

        Returns:
            VLAN dictionary or None if not found
        """
        site = self.get_site_info(site_name)
        for vlan in site['vlans']:
            if vlan['id'] == vlan_id:
                return vlan
        return None

    def calculate_free_ips(self, vlan_id: int, site_name: str) -> List[str]:
        """
        Calculate free IP addresses in a VLAN

        Args:
            vlan_id: VLAN ID
            site_name: Site name

        Returns:
            List of available IP addresses (as strings)
        """
        # Get VLAN info
        vlan_info = self.get_vlan_info(vlan_id, site_name)
        if not vlan_info:
            return []

        # Parse subnet
        network = ipaddress.ip_network(vlan_info['subnet'], strict=False)

        # Get all used IPs in this VLAN
        devices = self.get_devices_by_vlan(vlan_id, site_name)
        used_ips = set()

        for device in devices:
            ip = device.get('ip')
            if ip and ip != 'dhcp':
                used_ips.add(ipaddress.ip_address(ip))

        # Add gateway to used IPs
        if 'gateway' in vlan_info:
            used_ips.add(ipaddress.ip_address(vlan_info['gateway']))

        # Add DHCP pool to used IPs if it exists
        if 'dhcp_pool' in vlan_info:
            start_ip = ipaddress.ip_address(vlan_info['dhcp_pool']['start'])
            end_ip = ipaddress.ip_address(vlan_info['dhcp_pool']['end'])

            # Generate all IPs in DHCP range
            current = start_ip
            while current <= end_ip:
                used_ips.add(current)
                current = ipaddress.ip_address(int(current) + 1)

        # Calculate free IPs (exclude network and broadcast)
        free_ips = []
        for ip in network.hosts():
            if ip not in used_ips:
                free_ips.append(str(ip))

        return free_ips

    def get_network_statistics(self, site_name: Optional[str] = None) -> Dict:
        """
        Get statistics about the network

        Args:
            site_name: Optional site filter

        Returns:
            Dictionary with network statistics
        """
        devices = self.get_all_devices(site_name)

        # Count by type
        type_counts = {}
        for device in devices:
            device_type = device.get('type', 'unknown')
            type_counts[device_type] = type_counts.get(device_type, 0) + 1

        # Count by VLAN
        vlan_counts = {}
        for device in devices:
            vlan = device.get('vlan', 0)
            vlan_counts[vlan] = vlan_counts.get(vlan, 0) + 1

        # Count by status
        status_counts = {}
        for device in devices:
            status = device.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1

        stats = {
            'total_devices': len(devices),
            'by_type': type_counts,
            'by_vlan': vlan_counts,
            'by_status': status_counts
        }

        # Add DHCP device count
        dhcp_count = sum(1 for d in devices if d.get('ip') == 'dhcp')
        stats['dhcp_devices'] = dhcp_count
        stats['static_devices'] = len(devices) - dhcp_count

        return stats

    def add_device(self, site_name: str, device_data: Dict) -> bool:
        """
        Add a new device to the inventory

        Args:
            site_name: Site to add device to
            device_data: Dictionary with device information

        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate required fields
            required = ['name', 'type', 'vlan', 'ip', 'port', 'switch', 'status']
            for field in required:
                if field not in device_data:
                    raise ValueError(f"Missing required field: {field}")

            # Check if device name already exists
            if self.get_device_by_name(device_data['name'], site_name):
                raise ValueError(f"Device '{device_data['name']}' already exists")

            # Add device to site
            site = self.get_site_info(site_name)
            site['devices'].append(device_data)

            # Save inventory
            self.save_inventory()
            logger.info(f"Added device '{device_data['name']}' to site '{site_name}'")
            return True

        except Exception as e:
            logger.error(f"Failed to add device: {e}")
            return False

    def update_device(self, site_name: str, device_name: str, updates: Dict) -> bool:
        """
        Update an existing device

        Args:
            site_name: Site where device is located
            device_name: Name of device to update
            updates: Dictionary with fields to update

        Returns:
            True if successful, False otherwise
        """
        try:
            site = self.get_site_info(site_name)

            # Find device in site
            device_found = False
            for i, device in enumerate(site['devices']):
                if device['name'] == device_name:
                    # Update device fields
                    site['devices'][i].update(updates)
                    device_found = True
                    break

            if not device_found:
                raise ValueError(f"Device '{device_name}' not found in site '{site_name}'")

            # Save inventory
            self.save_inventory()
            logger.info(f"Updated device '{device_name}' in site '{site_name}'")
            return True

        except Exception as e:
            logger.error(f"Failed to update device: {e}")
            return False

    def delete_device(self, site_name: str, device_name: str) -> bool:
        """
        Delete a device from inventory

        Args:
            site_name: Site where device is located
            device_name: Name of device to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            site = self.get_site_info(site_name)

            # Find and remove device
            initial_count = len(site['devices'])
            site['devices'] = [d for d in site['devices'] if d['name'] != device_name]

            if len(site['devices']) == initial_count:
                raise ValueError(f"Device '{device_name}' not found in site '{site_name}'")

            # Save inventory
            self.save_inventory()
            logger.info(f"Deleted device '{device_name}' from site '{site_name}'")
            return True

        except Exception as e:
            logger.error(f"Failed to delete device: {e}")
            return False

    def export_to_csv(self, output_path: str, site_name: Optional[str] = None) -> bool:
        """
        Export device inventory to CSV

        Args:
            output_path: Path for CSV file
            site_name: Optional site filter

        Returns:
            True if successful, False otherwise
        """
        import csv

        try:
            devices = self.get_all_devices(site_name)

            if not devices:
                logger.warning("No devices to export")
                return False

            # Get all unique keys from devices
            fieldnames = set()
            for device in devices:
                fieldnames.update(device.keys())

            fieldnames = sorted(fieldnames)

            # Write CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(devices)

            logger.info(f"Exported {len(devices)} devices to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    # Initialize manager
    manager = IPManager("data/devices.yaml")

    # Test: Get all sites
    print("=== ALL SITES ===")
    sites = manager.get_all_sites()
    print(f"Sites: {sites}\n")

    # Test: Get all devices
    print("=== ALL DEVICES ===")
    all_devices = manager.get_all_devices()
    print(f"Total devices: {len(all_devices)}\n")

    # Test: Get HQ devices
    print("=== HQ DEVICES ===")
    hq_devices = manager.get_all_devices('hq')
    print(f"HQ devices: {len(hq_devices)}\n")

    # Test: Get devices in VLAN 20
    print("=== VLAN 20 DEVICES ===")
    vlan20 = manager.get_devices_by_vlan(20, 'hq')
    for device in vlan20:
        print(f"  {device['name']}: {device['ip']}")
    print()

    # Test: Calculate free IPs in VLAN 20
    print("=== FREE IPs IN HQ VLAN 20 ===")
    free_ips = manager.calculate_free_ips(20, 'hq')
    print(f"Free IPs: {len(free_ips)}")
    print(f"First 10: {free_ips[:10]}\n")

    # Test: Get statistics
    print("=== NETWORK STATISTICS ===")
    stats = manager.get_network_statistics('hq')
    print(f"Total: {stats['total_devices']}")
    print(f"By type: {stats['by_type']}")
    print(f"DHCP devices: {stats['dhcp_devices']}")
    print(f"Static devices: {stats['static_devices']}")