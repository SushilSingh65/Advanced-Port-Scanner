# main.py
import concurrent.futures
from colorama import init, Fore, Style
from scanner_core import run_scan, get_ip_from_domain, open_ports, closed_ports, reset_results

init(autoreset=True)

GREEN = Fore.GREEN
RED = Fore.RED
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
RESET = Style.RESET_ALL

BANNER = r"""
 ____   ___  ____ _____   ____   ____    _    _   _ _   _ ___ _   _  ____ 
|  _ \ / _ \|  _ \_   _| / ___| / ___|  / \  | \ | | \ | |_ _| \ | |/ ___|
| |_) | | | | |_) || |   \___ \| |     / _ \ |  \| |  \| || ||  \| | |  _ 
|  __/| |_| |  _ < | |    ___) | |___ / ___ \| |\  | |\  || || |\  | |_| |
|_|___ \___/|_|_\_\|_|   |____/ \____/_/   \_\_| \_|_| \_|___|_| \_|\____|
"""


# Get user input
def get_input():
    print(f"{CYAN}{BANNER}{RESET}")
    print(f"{CYAN}Welcome to the Advanced Interactive Port Scanner 🔍{RESET}")

    ip = None
    while not ip:
        target = input(f"{YELLOW}Enter target IP/domain: {RESET}")
        if not target.strip():
            print(f"{RED}[!] Please enter a valid target.{RESET}")
            continue
        ip = get_ip_from_domain(target)
        if not ip:
            print(f"{RED}[!] Could not resolve domain '{target}'. Please try again.{RESET}")

    port_input = input(f"{YELLOW}Enter port range (default is 1-1000): {RESET}")
    if not port_input.strip():
        ports = range(1, 1001)
    else:
        try:
            start, end = map(int, port_input.split('-'))
            ports = range(start, end + 1)
        except:
            print(f"{RED}[!] Invalid port range. Use format like 20-80.{RESET}")
            return get_input()

    scan_type = input(f"{YELLOW}Choose scan type (connect / syn): {RESET}").strip().lower()
    if scan_type not in ["connect", "syn"]:
        print(f"{RED}[!] Invalid scan type. Defaulting to 'connect'.{RESET}")
        scan_type = "connect"

    return ip, ports, scan_type

# Print results
def print_results():
    print("\n" + "=" * 60)
    print(f"{CYAN}[+] Scan complete.{RESET}")
    print("=" * 60)

    print(f"\n{GREEN}[OPEN PORTS]{RESET}")
    if open_ports:
        for port, service, banner in open_ports:
            print(f"{GREEN}Port {port} ({service}) - Banner: {banner if banner else 'No banner'}{RESET}")
    else:
        print("No open ports found.")

    print(f"\n{RED}[CLOSED PORTS]{RESET}")
    if closed_ports:
        for port in closed_ports:
            print(f"{RED}Port {port} - Closed{RESET}")
    else:
        print("All ports are open? Hmm... unlikely.")

# Main loop
def main():
    while True:
        ip, ports, scan_type = get_input()

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            run_scan(ip, ports, scan_type, executor)

        print_results()

        again = input(f"\n{YELLOW}Press 'Enter' to scan another IP, or 'E' to exit: {RESET}").lower()
        if again == 'e':
            print(f"{CYAN}Exiting Port Scanner...{RESET}")
            break
        else:
            reset_results()

if __name__ == "__main__":
    main()
