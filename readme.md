# Lab Setup Documentation

## Part 1: Install DEVASC VM

### Steps
1. Import OVA in VMware: File > Open > Select DEVASC VM OVA
2. Power On VM
3. Accept Packet Tracer EULA (arrow keys + I Agree)
4. Wait for Ubuntu desktop to load

### Verification
No login required - boots to desktop automatically

---

## Part 2: Install CSR1000v VM

### Steps
1. Import OVA: File > Open > Select CSR1000v_for_VMware.ova
2. Edit VM Settings > First CD/DVD Drive > Browse > Select csr1000v-universalk9.16.09.05.iso
3. Power On VM
4. Wait 5-10 minutes for boot (ignore "Press any key" messages)
5. Press Enter when messages stop

### Verification
```bash
CSR1kv# show ip interface brief
```
**IP Address:** 192.168.127.130

---

## Connectivity Test

From DEVASC VM Terminal:
```bash
ping 192.168.127.130
ssh cisco@192.168.127.130
```
**Password:** cisco123!

**Status:** ✅ Both VMs operational and communicating

## Part 3 

# Part 3: Python Network Automation with Netmiko

## 3a: Connecting to an IOS-XE Device

### Task Preparation and Implementation

**Installed Netmiko:**
```bash
pip3 install netmiko
```

**Created comprehensive script** `netmiko_complete.py` with all required features:
- Dictionary-based device connection
- Class-based implementation (`NetworkAutomation`)
- Functions for each task
- Conditional statements (if/else) throughout
- Menu-driven interface

**Key components implemented:**

1. **Show commands (single device):**
```python
def send_show_command(self, command):
    output = self.connection.send_command(command)
    return output
```

2. **Configuration commands:**
```python
def send_config_commands(self, commands):
    output = self.connection.send_config_set(commands)
    return output
```

3. **Save output to file:**
```python
def save_output(self, command, filename=None):
    output = self.send_show_command(command)
    with open(filename, 'w') as f:
        f.write(output)
```

4. **Backup configuration:**
```python
def backup_config(self):
    config = self.connection.send_command('show running-config')
    filename = f"{hostname}_backup_{timestamp}.cfg"
```

5. **Configure from external file:**
```python
def config_from_file(self, filepath):
    with open(filepath, 'r') as f:
        commands = f.read().splitlines()
    output = self.send_config_commands(commands)
```

6. **Configure multiple interfaces:**
```python
def configure_interfaces(self, interface_list):
    for interface in interface_list:
        commands = [f"interface {interface['name']}", ...]
        self.send_config_commands(commands)
```

7. **Multiple device operations:**
```python
def show_commands_multiple_devices(devices, command):
    for device in devices:
        # Connect and execute
```

### Task Troubleshooting

**Issue:** Connection timeout on first attempt
- **Solution:** CSR1000v needed to fully boot (wait 5-10 minutes)

**Issue:** SSH authentication failed
- **Solution:** Verified password is `cisco123!` (with exclamation mark)

**Issue:** IP address different than lab document
- **Solution:** Used `show ip interface brief` to confirm actual IP: `192.168.127.130`

### Task Verification

**Tested all menu options:**
```bash
python3 netmiko_complete.py
```

**Option 1 - Show command:**
```
Enter: show ip interface brief
Result: ✓ Interface list displayed
```

**Option 2 - Config commands:**
```
Commands: interface Loopback20, ip address 20.20.20.1 255.255.255.0
Result: ✓ Interface configured
```

**Option 4 - Backup:**
```
Result: ✓ Created CSR1kv_backup_TIMESTAMP.cfg
```

**Option 6 - Multiple interfaces:**
```
Result: ✓ Loopback10 and Loopback11 created
```

**Verified on CSR1000v:**
```bash
ssh cisco@192.168.127.130
show ip int brief | include Loop
```
Output confirmed all configured interfaces present.

---

## 3b: Network Diagnostics Collector

### Task Preparation and Implementation

**Created** `network_diagnostics.py` - a practical tool network engineers use daily for troubleshooting.

**Purpose:** Automatically collect comprehensive diagnostic information and save to timestamped file.

**Commands collected:**
- show version
- show running-config
- show ip interface brief
- show ip route
- show interfaces
- show ip arp
- show processes cpu
- show processes memory
- show logging

**Key features:**
- Single execution collects all diagnostics
- Timestamped output files
- Clean formatted output
- Progress indicator while running

**Use cases:**
- Pre/post change documentation
- Troubleshooting snapshots
- Daily health checks
- Sending diagnostics to colleagues/vendors

### Task Troubleshooting

**Issue:** Large output files
- **Solution:** This is expected - full diagnostics are comprehensive

**Issue:** `show logging` took longer than other commands
- **Solution:** Added slight delay, normal for log retrieval

### Task Verification

**Executed script:**
```bash
python3 network_diagnostics.py
```

**Output:**
```
Connecting to device...
Connected!

Running: show version
Running: show running-config
Running: show ip interface brief
...
✓ All diagnostics saved to: CSR1kv_diagnostics_20251217_143022.txt
✓ Total commands executed: 13
```


**Verified file contents:**
```bash
cat CSR1kv_diagnostics_20251217_143022.txt | head -20
```
Confirmed all command outputs present with proper formatting.

**File size:** ~50KB - comprehensive diagnostic snapshot ready for analysis.

---