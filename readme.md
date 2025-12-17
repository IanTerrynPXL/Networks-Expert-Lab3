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