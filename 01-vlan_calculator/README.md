# VLAN Calculator
**Version:** 2.0  
**Status:** ✅ Feature Complete

## 📋 Beschreibung

Automatisches Berechnungs-Tool für Netzwerk-Parameter von VLANs 
im OnPrem Enterprise-Netzwerk.

---

## 🎯 Funktionen

- ✅ Berechnung von Subnet, Gateway, IP-Range
- ✅ Unterstützung für 2 Standorte (HQ, Branch)
- ✅ 5 VLANs (10, 20, 30, 40, 50)
- ✅ DHCP-Range-Berechnung (für VLAN 50)
- ✅ CSV-Export der Ergebnisse
- ✅ Input-Validierung

---

## 🛠️ Technologien

- **Sprache:** Python 3.11+
- **Libraries:** csv, datetime (Standard-Bibliothek)
- **IDE:** PyCharm Professional

---

## 🚀 Installation
```bash
cd 01-vlan_calculator
pip install -r requirements.txt
```

---

## 💻 Verwendung
```bash
python vlan_calculator.py
```

**Beispiel-Interaktion:**
```
==================================================
VLAN Calculator - OnPrem Network
==================================================

VLAN-ID (10/20/30/40/50): 20
Standort (HQ/Branch): HQ

==================================================
VLAN 20 - Server (HQ)
==================================================
Subnet:        10.10.20.0/24
Subnet Mask:   255.255.255.0
Gateway:       10.10.20.1
IP-Range:      10.10.20.2 - 10.10.20.254
Broadcast:     10.10.20.255
Usable IPs:    254
==================================================
```

---

## 📊 VLAN-Übersicht

| VLAN | Name | HQ Subnet | Branch Subnet | Verwendung |
|------|------|-----------|---------------|------------|
| 10 | Hypervisor | 10.10.10.0/24 | - | Virtualisierung |
| 20 | Server | 10.10.20.0/24 | 10.20.20.0/24 | Infrastruktur |
| 30 | Backup | 10.10.30.0/24 | 10.20.30.0/24 | Backup-Systeme |
| 40 | Management | 10.10.40.0/24 | - | Admin-Zugriff |
| 50 | Clients | 10.10.50.0/24 | 10.20.50.0/24 | Arbeitsplätze |

---

## 📝 Beispiel-Output (CSV)
```csv
Timestamp,VLAN-ID,Name,Site,Subnet,Gateway,DHCP-Start,DHCP-End
2025-11-12 21:30:00,20,Server,HQ,10.10.20.0/24,10.10.20.1,N/A,N/A
2025-11-12 21:31:00,50,Clients,Branch,10.20.50.0/24,10.20.50.1,10.20.50.50,10.20.50.150
```

---

## 🧪 Testing
```bash
python -m pytest tests/
```

---

## 📚 Dokumentation

Detaillierte Dokumentation in:
- `docs/documentation.md`
- `../network-design/IHK-Dokumentation.pdf`

---

## 🔜 Geplante Features

- [ ] IP-Konflikt-Erkennung
- [ ] Freie IP-Vorschläge
- [ ] Integration mit Tool 2 (IP Management)
- [ ] GUI-Version

---

**Version:** 1.0  
**Status:** In Entwicklung  
**Autor:** Philipp Prinzen  
**Datum:** November 2025