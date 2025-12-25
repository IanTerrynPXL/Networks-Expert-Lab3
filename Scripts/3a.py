from netmiko import ConnectHandler
from datetime import datetime
import os

# Device dictionary
device_csr = {
    'device_type': 'cisco_ios',
    'host': '192.168.127.130',
    'username': 'cisco',
    'password': 'cisco123!',
}

# Multiple devices (add more if available)
devices = [device_csr]

class NetworkAutomation:
    def __init__(self, device):
        self.device = device
        self.connection = None
    
    def connect(self):
        """Connect to device"""
        print(f"Connecting to {self.device['host']}...")
        self.connection = ConnectHandler(**self.device)
        print("Connected!")
    
    def disconnect(self):
        """Disconnect from device"""
        if self.connection:
            self.connection.disconnect()
            print("Disconnected.")
    
    def send_show_command(self, command):
        """Send show command"""
        output = self.connection.send_command(command)
        return output
    
    def send_config_commands(self, commands):
        """Send configuration commands"""
        output = self.connection.send_config_set(commands)
        return output
    
    def save_output(self, command, filename=None):
        """Run show command and save output"""
        output = self.send_show_command(command)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(output)
        
        print(f"Output saved to {filename}")
        return filename
    
    def backup_config(self):
        """Backup device configuration"""
        hostname = self.connection.send_command('show run | include hostname').split()[1]
        config = self.connection.send_command('show running-config')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{hostname}_backup_{timestamp}.cfg"
        
        with open(filename, 'w') as f:
            f.write(config)
        
        print(f"Backup saved: {filename}")
        return filename
    
    def config_from_file(self, filepath):
        """Configure device from external file"""
        if not os.path.exists(filepath):
            print(f"Error: File {filepath} not found!")
            return None
        
        with open(filepath, 'r') as f:
            commands = f.read().splitlines()
        
        output = self.send_config_commands(commands)
        print("Configuration applied from file.")
        return output
    
    def configure_interfaces(self, interface_list):
        """Configure subset of interfaces"""
        for interface in interface_list:
            commands = [
                f"interface {interface['name']}",
                f"description {interface['description']}",
            ]
            if 'ip' in interface:
                commands.append(f"ip address {interface['ip']} {interface['mask']}")
            
            output = self.send_config_commands(commands)
            print(f"Configured {interface['name']}")

def show_commands_multiple_devices(devices, command):
    """Send show command to multiple devices"""
    results = {}
    for device in devices:
        net = NetworkAutomation(device)
        net.connect()
        output = net.send_show_command(command)
        results[device['host']] = output
        net.disconnect()
    return results

def config_multiple_devices(devices, commands):
    """Send config commands to multiple devices"""
    for device in devices:
        net = NetworkAutomation(device)
        net.connect()
        output = net.send_config_commands(commands)
        print(f"\n--- {device['host']} ---")
        print(output)
        net.disconnect()

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("NETMIKO NETWORK AUTOMATION MENU")
        print("="*50)
        print("1.  Send show command")
        print("2.  Send config commands")
        print("3.  Save show command output")
        print("4.  Backup device configuration")
        print("5.  Configure from file")
        print("6.  Configure multiple interfaces")
        print("7.  Show command on multiple devices")
        print("8.  Config multiple devices")
        print("9.  Exit")
        print("="*50)
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            command = input("Enter show command: ")
            net = NetworkAutomation(device_csr)
            net.connect()
            output = net.send_show_command(command)
            print(output)
            net.disconnect()
        
        elif choice == '2':
            print("Enter config commands (empty line to finish):")
            commands = []
            while True:
                cmd = input()
                if cmd == '':
                    break
                commands.append(cmd)
            
            net = NetworkAutomation(device_csr)
            net.connect()
            output = net.send_config_commands(commands)
            print(output)
            net.disconnect()
        
        elif choice == '3':
            command = input("Enter show command: ")
            net = NetworkAutomation(device_csr)
            net.connect()
            net.save_output(command)
            net.disconnect()
        
        elif choice == '4':
            net = NetworkAutomation(device_csr)
            net.connect()
            net.backup_config()
            net.disconnect()
        
        elif choice == '5':
            filepath = input("Enter config file path: ")
            net = NetworkAutomation(device_csr)
            net.connect()
            net.config_from_file(filepath)
            net.disconnect()
        
        elif choice == '6':
            interfaces = [
                {'name': 'Loopback10', 'description': 'Test Interface 1', 'ip': '10.10.10.1', 'mask': '255.255.255.0'},
                {'name': 'Loopback11', 'description': 'Test Interface 2', 'ip': '10.11.11.1', 'mask': '255.255.255.0'},
            ]
            net = NetworkAutomation(device_csr)
            net.connect()
            net.configure_interfaces(interfaces)
            net.disconnect()
        
        elif choice == '7':
            command = input("Enter show command: ")
            results = show_commands_multiple_devices(devices, command)
            for host, output in results.items():
                print(f"\n--- {host} ---")
                print(output)
        
        elif choice == '8':
            print("Enter config commands (empty line to finish):")
            commands = []
            while True:
                cmd = input()
                if cmd == '':
                    break
                commands.append(cmd)
            config_multiple_devices(devices, commands)
        
        elif choice == '9':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()