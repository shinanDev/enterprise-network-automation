# Tool 2: IP Management System 🌐

**Enterprise Network Automation Suite - Part 2**

Author: Philipp Prinzen  
Date: 2025-11-13  
Project: IHK Fachinformatiker Abschlussprojekt

---

## 📋 Overview

IP Management System for network device inventory management:
- YAML-based device inventory (41 devices, 2 sites)
- Free IP address calculation
- Device filtering (VLAN, Type, Site)
- Network utilization statistics
- CSV export for documentation

**Status:** Core logic complete ✅ | Flask UI in progress 🔄

---

## 🗂️ Project Structure

```
tool2-ip-management/
├── data/
│   └── devices.yaml           # Device inventory (HQ + Branch)
├── static/                    # CSS/JS (coming soon)
├── templates/                 # HTML templates (coming soon)
├── tests/                     # pytest (coming soon)
├── ip_manager.py              # Core logic (DONE!)
├── app.py                     # Flask backend (coming next)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🚀 Installation (Windows)

### 1. Create Virtual Environment

```powershell
# In project directory:
python -m venv venv

# Activate:
venv\Scripts\activate

# You should now see "(venv)" in your terminal
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Test

```powershell
# Test core logic:
python ip_manager.py
```

**Expected Output:**
```
=== ALL SITES ===
Sites: ['hq', 'branch']

=== ALL DEVICES ===
Total devices: 40

=== HQ DEVICES ===
HQ devices: 21
...
```

---

## 📦 Dependencies

- **PyYAML 6.0.1** - YAML parsing
- **Flask 3.0.0** - Web framework
- **python-dotenv 1.0.0** - Environment variables

Later (for testing):
- pytest 7.4.3
- pytest-cov 4.1.0

---

## 🔧 Core Features (ip_manager.py)

### Class: `IPManager`

**Initialization:**
```python
from ip_manager import IPManager

# Load inventory
manager = IPManager("data/devices.yaml")
```

**Key Methods:**

```python
# Sites
sites = manager.get_all_sites()
# -> ['hq', 'branch']

# All devices
devices = manager.get_all_devices()
# -> List with 40 devices

# Devices by site
hq_devices = manager.get_all_devices('hq')
# -> 21 devices

# Devices by VLAN
vlan20 = manager.get_devices_by_vlan(20, 'hq')
# -> 12 servers in HQ VLAN 20

# Devices by type
servers = manager.get_devices_by_type('server', 'hq')
# -> 13 servers in HQ

# Find device
dc01 = manager.get_device_by_name('DC-01', 'hq')
# -> {'name': 'DC-01', 'ip': '10.10.20.200', ...}

# Calculate free IPs
free_ips = manager.calculate_free_ips(20, 'hq')
# -> ['10.10.20.2', '10.10.20.3', ...]  (241 IPs)

# Statistics
stats = manager.get_network_statistics('hq')
# -> {'total_devices': 21, 'by_type': {...}, ...}

# Add device
manager.add_device('hq', {
    'name': 'NEW-SRV-01',
    'type': 'server',
    'vlan': 20,
    'ip': '10.10.20.240',
    'port': 'Fa0/18',
    'switch': 'SW-01',
    'status': 'active'
})

# Update device
manager.update_device('hq', 'NEW-SRV-01', {
    'status': 'inactive',
    'description': 'Maintenance'
})

# Delete device
manager.delete_device('hq', 'NEW-SRV-01')

# CSV export
manager.export_to_csv('output.csv', 'hq')
```

---

## 📊 Network Overview

### HQ (10.10.x.x)
- **VLAN 10** - Hypervisors (2 devices)
- **VLAN 20** - VMs/Servers (13 devices)
- **VLAN 30** - Backup (1 device)
- **VLAN 40** - Management (1 device)
- **VLAN 50** - Clients (5 devices, DHCP)

**Total HQ:** 21 Devices (16 Static, 5 DHCP)

### Branch (10.20.x.x)
- **VLAN 20** - VMs (2 devices)
- **VLAN 30** - Backup (1 device)
- **VLAN 50** - Clients (16 devices, DHCP)

**Total Branch:** 19 Devices (3 Static, 16 DHCP)

**Network Total:** 40 Devices across 2 sites

---

## 🎯 Next Steps

### Phase 1: Flask Web UI (IN PROGRESS)
- [ ] Dashboard (overview, statistics)
- [ ] Device list (sortable, filterable)
- [ ] Add device form
- [ ] Free IP search
- [ ] Bootstrap UI

### Phase 2: Advanced Features (LATER)
- [ ] Ping status checks (requires admin rights)
- [ ] SQLite history log
- [ ] Excel export
- [ ] VLAN visualization (charts)

### Phase 3: Integration (IHK PROJECT)
- [ ] API for Tool 4 (AI Assistant)
- [ ] SNMP integration
- [ ] Config Generator integration (Tool 3)

---

## 🧪 Testing

```powershell
# Run all tests (when pytest is installed):
pytest tests/

# With coverage:
pytest --cov=. tests/
```



---

## 📝 Code Quality

- ✅ **PEP 8** compliant
- ✅ **Type Hints** (Python 3.10+)
- ✅ **Docstrings** for all functions
- ✅ **Logging** instead of print()
- ✅ **Error Handling** with try/except
- ✅ **Separation of Concerns** (YAML, Logic, UI separated)



---

## 🔐 Best Practices

1. **Always use Virtual Environment**
2. **Keep requirements.txt updated**
3. **Backup YAML before changes** (`devices.yaml.backup`)
4. **Git commits after each feature**
5. **Write tests** (TDD when possible)

---

## 🐛 Troubleshooting

### "No module named 'yaml'"
```powershell
# Virtual environment activated?
venv\Scripts\activate

# Install dependencies:
pip install -r requirements.txt
```

### "FileNotFoundError: devices.yaml"
```powershell
# Are you in the right directory?
cd tool2-ip-management

# Is devices.yaml present?
dir data\devices.yaml
```

### "Permission denied" during CSV export
```powershell
# File already open in Excel?
# Close Excel and try again
```

---

## 🎓 Credits

- **Architecture inspired by:** Ethical AI Post Agent (FemAI)
- **Mentor:** Alexandra Wudel (AI Person of the Year 2024)
- **Principles:** Clean Code, Ethical AI, Human-in-the-Loop

---

## 📫 Support

Questions? Issues?

- **GitHub Issues:** [Create an issue](https://github.com/rhineday/enterprise-network-automation/issues)
- **LinkedIn:** [Philipp Prinzen](https://www.linkedin.com/in/philipp-prinzen-4a95b1b0)

---

**Built with ❤️ in Hamburg**  
 


---

*Last updated: 2025-11-13*