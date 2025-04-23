from smolagents import tool, Tool
import ipaddress
import socket
import netifaces

class NetworkTools(Tool):
    name = "network_tools"
    description = "Tools for network discovery and topology mapping using ping3"

    def __init__(self):
        self.is_initialized = True
  
    @tool
    def get_delay_time(target:str)-> float:
        """
        Returns the delay time in seconds for a given target.
        Args:
            target (str): The target host to ping.
        Returns:
            The delay time in seconds.
        """
        import ping3
        # Implement your ping logic here
        delay = ping3.ping(target)
        return delay if delay is not None else float(-1)
    @tool
    def resolve_hostname(ip: str) -> str:
        """
        Resolves IP address to hostname.
        Args:
            ip (str): IP address to resolve
        Returns:
            Hostname or original IP if resolution fails
        """
        import socket
        try:
            hostname = socket.getfqdn(ip)
            if hostname != ip:
                return hostname
            return "Unknown"
        except Exception as e:
            return "Error"
    
    @tool
    def get_local_ip() -> str:
        """
        Gets the local IP address of this machine.
        Returns:
            Local IP address
        """
        import socket
        try:
            # Create a socket that connects to an external server
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Doesn't actually connect, just sets up the socket
            s.connect(('8.8.8.8', 1))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            return socket.gethostbyname(socket.gethostname())
    @tool
    def discover_hosts(subnet_cidr:str) -> list:
        """
        Discovers live hosts on the specified subnet using nmap3's ping scan.

        Args:
            subnet_cidr (str): The target subnet in CIDR notation (e.g., "192.168.1.0/24").

        Returns:
            list: A list of IP addresses of live hosts found, or None if an error occurs.
        """
        import nmap3
        import ipaddress
        import time
        live_hosts = []
        if (subnet_cidr=='127.0.0.0/8'):
            return None
        # Validate subnet format
        try:
            network = ipaddress.ip_network(subnet_cidr, strict=False)
            print(f"[*] Valid subnet provided: {network.with_prefixlen}")
        except ValueError:
            print(f"[!] Error: Invalid subnet format: {subnet_cidr}")
            print("[!] Please use CIDR notation (e.g., 192.168.1.0/24, 10.0.0.0/8).")
            return None

        # --- Initialize nmap3 ---
        # Using NmapHostDiscovery is slightly more semantic for -sn scans
        # Alternatively, you could use nmap = nmap3.Nmap()
        try:
            nmap = nmap3.NmapHostDiscovery()

            print(f"[*] Starting Nmap ping scan on {subnet_cidr}...")
            start_time = time.time()

            # --- Perform the Scan ---
            results = nmap.nmap_no_portscan(subnet_cidr)

            end_time = time.time()
            print(f"[*] Scan completed in {end_time - start_time:.2f} seconds.")

        except nmap3.exceptions.NmapNotInstalledError:
            print("[!] Error: Nmap is not installed or not found in your system's PATH.")
            print("[!] Please install Nmap: https://nmap.org/download.html")
            return None
        except PermissionError: # Catch potential permission issues (common with raw sockets)
            print("[!] Error: Insufficient privileges. Try running this script as root or administrator.")
            return None
        except Exception as e:
            print(f"[!] An unexpected error occurred during the Nmap scan: {e}")
            return None

        # --- Process Results ---
        # nmap3 returns a dictionary. Live hosts usually have a 'state' entry marked 'up'.
        # The keys of the dictionary (excluding metadata like 'stats', 'runtime') are the IPs.
        if not results:
            print("[!] No results returned from Nmap scan.")
            return []

        print("[*] Processing scan results...")
        for ip_address, data in results.items():
            # Skip metadata keys added by nmap3/nmap
            if ip_address in ['stats', 'runtime', 'task_results']:
                continue
            # Check if the host is reported as 'up'
            if isinstance(data, dict) and 'state' in data and data['state'].get('state') == 'up':
                # Optional: Try to get hostname if available in results
                #hostname = ""
                # if 'hostname' in data and isinstance(data['hostname'], list) and data['hostname']:
                #      # Get the first hostname listed
                #      hostname_entry = data['hostname'][0]
                #      if 'name' in hostname_entry and hostname_entry['name']:
                #           hostname = f" ({hostname_entry['name']})"

                live_hosts.append(f"{ip_address}")


        # --- Return Found Hosts ---
        return sorted(live_hosts) # Return sorted list for consistency
    @tool
    def get_all_subnets() -> list:
        """
        Returns the list of all local subnets in CIDR notation.
        
        Returns:
            list: A list of local subnets in CIDR notation (e.g., ['192.168.1.0/24'])
        """
        subnets = set()  # Use a set to avoid duplicates
        
        try:
            # Get all network interfaces
            for iface in netifaces.interfaces():
                # Get address information for the interface
                addrs = netifaces.ifaddresses(iface)
                
                # Check for IPv4 addresses
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr.get('addr')
                        netmask = addr.get('netmask')
                        
                        if ip and netmask:
                            try:
                                # Create network object from IP and netmask
                                network = ipaddress.IPv4Network(f'{ip}/{netmask}', strict=False)
                                subnets.add(str(network))
                            except ValueError as e:
                                print(f"Skipping invalid IP/netmask: {ip}/{netmask} - {e}")
                                
        except Exception as e:
            print(f"Error retrieving subnets: {e}")
            
        return list(subnets)   