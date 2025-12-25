from netmiko import ConnectHandler
from datetime import datetime

# Device info
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.127.130',
    'username': 'cisco',
    'password': 'cisco123!',
}

# All the commands to run
diagnostic_commands = [
    'show version',
    'show running-config',
    'show ip interface brief',
    'show ip route',
    'show interfaces',
    'show interfaces status',
    'show ip arp',
    'show processes cpu',
    'show processes memory',
    'show logging',
    'show users',
    'show clock',
    'show inventory',
]

def collect_diagnostics():
    """Collect all diagnostic info and save to file"""
    print("Connecting to device...")
    connection = ConnectHandler(**device)
    print("Connected!\n")
    
    # Get hostname for filename
    hostname = connection.send_command('show run | include hostname').split()[1]
    
    # Create output file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{hostname}_diagnostics_{timestamp}.txt"
    
    print(f"Collecting diagnostics and saving to {filename}...\n")
    
    with open(filename, 'w') as f:
        # Header
        f.write("="*70 + "\n")
        f.write(f"NETWORK DIAGNOSTICS REPORT\n")
        f.write(f"Device: {hostname}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        # Run each command
        for cmd in diagnostic_commands:
            print(f"Running: {cmd}")
            
            f.write("\n" + "="*70 + "\n")
            f.write(f"COMMAND: {cmd}\n")
            f.write("="*70 + "\n\n")
            
            output = connection.send_command(cmd)
            f.write(output + "\n")
    
    connection.disconnect()

    print(f"\n✓ All diagnostics saved to: {filename}")
    print(f"✓ Total commands executed: {len(diagnostic_commands)}")

if __name__ == "__main__":
    collect_diagnostics()
