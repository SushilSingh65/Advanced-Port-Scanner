# scanner_core.py
import socket
import threading

open_ports = []
closed_ports = []
lock = threading.Lock()

# Resolve domain to IP
def get_ip_from_domain(domain):
    try:
        ip_list = socket.gethostbyname_ex(domain)[2]
        return ip_list[0]
    except socket.gaierror:
        return None

# Grab service banner
def grab_banner(ip, port):
    try:
        with socket.socket() as s:
            s.settimeout(1)
            s.connect((ip, port))
            return s.recv(1024).decode().strip()
    except:
        return None

# Port scanner
def scan_port(ip, port, scan_type):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))

            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Unknown"
                banner = grab_banner(ip, port)
                with lock:
                    open_ports.append((port, service, banner))
            else:
                with lock:
                    closed_ports.append(port)
    except:
        pass

# Run the scan with concurrency
def run_scan(target, ports, scan_type, executor):
    for port in ports:
        executor.submit(scan_port, target, port, scan_type)

# Reset results
def reset_results():
    global open_ports, closed_ports
    open_ports.clear()
    closed_ports.clear()
