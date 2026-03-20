import psutil


def get_cpu():
    return psutil.cpu_percent(interval=1)


def get_memory():
    memory = psutil.virtual_memory()
    return memory.percent


def get_disk():
    disk = psutil.disk_usage("/")
    return disk.percent


def main():
    cpu = get_cpu()
    memory = get_memory()
    disk = get_disk()

    print(f"CPU (процессор): {cpu}%")
    print(f"RAM (оперативная память): {memory}%")
    print(f"Disk (диск): {disk}%")


if __name__ == "__main__":
    main()