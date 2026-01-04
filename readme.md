# Lab Setup Documentation
# IAN TERRYN 

## Part 1: Install DEVASC VM

### Task Preparation and Implementation

**Steps:**
1. Import OVA in VMware: File > Open > Select DEVASC VM OVA
2. Power On VM
3. Accept Packet Tracer EULA (arrow keys + I Agree)
4. Wait for Ubuntu desktop to load

### Task Troubleshooting

No problems encountered. VM booted to desktop without issues.

### Task Verification

**Verification method:** Visual verification
- No login required - boots to desktop automatically
- Ubuntu desktop loaded successfully

---

## Part 2: Install CSR1000v VM

### Task Preparation and Implementation

**Steps:**
1. Import OVA: File > Open > Select CSR1000v_for_VMware.ova
2. Edit VM Settings > First CD/DVD Drive > Browse > Select csr1000v-universalk9.16.09.05.iso
3. Power On VM
4. Wait 5-10 minutes for boot (ignore "Press any key" messages)
5. Press Enter when messages stop

### Task Troubleshooting

**Problem:** Boot process took longer than expected
- **Solution:** Waited 5-10 minutes as per documentation, ignored "Press any key" messages

### Task Verification

**Verification method:** CLI command verification
```bash
CSR1kv# show ip interface brief
```
**Result:** IP Address: 192.168.127.130

**Connectivity test from DEVASC VM:**
```bash
ping 192.168.127.130
ssh cisco@192.168.127.130
```
**Password:** cisco123!

**Status:** Both VMs operational and communicating

---

## Part 3a: Python Network Automation with Netmiko - Connecting to an IOS-XE Device

### Task Preparation and Implementation

**Tools used:**
- Python 3
- Netmiko library
- VMware (DEVASC VM + CSR1000v)

**Installation:**
```bash
pip3 install netmiko
```

**Implementation:**
Created comprehensive script `netmiko_complete.py` with:
- Dictionary-based device connection
- Class-based implementation (`NetworkAutomation`)
- Functions for each task:
  1. Show commands (single device)
  2. Configuration commands
  3. Save output to file
  4. Backup configuration
  5. Configure from external file
  6. Configure multiple interfaces
  7. Multiple device operations
- Conditional statements (if/else) throughout
- Menu-driven interface

**Key code snippets:**

1. **Show commands:**
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

3. **Backup configuration:**
```python
def backup_config(self):
    config = self.connection.send_command('show running-config')
    filename = f"{hostname}_backup_{timestamp}.cfg"
```

### Task Troubleshooting

**Probleem 1:** Connection timeout on first attempt
- **Solution:** CSR1000v needed to fully boot (wait 5-10 minutes)

**Probleem 2:** SSH authentication failed
- **Solution:** Verified password is `cisco123!` (with exclamation mark)

**Probleem 3:** IP address different than lab document
- **Solution:** Used `show ip interface brief` to confirm actual IP: `192.168.127.130`

### Task Verification

**Test methods:**
1. Tested all menu options in `netmiko_complete.py`
2. CLI verification on CSR1000v
3. File output verification

**Test results:**

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

**Verification on CSR1000v:**
```bash
ssh cisco@192.168.127.130
show ip int brief | include Loop
```
Output confirmed all configured interfaces present.

---

## Part 3b: Network Diagnostics Collector

### Task Preparation and Implementation

**Goal:** Automatically collect comprehensive diagnostic information and save to timestamped file.

**Script:** `network_diagnostics.py`

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

**Features:**
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

**Probleem 1:** Large output files
- **Solution:** This is expected - full diagnostics are comprehensive

**Probleem 2:** `show logging` took longer than other commands
- **Solution:** Added slight delay, normal for log retrieval

### Task Verification

**Test method:** Script execution and output validation

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

## Part 4: YANG Data Models

### Task Preparation and Implementation

**Steps:**
1. VM was already available (DEVASC)
2. Downloaded `ietf-interfaces.yang` file
3. Placed file in `~/devnet` directory
4. Executed pyang tree command

### Task Troubleshooting

**Problem:** Module "ietf-yang-types" not found warning
- **Note:** This is a non-blocking warning, tree output still generated successfully

### Task Verification

**Verification method:** pyang tree command execution

**Command:**
```bash
pyang -f tree ietf-interfaces.yang
```

**Output:**
```
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
```

**Result:** YANG model tree successfully displayed

---

## Part 5: NETCONF Configuration

### Task 5.1: SSH Access Troubleshooting

#### Task Preparation and Implementation

**Goal:** Establish SSH access to CSR1000v router

**Steps:**
1. Test connectivity with ping
2. Identify correct IP address
3. Troubleshoot SSH host key issues
4. Establish successful SSH connection

#### Task Troubleshooting

**Probleem 1:** Unable to ping 192.168.0.130
- **Cause:** Wrong IP address
- **Solution:** Corrected to 192.168.127.130
- **Verification:** `ping 192.168.127.130` - Connectivity confirmed (2/3 packets received)

**Probleem 2:** SSH host key verification failed
```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```
- **Cause:** Old SSH host key stored in `~/.ssh/known_hosts` from previous VM installation
- **Solution:**
```bash
ssh-keygen -f "/home/devasc/.ssh/known_hosts" -R "192.168.127.130"
```

#### Task Verification

**Verification method:** Successful SSH connection

**Command:**
```bash
ssh cisco@192.168.127.130
```
**Password:** cisco123!

**Result:** SSH access successful

---

### Task 5.2: NETCONF Session Operations

#### Task Preparation and Implementation

**Goal:** Manually establish NETCONF session via SSH

**Steps:**
1. Start NETCONF session on port 830
2. Send client hello message
3. Query interface information
4. Close session

**Commands used:**
```bash
ssh cisco@192.168.127.130 -p 830 -s netconf
```

**Client hello message:**
```xml
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<capabilities>
<capability>urn:ietf:params:netconf:base:1.0</capability>
</capabilities>
</hello>
]]>]]>
```

**RPC request:**
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

#### Task Troubleshooting

No problems encountered. NETCONF session worked immediately after correct configuration.

#### Task Verification

**Verification methods:**
1. Verify session on router
2. Verify RPC response
3. Verify session closure

**Verification 1 - Active session:**
```bash
CSR1kv# show netconf-yang sessions
```
**Result:** Session 24 active

**Verification 2 - RPC response received:**
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

**Verification 3 - Session closed:**
```bash
CSR1kv# show netconf-yang sessions
```
**Result:** "There are no active sessions"

---

### Task 5.3: Python NETCONF with ncclient

#### Task Preparation and Implementation

**Steps:**
1. Create netconf directory
2. Install ncclient library
3. Create Python script for NETCONF connection

**Directory setup:**
```bash
mkdir netconf
cd netconf
```

**Script:** `ncclient-netconf.py`
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

#### Task Troubleshooting

No problems encountered. ncclient connection worked immediately.

#### Task Verification

**Verification methods:**
1. Script execution without errors
2. Router logs verification

**Test 1 - Script execution:**
```bash
python3 ncclient-netconf.py
```
**Result:** No errors, connection successful

**Test 2 - Router logs:**
```
*Dec 25 15:53:48.860: %DMI-5-AUTH_PASSED: M0/0: dmiauthd: User 'cisco' authenticated successfully from 192.168.127.1:51512 and was authorized for netconf over ssh. External groups: PRIV15
```

**Result:** NETCONF session established via ncclient

---

### Task 5.4: Display NETCONF Capabilities

#### Task Preparation and Implementation

**Goal:** Retrieve and display all NETCONF capabilities (YANG models) supported by the router

**Updated script:**
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

#### Task Troubleshooting

No problems encountered.

#### Task Verification

**Verification method:** Script execution and output review

**Executed:**
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
urn:ietf:params:xml:ns:netconf:base:1.0?module=ietf-netconf&revision=2011-06-01
urn:ietf:params:xml:ns:yang:ietf-netconf-with-defaults?module=ietf-netconf-with-defaults&revision=2011-06-01
urn:ietf:params:netconf:capability:notification:1.1
```

**Result:** All capabilities displayed successfully (same as manual NETCONF hello exchange)

---

### Task 5.5: Retrieve Running Configuration

#### Task Preparation and Implementation

**Method:** Use ncclient `get_config()` method to retrieve running configuration

**Updated script:**
```python
from ncclient import manager

m = manager.connect(
    host="192.168.127.130",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

netconf_reply = m.get_config(source="running")
print(netconf_reply)
```

#### Task Troubleshooting

**Problem:** XML output is unformatted and difficult to read
- **Note:** This will be addressed in next task with prettification

#### Task Verification

**Verification method:** Script execution and output inspection

**Executed:**
```bash
python3 ncclient-netconf.py
```

**Result:** 100+ lines of XML containing entire running configuration including:
- Interface configurations (GigabitEthernet1)
- VTY line settings
- Licensing configuration
- Network instances
- Routing protocols
- NACM access control rules

---

### Task 5.6: Prettify XML Output

#### Task Preparation and Implementation

**Goal:** Format XML output for better readability

**Tools:** Python `xml.dom.minidom` library

**Updated script:**
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

netconf_reply = m.get_config(source="running")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
```

#### Task Troubleshooting

No problems encountered.

#### Task Verification

**Verification method:** Visual inspection of formatted output

**Executed:**
```bash
python3 ncclient-netconf.py
```

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

**Result:** XML now readable with proper indentation instead of single compressed line

---

### Task 5.7: Filter NETCONF Query for Specific YANG Model

#### Task Preparation and Implementation

**Goal:** Retrieve only specific YANG model data instead of entire configuration

**YANG model used:** Cisco IOS XE native

**Updated script:**
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

netconf_filter = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
</filter>
"""

netconf_reply = m.get_config(source="running", filter=netconf_filter)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
```

#### Task Troubleshooting

No problems encountered.

#### Task Verification

**Verification method:** Output comparison (filtered vs unfiltered)

**Executed:**
```bash
python3 ncclient-netconf.py
```

**Result:** Filtered output showing only the Cisco IOS XE native YANG model data, significantly reducing output size. Filter eliminated other models like OpenConfig interfaces, NACM, and routing.

**Conclusion:** Filtering allows retrieval of specific configuration subsets, improving efficiency for targeted queries.

---

### Task 5.8: Configure Device with NETCONF

#### Task Preparation and Implementation

**Goal:** Demonstrate NETCONF configuration capabilities and validation

**Configurations:**
1. Change hostname
2. Create loopback interface
3. Test duplicate IP validation

**Step 1 - Change hostname:**
```python
netconf_hostname = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
 <hostname>NEWHOSTNAME</hostname>
 </native>
</config>
"""

netconf_reply = m.edit_config(target="running", config=netconf_hostname)
```

**Step 2 - Create loopback:**
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
```

**Step 3 - Test duplicate IP:**
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

#### Task Troubleshooting

**Problem:** Duplicate IP address rejected
- **Error:** `ncclient.operations.rpc.RPCError: inconsistent value: Device refused one or more commands`
- **Cause:** NETCONF validation detected duplicate IP address
- **Result:** This is expected behavior - NETCONF validates before applying

#### Task Verification

**Verification methods:**
1. Hostname change verification
2. Loopback1 creation verification
3. Loopback2 rejection verification

**Verification 1 - Hostname:**
```bash
CSR1kv# show running-config | include hostname
```
**Result:** Hostname changed to NEWHOSTNAME

**Verification 2 - Loopback1:**
```bash
NEWHOSTNAME# show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       192.168.127.130 YES DHCP   up                    up
Loopback1              10.1.1.1        YES other  up                    up
```
**Result:** Loopback1 created successfully

**Verification 3 - Loopback2:**
```bash
NEWHOSTNAME# show ip interface brief
```
**Result:** Loopback2 NOT created - NETCONF validation prevented duplicate IP

**Key learning:** NETCONF validates entire configuration before applying. If any command fails, none are applied.

---

### Task 5.9: Part 6 Challenge - Advanced NETCONF Operations

#### Task Preparation and Implementation

**Goal:** Create advanced reusable NETCONF automation script

**Script:** `netconf_challenge.py`

**Features:**
- Function-based structure for reusability
- Dynamic loopback creation with parameters
- Interface deletion capability
- Interface query and display

**Script structure:**
```python
from ncclient import manager
import xml.dom.minidom

def connect_device():
    return manager.connect(
        host="192.168.127.130",
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False
    )

def create_loopback(m, loop_num, ip_address):
    # Creates loopback with specified number and IP

def delete_loopback(m, loop_num):
    # Deletes loopback by number using NETCONF delete operation

def get_interfaces(m):
    # Retrieves and formats all interfaces
```

**Operations performed:**
1. Create Loopback100 with IP 10.100.100.1/24
2. Create Loopback200 with IP 10.200.200.1/24
3. Retrieve all interfaces in formatted XML
4. Delete Loopback100

#### Task Troubleshooting

No problems encountered. All operations worked as expected.

#### Task Verification

**Verification method:** Script execution and router verification

**Executed:**
```bash
python3 ncclient-netconf.py
```

**Output:**
```
Created Loopback100: 10.100.100.1
Created Loopback200: 10.200.200.1

--- Current Interfaces ---
<?xml version="1.0" ?>
<rpc-reply>
  <data>
    <interfaces>
      <interface>
        <name>GigabitEthernet1</name>
        <description>VBox</description>
      </interface>
      <interface>
        <name>Loopback1</name>
        <ip>10.1.1.1</ip>
      </interface>
      <interface>
        <name>Loopback100</name>
        <ip>10.100.100.1</ip>
      </interface>
      <interface>
        <name>Loopback200</name>
        <ip>10.200.200.1</ip>
      </interface>
    </interfaces>
  </data>
</rpc-reply>

Deleted Loopback100
Script complete!
```

**Router verification:**
```bash
NEWHOSTNAME# show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       192.168.127.130 YES DHCP   up                    up
Loopback1              10.1.1.1        YES other  up                    up
Loopback200            10.200.200.1    YES other  up                    up
```

**Result:**
- Loopback100 successfully deleted
- Loopback200 remains configured
- All operations completed successfully

**Key skills demonstrated:**
- Programmatic interface creation/deletion
- Dynamic configuration using f-strings
- Structured functions for reusable NETCONF code
- Complete automation workflow
- NETCONF delete operations

---

## NETCONF Lab Summary

**Completed tasks:**
- Task 5.1: SSH access troubleshooting
- Task 5.2: Manual NETCONF session operations
- Task 5.3: Python ncclient connection
- Task 5.4: Display NETCONF capabilities
- Task 5.5: Retrieve running configuration
- Task 5.6: Prettify XML output
- Task 5.7: Filter queries for specific YANG models
- Task 5.8: Device configuration with validation
- Task 5.9: Advanced programmatic operations

**Final router state:**
- Hostname: NEWHOSTNAME
- Interfaces: GigabitEthernet1, Loopback1, Loopback200
- All configurations applied via NETCONF

---

## Part 6: RESTCONF Configuration

### Task 6.1: Connectivity Verification

#### Task Preparation and Implementation

**Goal:** Verify network connectivity before RESTCONF configuration

**Commands:**
```bash
ping 192.168.127.130
ssh cisco@192.168.127.130
```

#### Task Troubleshooting

No problems. Connectivity worked from earlier configuration.

#### Task Verification

**Verification method:** Successful ping and SSH connection

**Result:**
- Ping successful
- SSH connection established with password: `cisco123!`

---

### Task 6.2: Configure RESTCONF on CSR1kv

#### Task Preparation and Implementation

**Goal:** Enable RESTCONF API and HTTPS server on router

**Configuration commands:**
```bash
NEWHOSTNAME# configure terminal
NEWHOSTNAME(config)# restconf
NEWHOSTNAME(config)# ip http secure-server
NEWHOSTNAME(config)# ip http authentication local
NEWHOSTNAME(config)# exit
```

**Services enabled:**
- RESTCONF API
- HTTPS server (nginx)
- Local authentication

#### Task Troubleshooting

No problems. Services started immediately after configuration.

#### Task Verification

**Verification method:** Check YANG management processes

**Command:**
```bash
NEWHOSTNAME# show platform software yang-management process
```

**Output:**
```
confd            : Running
nesd             : Running
syncfd           : Running
ncsshd           : Running
dmiauthd         : Running
nginx            : Running
ndbmand          : Running
pubd             : Running
```

**Result:** nginx (HTTPS server) running and ready for RESTCONF API calls

---

### Task 6.3: Configure Postman

#### Task Preparation and Implementation

**Goal:** Disable SSL verification for self-signed certificates

**Settings:**
- File > Settings > SSL certificate verification: OFF

#### Task Troubleshooting

No problems.

#### Task Verification

**Verification method:** Setting visible in Postman preferences

---

### Task 6.4: Postman GET Requests

#### Task Preparation and Implementation

**Goal:** Test RESTCONF connectivity and retrieve interface data

**Test 1: Verify RESTCONF connection**

**Request configuration:**
- Type: GET
- URL: `https://192.168.127.130/restconf/`
- Authorization: Basic Auth (cisco / cisco123!)
- Headers:
  - Content-Type: `application/yang-data+json`
  - Accept: `application/yang-data+json`

**Test 2: Get all interfaces**

**Request:**
- URL: `https://192.168.127.130/restconf/data/ietf-interfaces:interfaces`

**Test 3: Configure static IP**

Due to DHCP IP not showing in RESTCONF responses, configured static IP:
```bash
configure terminal
interface GigabitEthernet1
ip address 192.168.127.130 255.255.255.0
end
```

**Test 4: Get specific interface**

**Request:**
- URL: `https://192.168.127.130/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1`

#### Task Troubleshooting

**Problem:** DHCP IP address doesn't show in RESTCONF responses
- **Solution:** Configured static IP address on GigabitEthernet1

#### Task Verification

**Verification method:** Postman response status and content

**Test 1 Result:**
```json
{
    "ietf-restconf:restconf": {
        "data": {},
        "operations": {},
        "yang-library-version": "2016-06-21"
    }
}
```
**Status:** 200 OK - RESTCONF connection verified

**Test 2 Result:** JSON data showing all interfaces (GigabitEthernet1, Loopback1, Loopback200)

**Test 4 Result:**
```json
{
    "ietf-interfaces:interface": {
        "name": "GigabitEthernet1",
        "description": "VBox",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": true,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "192.168.127.130",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}
```

**Result:** IP address now visible in RESTCONF response

---

### Task 6.5: Postman PUT Request

#### Task Preparation and Implementation

**Goal:** Create new loopback interface using RESTCONF PUT

**Request configuration:**
- Type: PUT
- URL: `https://192.168.127.130/restconf/data/ietf-interfaces:interfaces/interface=Loopback3`
- Body (raw JSON):
```json
{
  "ietf-interfaces:interface": {
    "name": "Loopback3",
    "description": "My first RESTCONF loopback",
    "type": "iana-if-type:softwareLoopback",
    "enabled": true,
    "ietf-ip:ipv4": {
      "address": [
        {
          "ip": "10.3.3.3",
          "netmask": "255.255.255.0"
        }
      ]
    },
    "ietf-ip:ipv6": {}
  }
}
```

#### Task Troubleshooting

No problems. Interface was created immediately.

#### Task Verification

**Verification methods:**
1. Postman response status
2. Router CLI verification

**Verification 1 - Postman:**
**Response:** Status: 201 Created

**Verification 2 - Router CLI:**
```bash
NEWHOSTNAME# show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       192.168.127.130 YES manual up                    up
Loopback1              10.1.1.1        YES other  up                    up
Loopback3              10.3.3.3        YES other  up                    up
Loopback200            10.200.200.1    YES other  up                    up
```

**Result:** Loopback3 successfully created via RESTCONF PUT request

---

### Task 6.6: Python RESTCONF GET Script

#### Task Preparation and Implementation

**Goal:** Retrieve interface data programmatically using Python requests library

**Script:** `restconf-get.py`
```python
import json
import requests
requests.packages.urllib3.disable_warnings()

api_url = "https://192.168.127.130/restconf/data/ietf-interfaces:interfaces"

headers = { "Accept": "application/yang-data+json",
            "Content-type":"application/yang-data+json"
          }

basicauth = ("cisco", "cisco123!")

resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

print(resp)

response_json = resp.json()
print(json.dumps(response_json, indent=4))
```

#### Task Troubleshooting

No problems. Script worked immediately.

#### Task Verification

**Verification method:** Script execution and output validation

**Executed:**
```bash
python3 restconf-get.py
```

**Output:**
```
<Response [200]>
{
    "ietf-interfaces:interfaces": {
        "interface": [
            {
                "name": "GigabitEthernet1",
                "ip": "192.168.127.130"
            },
            {
                "name": "Loopback1",
                "ip": "10.1.1.1"
            },
            {
                "name": "Loopback3",
                "ip": "10.3.3.3"
            },
            {
                "name": "Loopback200",
                "ip": "10.200.200.1"
            }
        ]
    }
}
```

**Result:** Python script successfully retrieves and formats interface data from RESTCONF API

---

### Task 6.7: Python RESTCONF PUT Script

#### Task Preparation and Implementation

**Goal:** Create new interface programmatically using Python

**Script:** `restconf-put.py`
```python
import json
import requests
requests.packages.urllib3.disable_warnings()

api_url = "https://192.168.127.130/restconf/data/ietf-interfaces:interfaces/interface=Loopback4"

headers = { "Accept": "application/yang-data+json",
            "Content-type":"application/yang-data+json"
          }

basicauth = ("cisco", "cisco123!")

yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback4",
        "description": "My second RESTCONF loopback",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "10.4.4.4",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}

resp = requests.put(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

if(resp.status_code >= 200 and resp.status_code <= 299):
    print("STATUS OK: {}".format(resp.status_code))
else:
    print('Error. Status Code: {} \nError message: {}'.format(resp.status_code,resp.json()))
```

#### Task Troubleshooting

No problems. Interface was created immediately.

#### Task Verification

**Verification methods:**
1. Script output
2. Router CLI verification

**Verification 1 - Script output:**
```bash
python3 restconf-put.py
```
**Output:**
```
STATUS OK: 201
```

**Verification 2 - Router CLI:**
```bash
NEWHOSTNAME# show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       192.168.127.130 YES manual up                    up
Loopback1              10.1.1.1        YES other  up                    up
Loopback3              10.3.3.3        YES other  up                    up
Loopback4              10.4.4.4        YES other  up                    up
Loopback200            10.200.200.1    YES other  up                    up
```

**Result:** Loopback4 successfully created via Python RESTCONF PUT request

---

## RESTCONF Lab Summary

**Completed tasks:**
- Task 6.1: VM connectivity verification
- Task 6.2: RESTCONF and HTTPS configuration on CSR1kv
- Task 6.3: Postman SSL configuration
- Task 6.4: Postman GET requests (verify, get all, get specific)
- Task 6.5: Postman PUT request (created Loopback3)
- Task 6.6: Python GET script
- Task 6.7: Python PUT script (created Loopback4)

**Key concepts demonstrated:**
- RESTCONF API over HTTPS
- RESTful operations (GET, PUT)
- YANG data models (ietf-interfaces)
- JSON data formatting
- Basic authentication
- Python requests library
- Postman API testing

**Final router state:**
- Hostname: NEWHOSTNAME
- Interfaces: GigabitEthernet1, Loopback1, Loopback3, Loopback4, Loopback200
- All RESTCONF operations successful

---

## Task 38: RESTCONF GitHub-Based Configuration Deployment

### Task Preparation and Implementation

**Goal:** Develop an automated solution that fetches network configuration from GitHub and deploys it to a Cisco IOS-XE device using RESTCONF and YANG models.

**Requirements:**
- Use RESTCONF only (no NETCONF, no CLI)
- Configuration must be YANG-compliant (JSON format)
- GitHub as single source of truth
- Configure: hostname, interfaces with IP addresses, OSPF routing
- Check HTTP status codes and log all operations

**Script:** `restconf-github-deploy.py`

**Implementation approach:**

1. **GitHub configuration storage:**
   - Created `cisco-config.json` in repository
   - Contains hostname, interface, and OSPF configuration
   - Accessible via GitHub raw URL

2. **Python script structure:**
```python
def fetch_config_from_github():
    # Fetches JSON configuration from GitHub

def configure_hostname(hostname):
    # Uses RESTCONF PUT to set hostname

def configure_interface(interface_config):
    # Uses RESTCONF PUT with ietf-interfaces YANG model

def configure_ospf(ospf_config):
    # Uses RESTCONF PATCH with Cisco-IOS-XE-ospf YANG model

def verify_configuration():
    # Verifies all changes were applied

def main():
    # Orchestrates deployment with success/failure tracking
```

3. **YANG models used:**
   - **Hostname:** `Cisco-IOS-XE-native:native/hostname`
   - **Interfaces:** `ietf-interfaces:interfaces` (standard IETF model)
   - **OSPF:** `Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospf:ospf`

4. **Key features:**
   - Comprehensive logging (timestamped file + console output)
   - HTTP status code validation (200-299 range)
   - Error handling with try/except blocks
   - Success/failure counters
   - Configuration verification after deployment
   - Idempotent operations (can run multiple times safely)

**Configuration example (cisco-config.json):**
```json
{
  "hostname": "NETAUTO-R1",
  "interfaces": [
    {
      "name": "Loopback10",
      "description": "Management Loopback",
      "type": "iana-if-type:softwareLoopback",
      "ip": "10.10.10.1",
      "netmask": "255.255.255.0"
    },
    {
      "name": "Loopback20",
      "description": "OSPF Loopback",
      "type": "iana-if-type:softwareLoopback",
      "ip": "10.20.20.1",
      "netmask": "255.255.255.0"
    }
  ],
  "ospf": {
    "process_id": "1",
    "router_id": "1.1.1.1",
    "networks": [
      {
        "ip": "10.10.10.0",
        "wildcard": "0.0.0.255",
        "area": "0"
      },
      {
        "ip": "10.20.20.0",
        "wildcard": "0.0.0.255",
        "area": "0"
      }
    ]
  }
}
```

### Task Troubleshooting

**Problem 1:** Multiple duplicate OSPF function definitions in initial script
- **Cause:** Multiple attempts at finding correct YANG model structure left orphaned code blocks (7 versions of `configure_ospf()`)
- **Solution:** Cleaned up script, removed lines 189-513 containing orphaned code
- **Result:** File reduced from 607 lines to 281 lines, single clean `configure_ospf()` function

**Problem 2:** Finding correct YANG model structure for OSPF
- **Cause:** OSPF YANG model structure is complex with nested elements
- **Solution:** Used RESTCONF PATCH with proper structure:
```python
payload = {
    "Cisco-IOS-XE-native:router": {
        "Cisco-IOS-XE-ospf:ospf": [
            {
                "id": int(process_id),
                "router-id": router_id,
                "network": networks
            }
        ]
    }
}
```
- **Note:** YANG model uses "mask" instead of "wildcard" for network statements

**Problem 3:** Initial confusion about idempotency
- **Solution:** Confirmed that RESTCONF PUT operations are idempotent - running script multiple times produces same result without errors

### Task Verification

**Test method:** Execute script and verify via logging and device verification

**Execution:**
```bash
python3 restconf-github-deploy.py
```

**Output:**
```
2026-01-04 16:41:00,376 - INFO - ============================================================
2026-01-04 16:41:00,376 - INFO - RESTCONF GitHub Deployment Started
2026-01-04 16:41:00,376 - INFO - ============================================================
2026-01-04 16:41:00,376 - INFO - Fetching configuration from GitHub: https://raw.githubusercontent.com/IanTerrynPXL/Networks-Expert-Lab3/refs/heads/main/cisco-config.json
2026-01-04 16:41:00,646 - INFO - ✓ Successfully fetched configuration from GitHub
2026-01-04 16:41:00,646 - INFO - Configuring hostname: NETAUTO-R1
2026-01-04 16:41:02,058 - INFO - ✓ Hostname configured successfully (Status: 204)
2026-01-04 16:41:02,058 - INFO - Configuring interface: Loopback10
2026-01-04 16:41:02,425 - INFO - ✓ Interface Loopback10 configured (Status: 201)
2026-01-04 16:41:02,425 - INFO - Configuring interface: Loopback20
2026-01-04 16:41:02,805 - INFO - ✓ Interface Loopback20 configured (Status: 201)
2026-01-04 16:41:02,805 - INFO - Configuring OSPF process 1
2026-01-04 16:41:03,103 - INFO - ✓ OSPF configured successfully (Status: 204)
2026-01-04 16:41:03,103 - INFO - Verifying configuration...
2026-01-04 16:41:03,170 - INFO - ✓ Current hostname: NETAUTO-R1
2026-01-04 16:41:03,300 - INFO - ✓ Total interfaces configured: 3
2026-01-04 16:41:03,301 - INFO -   - GigabitEthernet1: VBox
2026-01-04 16:41:03,301 - INFO -   - Loopback10: Management Loopback
2026-01-04 16:41:03,301 - INFO -   - Loopback20: OSPF Loopback
2026-01-04 16:41:03,301 - INFO - ============================================================
2026-01-04 16:41:03,302 - INFO - Deployment Summary:
2026-01-04 16:41:03,302 - INFO -   Successful operations: 4
2026-01-04 16:41:03,302 - INFO -   Failed operations: 0
2026-01-04 16:41:03,302 - INFO - ✓ Deployment completed successfully!
2026-01-04 16:41:03,303 - INFO - ============================================================
```

**Verification results:**

**HTTP Status Codes:**
- **204 No Content** - Successful modification (hostname, OSPF)
- **201 Created** - Successfully created new resources (interfaces)

**Operations completed:**
1. ✓ Fetched configuration from GitHub
2. ✓ Configured hostname: NETAUTO-R1
3. ✓ Created Loopback10 (10.10.10.1/24) with description
4. ✓ Created Loopback20 (10.20.20.1/24) with description
5. ✓ Configured OSPF process 1 with router-id 1.1.1.1
6. ✓ Verified all changes applied

**Device verification:**
```bash
NETAUTO-R1# show running-config | section hostname
hostname NETAUTO-R1

NETAUTO-R1# show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       192.168.127.130 YES manual up                    up
Loopback10             10.10.10.1      YES other  up                    up
Loopback20             10.20.20.1      YES other  up                    up

NETAUTO-R1# show ip ospf neighbor
# OSPF process running with configured networks
```