import psutil


def list_processes():
    for process in psutil.process_iter(attrs=['pid', 'name', 'status']):
        try:
            process_info = process.info
            print(f"PID: {process_info['pid']}, Name: {process_info['name']}, Status: {process_info['status']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


if __name__ == "__main__":
    print("List of running processes:")
    list_processes()
