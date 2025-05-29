import socket
import threading
import queue

print_lock = threading.Lock()

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        with print_lock:
            if result == 0:
                print(f"[+] Port {port} is open on {target}")
        sock.close()
    except Exception as e:
        pass

def worker(target, q):
    while not q.empty():
        port = q.get()
        scan_port(target, port)
        q.task_done()

def main():
    target = input("Enter target IP or hostname: ").strip()
    port_start = 1
    port_end = 1024

    q = queue.Queue()

    for port in range(port_start, port_end + 1):
        q.put(port)

    thread_count = 100
    threads = []

    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(target, q))
        t.start()
        threads.append(t)

    q.join()

    for t in threads:
        t.join()

    print("Scanning completed.")

if __name__ == "__main__":
    main()
