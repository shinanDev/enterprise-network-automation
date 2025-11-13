# vlan_calculator.py - Version 2.0
# Autor: Philipp Prinzen
# Datum: November 2025
# Beschreibung: VLAN Calculator für OnPrem Network mit CSV-Export

import csv
from datetime import datetime

def calculate_vlan(vlan_id, site):
    """
    Berechnet Netzwerk-Parameter für ein VLAN

    Args:
        vlan_id (int): VLAN-ID (10, 20, 30, 40, 50)
        site (str): Standort ('HQ' oder 'Branch')

    Returns:
        dict: Netzwerk-Informationen
    """

    # VLAN-Namen definieren
    vlan_names = {
        10: "Hypervisor",
        20: "Server",
        30: "Backup",
        40: "Management",
        50: "Clients"
    }

    # Standort-Präfix
    site_prefix = "10" if site.upper() == "HQ" else "20"

    # Subnet-Berechnung
    subnet = f"10.{site_prefix}.{vlan_id}.0"
    subnet_mask = "255.255.255.0"
    cidr = f"{subnet}/24"

    # Gateway (immer .1)
    gateway = f"10.{site_prefix}.{vlan_id}.1"

    # IP-Range
    first_usable = f"10.{site_prefix}.{vlan_id}.2"
    last_usable = f"10.{site_prefix}.{vlan_id}.254"
    broadcast = f"10.{site_prefix}.{vlan_id}.255"

    # DHCP-Range (nur für VLAN 50)
    if vlan_id == 50:
        dhcp_start = f"10.{site_prefix}.{vlan_id}.50"
        dhcp_end = f"10.{site_prefix}.{vlan_id}.150"
    else:
        dhcp_start = "N/A"
        dhcp_end = "N/A"

    # Ergebnis als Dictionary
    result = {
        "vlan_id": vlan_id,
        "vlan_name": vlan_names.get(vlan_id, "Unknown"),
        "site": site.upper(),
        "subnet": subnet,
        "subnet_mask": subnet_mask,
        "cidr": cidr,
        "gateway": gateway,
        "first_usable": first_usable,
        "last_usable": last_usable,
        "broadcast": broadcast,
        "dhcp_start": dhcp_start,
        "dhcp_end": dhcp_end,
        "usable_ips": 254
    }

    return result


def print_vlan_info(info):
    """Formatierte Ausgabe der VLAN-Informationen"""

    import csv
    from datetime import datetime

    def export_to_csv(info, filename="vlan_calculations.csv"):
        """Exportiert VLAN-Info als CSV"""

        import os
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Header (nur beim ersten Mal)
            if not file_exists:
                writer.writerow([
                    "Timestamp", "VLAN-ID", "Name", "Site",
                    "Subnet", "Gateway", "DHCP-Start", "DHCP-End"
                ])

            # Daten
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                info['vlan_id'],
                info['vlan_name'],
                info['site'],
                info['cidr'],
                info['gateway'],
                info['dhcp_start'],
                info['dhcp_end']
            ])

        print(f"\n✅ Exportiert nach: {filename}")


def export_to_csv(info, filename="vlan_calculations.csv"):
    """
    Exportiert VLAN-Informationen in eine CSV-Datei

    Args:
        info (dict): VLAN-Informationen aus calculate_vlan()
        filename (str): Name der CSV-Datei (Standard: vlan_calculations.csv)
    """

    import os

    # Prüfen ob Datei bereits existiert (für Header)
    file_exists = os.path.isfile(filename)

    # Datei öffnen (append mode = anhängen, nicht überschreiben)
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Header nur beim ersten Mal schreiben
        if not file_exists:
            writer.writerow([
                "Timestamp",
                "VLAN-ID",
                "Name",
                "Site",
                "Subnet",
                "Subnet Mask",
                "Gateway",
                "First IP",
                "Last IP",
                "Broadcast",
                "Usable IPs",
                "DHCP-Start",
                "DHCP-End"
            ])

        # Daten-Zeile schreiben
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            info['vlan_id'],
            info['vlan_name'],
            info['site'],
            info['cidr'],
            info['subnet_mask'],
            info['gateway'],
            info['first_usable'],
            info['last_usable'],
            info['broadcast'],
            info['usable_ips'],
            info['dhcp_start'],
            info['dhcp_end']
        ])

    print(f"\n✅ Erfolgreich exportiert nach: {filename}")

def main():
    """Hauptprogramm"""

    print("=" * 50)
    print("VLAN Calculator - OnPrem Network")
    print("=" * 50)

    # User-Input
    while True:
        try:
            vlan_id = int(input("\nVLAN-ID (10/20/30/40/50): "))
            if vlan_id not in [10, 20, 30, 40, 50]:
                print("⚠️  Ungültige VLAN-ID! Bitte 10, 20, 30, 40 oder 50 eingeben.")
                continue
            break
        except ValueError:
            print("⚠️  Bitte eine Zahl eingeben!")

    while True:
        site = input("Standort (HQ/Branch): ").strip()
        if site.upper() in ["HQ", "BRANCH"]:
            break
        print("⚠️  Ungültiger Standort! Bitte 'HQ' oder 'Branch' eingeben.")

    # Berechnung
    result = calculate_vlan(vlan_id, site)

    # Ausgabe
    print_vlan_info(result)

    # Ausgabe
    print_vlan_info(result)

    # === NEU: CSV-Export anbieten ===
    export = input("\nAls CSV exportieren? (j/n): ").strip().lower()
    if export == 'j':
        export_to_csv(result)
    # === ENDE NEU ===

    # Nochmal?
    again = input("\nWeitere Berechnung? (j/n): ").strip().lower()

    # Nochmal?
    again = input("Weitere Berechnung? (j/n): ").strip().lower()
    if again == 'j':
        main()
    else:
        print("\n👋 In Hamburg sagt man Tschüss!")


if __name__ == "__main__":
    main()