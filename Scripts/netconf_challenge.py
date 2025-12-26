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
    config = f"""
    <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
     <interface>
     <Loopback>
     <name>{loop_num}</name>
     <description>Auto-created loopback {loop_num}</description>
     <ip>
     <address>
     <primary>
     <address>{ip_address}</address>
     <mask>255.255.255.0</mask>
     </primary>
     </address>
     </ip>
     </Loopback>
     </interface>
    </native>
    </config>
    """
    reply = m.edit_config(target="running", config=config)
    print(f"Created Loopback{loop_num}: {ip_address}")
    return reply

def delete_loopback(m, loop_num):
    config = f"""
    <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
     <interface>
     <Loopback operation="delete">
     <name>{loop_num}</name>
     </Loopback>
     </interface>
    </native>
    </config>
    """
    reply = m.edit_config(target="running", config=config)
    print(f"Deleted Loopback{loop_num}")
    return reply

def get_interfaces(m):
    filter = """
    <filter>
     <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
    </filter>
    """
    reply = m.get_config(source="running", filter=filter)
    return xml.dom.minidom.parseString(reply.xml).toprettyxml()

# Main program
m = connect_device()

# Create multiple loopbacks
create_loopback(m, 100, "10.100.100.1")
create_loopback(m, 200, "10.200.200.1")

# Show interfaces
print("\n--- Current Interfaces ---")
print(get_interfaces(m))

# Delete a loopback
delete_loopback(m, 100)

print("\nScript complete!")