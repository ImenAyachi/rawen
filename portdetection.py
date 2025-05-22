import socket
import threading

# Dictionnaire des descriptions de ports
port_descriptions = {
    20: "FTP Data Transfer",
    21: "FTP Control",
    22: "SSH - Secure Shell",
    23: "Telnet",
    25: "SMTP - Email Sending",
    53: "DNS - Domain Name Resolution",
    80: "HTTP - Web Traffic",
    110: "POP3 - Email Retrieval",
    143: "IMAP - Email Retrieval",
    443: "HTTPS - Secure Web Traffic",
    3306: "MySQL Database",
    5432: "PostgreSQL Database",
    6379: "Redis",
    8080: "HTTP (Alternative)",
    8443: "HTTPS (Alternative)",
    27017: "MongoDB",
    5060: "SIP - VoIP",
    8081: "HTTP (Alternative)",
    8888: "HTTP (Jupyter / Dev)",
    9000: "Web App / Dev",
    9999: "Service / Dev",
    2049: "NFS - File Sharing",
    6000: "X11 - GUI",
    8088: "HTTP (Alt Admin)"
}

def is_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False

def scan_ports(target, num_ports=1000):
    open_ports = []

    try:
        target_ip = target if is_ip(target) else socket.gethostbyname(target)
    except:
        return [("Error", "Invalid IP or domain", "")]

    def get_banner(s):
        try:
            return s.recv(1024).decode().strip()
        except:
            return "No banner"

    def scan_port(ip, port):
        try:
            s = socket.socket()
            s.settimeout(3)
            s.connect((ip, port))
            banner = get_banner(s)
            description = port_descriptions.get(port, "Unknown service")
            open_ports.append((port, banner, description))
            s.close()
        except:
            pass

    threads = []
    for port in range(1, num_ports + 1):
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sorted(open_ports)
