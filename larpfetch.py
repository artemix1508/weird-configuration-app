import sys
import json #for reading logo ascii arts
import subprocess #to run commands, needed for detection of software and hardware
import os
import rich #to color print statemets
from rich.columns import Columns
from rich.text import Text
import getpass
import socket

username = getpass.getuser()

hostname = socket.gethostname()

user_host_format = f"{username}@{hostname}"

def get_gpu_info():
    result = subprocess.run(["lspci"], capture_output=True, text=True)
    output = result.stdout

    gpus = []

    for line in output.splitlines():
        if "VGA" in line:
            if "NVIDIA" in line:
                model = line.split('[')[-1].split(']')[0]
                gpus.append({'Vendor': 'NVIDIA', 'Model': model})
            elif "AMD" in line:
                model = line.split('[')[-1].split(']')[0]
                gpus.append({'Vendor': 'AMD', 'Model': model})
            elif "Intel" in line:
                model = line.split('[')[-1].split(']')[0]
                gpus.append({'Vendor': 'Intel', 'Model': model})
            pass
    return gpus

def get_de():
    desktop = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION")

    if desktop:
        return desktop
    return "Unknown"

def get_cpu_info():
    cpu_result = subprocess.run(["lscpu"], capture_output=True, text=True)
    cpu_output = cpu_result.stdout

    cpu = ""

    for line in cpu_output.splitlines():
        if "Model name" in line:
            model = line.split(':')[-1].strip()
            cpu = model
    return cpu

def get_distro_info():
    if not os.path.exists('/etc/os-release'):
        return None

    info = {}

    with open('/etc/os-release') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                info[key] = value
    return info

if getattr(sys, '_MEIPASS', None):
    logos_path = os.path.join(sys._MEIPASS, "logos.json")
else:
    logos_path = "logos.json"

with open(logos_path) as f:
    logos = json.load(f)

distro_info = get_distro_info()
distro_name = distro_info.get('ID', '').strip('"')
pretty_distro_name = distro_info.get('PRETTY_NAME', '').strip('"')
gpu_info = get_gpu_info()
cpu_info = get_cpu_info()
desktop_environment = get_de()

logo_data = logos.get(distro_name, "")
if isinstance(logo_data, list):
    logo_str = "\n".join(logo_data)
else:
    logo_str = logo_data

subprocess.run(["clear"])

info_text = Text()

info_text.append(f"{username}", style="bold cyan")
info_text.append("@", style="bold white")
info_text.append(f"{hostname}\n", style="bold cyan")

header_length = len(user_host_format)
info_text.append(f"{'-' * header_length}\n")

distro_display = pretty_distro_name
info_text.append("Distribution: ", style="bold cyan")
info_text.append(f"{distro_display}\n")

info_text.append("Desktop environment: ", style="bold cyan")
info_text.append(f"{desktop_environment}\n")

info_text.append("CPU: ", style="bold cyan")
info_text.append(f"{cpu_info}\n")

for i, gpu in enumerate(gpu_info, start=1):
    info_text.append(f"GPU{i}: ", style="bold cyan")
    info_text.append(f"{gpu['Vendor']}")
    info_text.append(", ")
    info_text.append(f"{gpu['Model']}\n")

logo_text = Text(logo_str, style="bold cyan")

rich.print(Columns([logo_text, info_text], padding=4))
