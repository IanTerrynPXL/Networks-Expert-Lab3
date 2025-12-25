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

**Status:** Both VMs operational and communicating

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
Result: Interface list displayed
```

**Option 2 - Config commands:**
```
Commands: interface Loopback20, ip address 20.20.20.1 255.255.255.0
Result: Interface configured
```

**Option 4 - Backup:**
```
Result: Created CSR1kv_backup_TIMESTAMP.cfg
```

**Option 6 - Multiple interfaces:**
```
Result: Loopback10 and Loopback11 created
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

## part 4

### 1
I already had the vm so that was easy

### 2
I just copy pasted in the raw file with the correct name. 

### 3
Then doing the following tree command gives back this
```
devasc@labvm:~/devnet$  pyang -f tree ietf-interfaces.yang  
ietf-interfaces.yang:6: error: module "ietf-yang-types" not found in search path
module: ietf-interfaces
  +--rw interfaces
  |  +--rw interface* [name]
  |     +--rw name                        string
  |     +--rw description?                string
  |     +--rw type                        identityref
  |     +--rw enabled?                    boolean
  |     +--rw link-up-down-trap-enable?   enumeration {if-mib}?
  +--ro interfaces-state
     +--ro interface* [name]
        +--ro name               string
        +--ro type               identityref
        +--ro admin-status       enumeration {if-mib}?
        +--ro oper-status        enumeration
        +--ro last-change?       yang:date-and-time
        +--ro if-index           int32 {if-mib}?
        +--ro phys-address?      yang:phys-address
        +--ro higher-layer-if*   interface-state-ref
        +--ro lower-layer-if*    interface-state-ref
        +--ro speed?             yang:gauge64
        +--ro statistics
           +--ro discontinuity-time    yang:date-and-time
           +--ro in-octets?            yang:counter64
           +--ro in-unicast-pkts?      yang:counter64
           +--ro in-broadcast-pkts?    yang:counter64
           +--ro in-multicast-pkts?    yang:counter64
           +--ro in-discards?          yang:counter32
           +--ro in-errors?            yang:counter32
           +--ro in-unknown-protos?    yang:counter32
           +--ro out-octets?           yang:counter64
           +--ro out-unicast-pkts?     yang:counter64
           +--ro out-broadcast-pkts?   yang:counter64
           +--ro out-multicast-pkts?   yang:counter64
           +--ro out-discards?         yang:counter32
           +--ro out-errors?           yang:counter32
devasc@labvm:~/devnet$ 

```
## part 5

### 4: SSH Access Troubleshooting

**Issue:** Unable to SSH to CSR1000v router

**Initial attempt:**
```bash
ping 192.168.0.130
```
**Result:** 100% packet loss - wrong IP address

**Corrected IP:**
```bash
ping 192.168.127.130
```
**Result:** ✓ Connectivity confirmed (2/3 packets received)

**SSH attempt:**
```bash
ssh cisco@192.168.127.130
```

**Error:**
```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Host key verification failed.
```

**Root cause:** Old SSH host key stored in `~/.ssh/known_hosts` from previous VM installation

**Solution:**
```bash
ssh-keygen -f "/home/devasc/.ssh/known_hosts" -R "192.168.127.130"
```

**Retry SSH:**
```bash
ssh cisco@192.168.127.130
```

**Status:** SSH access successful with password `cisco123!`

### 5: NETCONF Session Operations

**Started NETCONF session:**
```bash
ssh cisco@192.168.127.130 -p 830 -s netconf
```
**Password:** `cisco123!`

**Result:** Router sent hello message with 400+ lines of capabilities, ending with `]]>]]>`

**Sent client hello message:**
```xml
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<capabilities>
<capability>urn:ietf:params:netconf:base:1.0</capability>
</capabilities>
</hello>
]]>]]>
```

**Verified session on CSR1kv:**
```bash
CSR1kv# show netconf-yang sessions
```
**Result:** Session 24 active

**Sent RPC to get interface information:**
```xml
<rpc message-id="103" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<get>
<filter>
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
</get>
</rpc>
]]>]]>
```

**Received response (prettified):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="103">
  <data>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name>GigabitEthernet1</name>
        <description>VBox</description>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
        <enabled>true</enabled>
        <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"></ipv4>
        <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"></ipv6>
      </interface>
    </interfaces>
  </data>
</rpc-reply>
```

**Closed NETCONF session:**
```xml
<rpc message-id="9999999" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<close-session />
</rpc>
]]>]]>
```

**Verified session closed:**
```bash
CSR1kv# show netconf-yang sessions
```
**Result:** "There are no active sessions"

### 6: Python NETCONF with ncclient

**Created netconf directory:**
```bash
mkdir netconf
cd netconf
```

**Created script:** `ncclient-netconf.py`
```python
from ncclient import manager

m = manager.connect(
    host="192.168.127.130",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)
```

**Ran script:**
```bash
python3 ncclient-netconf.py
```
**Result:** No errors, connection successful

**Verified on CSR1kv:**
```
*Dec 25 15:53:48.860: %DMI-5-AUTH_PASSED: M0/0: dmiauthd: User 'cisco' authenticated successfully from 192.168.127.1:51512 and was authorized for netconf over ssh. External groups: PRIV15
```

**Status:** NETCONF session established via ncclient


### 7: Display NETCONF Capabilities

**Updated script:** `ncclient-netconf.py`
```python
from ncclient import manager

m = manager.connect(
    host="192.168.127.130",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

print("#Supported Capabilities (YANG models):")
for capability in m.server_capabilities:
    print(capability)
```

**Ran script:**
```bash
python3 ncclient-netconf.py
```

**Output (partial):**
```
#Supported Capabilities (YANG models):
urn:ietf:params:netconf:base:1.0
urn:ietf:params:netconf:base:1.1
urn:ietf:params:netconf:capability:writable-running:1.0
urn:ietf:params:netconf:capability:xpath:1.0
urn:ietf:params:xml:ns:yang:smiv2:SNMP-TARGET-MIB?module=SNMP-TARGET-MIB&revision=1998-08-04
urn:ietf:params:xml:ns:yang:smiv2:SNMPv2-MIB?module=SNMPv2-MIB&revision=2002-10-16
urn:ietf:params:xml:ns:yang:smiv2:TCP-MIB?module=TCP-MIB&revision=2005-02-18
urn:ietf:params:xml:ns:yang:smiv2:TUNNEL-MIB?module=TUNNEL-MIB&revision=2005-05-16
urn:ietf:params:xml:ns:yang:smiv2:UDP-MIB?module=UDP-MIB&revision=2005-05-20
urn:ietf:params:xml:ns:yang:smiv2:VPN-TC-STD-MIB?module=VPN-TC-STD-MIB&revision=2005-11-15
urn:ietf:params:xml:ns:netconf:base:1.0?module=ietf-netconf&revision=2011-06-01
urn:ietf:params:xml:ns:yang:ietf-netconf-with-defaults?module=ietf-netconf-with-defaults&revision=2011-06-01
urn:ietf:params:netconf:capability:notification:1.1
```

**Note:** Output shows same capabilities as manual NETCONF hello exchange, but formatted as clean list without XML tags.

### 8: Retrieve Running Configuration with ncclient

**Updated script:** `ncclient-netconf.py`
```python
from ncclient import manager

m = manager.connect(
    host="192.168.127.130",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

# Commented out capabilities display
'''
print("#Supported Capabilities (YANG models):")
for capability in m.server_capabilities:
    print(capability)
'''

# Get running configuration
netconf_reply = m.get_config(source="running")
print(netconf_reply)
```

**Ran script:**
```bash
python3 ncclient-netconf.py
```

**Output:** 100+ lines of unformatted XML containing entire running configuration including:
- Interface configurations (GigabitEthernet1)
- VTY line settings
- Licensing configuration
- Network instances
- Routing protocols
- NACM access control rules

**Note:** XML returned is compressed/unformatted, making it difficult to read.

### 9: Prettify XML Output with Python

**Updated script:** `ncclient-netconf.py`
```python
from ncclient import manager
import xml.dom.minidom

m = manager.connect(
    host="192.168.127.130",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

'''
print("#Supported Capabilities (YANG models):")
for capability in m.server_capabilities:
    print(capability)
'''

netconf_reply = m.get_config(source="running")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
```

**Ran script:**
```bash
python3 ncclient-netconf.py
```

**Output:** Properly formatted XML with indentation showing:
- Network instances and routing tables
- Interface configurations (GigabitEthernet1)
- NACM access control rules
- Routing protocols (static, directly connected)
- IPv4/IPv6 address families

**Example output structure:**
```xml
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
        <name>GigabitEthernet1</name>
        <description>VBox</description>
        <type>ianaift:ethernetCsmacd</type>
        <enabled>true</enabled>
    </interface>
</interfaces>
```

**Note:** XML now readable with proper indentation instead of single compressed line.

### 10: Filter NETCONF Query for Specific YANG Model

**Updated script:** `ncclient-netconf.py`
```python
from ncclient import manager
import xml.dom.minidom

m = manager.connect(
    host="192.168.127.130",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

'''
print("#Supported Capabilities (YANG models):")
for capability in m.server_capabilities:
    print(capability)
'''

netconf_filter = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
</filter>
"""

netconf_reply = m.get_config(source="running", filter=netconf_filter)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
```

**Ran script:**
```bash
python3 ncclient-netconf.py
```

**Result:** Filtered output showing only the Cisco IOS XE native YANG model data, significantly reducing output size compared to retrieving all YANG models. The filter eliminates other models like OpenConfig interfaces, NACM, and routing that were previously displayed.

**Note:** Filtering allows retrieval of specific configuration subsets rather than entire running config, improving efficiency for targeted queries.

### 11: Configure Device with NETCONF

**Step 1: Change hostname**

Added hostname configuration to script:
```python
netconf_hostname = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
 <hostname>NEWHOSTNAME</hostname>
 </native>
</config>
"""

netconf_reply = m.edit_config(target="running", config=netconf_hostname)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
```

Ran script, hostname changed to NEWHOSTNAME. Changed back to CSR1kv.

**Step 2: Create loopback interface**

Added loopback configuration:
```python
netconf_loopback = """
<config>
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
 <interface>
 <Loopback>
 <name>1</name>
 <description>My first NETCONF loopback</description>
 <ip>
 <address>
 <primary>
 <address>10.1.1.1</address>
 <mask>255.255.255.0</mask>
 </primary>
 </address>
 </ip>
 </Loopback>
 </interface>
</native>
</config>
"""

netconf_reply = m.edit_config(target="running", config=netconf_loopback)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
```

Result: Loopback1 created successfully with IP 10.1.1.1/24

**Step 3: Test duplicate IP address (validation)**

Added second loopback with same IP:
```python
netconf_newloop = """
<config>
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
 <interface>
 <Loopback>
 <name>2</name>
 <description>My second NETCONF loopback</description>
 <ip>
 <address>
 <primary>
 <address>10.1.1.1</address>
 <mask>255.255.255.0</mask>
 </primary>
 </address>
 </ip>
 </Loopback>
 </interface>
</native>
</config>
"""

netconf_reply = m.edit_config(target="running", config=netconf_newloop)
```

**Error received:**
```
ncclient.operations.rpc.RPCError: inconsistent value: Device refused one or more commands
```

**Verification:**
```bash
CSR1kv# show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       192.168.127.130 YES DHCP   up                    up      
Loopback1              10.1.1.1        YES other  up                    up
```

Result: Loopback2 was NOT created - NETCONF validated configuration and rejected duplicate IP before applying changes.

**Key learning:** NETCONF validates entire configuration before applying. If any command fails, none are applied.