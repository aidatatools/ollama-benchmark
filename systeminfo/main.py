import platform
import psutil
import GPUtil
import subprocess
import os

def get_total_memory_size():
    memory_info = psutil.virtual_memory()
    return (memory_info.total/(2**(10*3)))


system_info = platform.uname()

print("System Information:")
print(f"System: {system_info.system}")
print(f"Node Name: {system_info.node}")
print(f"Release: {system_info.release}")
print(f"Version: {system_info.version}")
print(f"Machine: {system_info.machine}")
print(f"Processor: {system_info.processor}")

cpu_info = platform.processor()
cpu_count = psutil.cpu_count(logical=False)
logical_cpu_count = psutil.cpu_count(logical=True)

print("\nCPU Information:")
print(f"Processor: {cpu_info}")
print(f"Physical Cores: {cpu_count}")
print(f"Logical Cores: {logical_cpu_count}")

memory_info = psutil.virtual_memory()

print("\nMemory Information:")
print(f"Total Memory: {memory_info.total} bytes")
print(f"Available Memory: {memory_info.available} bytes")
print(f"Used Memory: {memory_info.used} bytes")
print(f"Memory Utilization: {memory_info.percent}%")

disk_info = psutil.disk_usage('/')

print("\nDisk Information:")
print(f"Total Disk Space: {disk_info.total} bytes")
print(f"Used Disk Space: {disk_info.used} bytes")
print(f"Free Disk Space: {disk_info.free} bytes")
print(f"Disk Space Utilization: {disk_info.percent}%")

gpus = GPUtil.getGPUs()

if not gpus:
    print("\nNo GPU detected.")
else:
    for i, gpu in enumerate(gpus):
        print(f"\nGPU {i + 1} Information:")
        print(f"ID: {gpu.id}")
        print(f"Name: {gpu.name}")
        print(f"Driver: {gpu.driver}")
        print(f"GPU Memory Total: {gpu.memoryTotal} MB")
        print(f"GPU Memory Free: {gpu.memoryFree} MB")
        print(f"GPU Memory Used: {gpu.memoryUsed} MB")
        print(f"GPU Load: {gpu.load * 100}%")
        print(f"GPU Temperature: {gpu.temperature}°C")


def check_windows_shell():
    parent_process = psutil.Process(os.getppid()).name().lower()
    if 'cmd' in parent_process:
        return 'Command Prompt'
    elif 'powershell' in parent_process:
        return 'PowerShell'
    else:
        return 'Unknown'

try:
    if(system_info.system=='Darwin'):
        print('\n----------Apple Mac---------')
        r1 = subprocess.run(['system_profiler', 'SPHardwareDataType'],capture_output=True,text=True)
        print(r1.stdout)
        r2 = subprocess.run(['system_profiler', 'SPDisplaysDataType'],capture_output=True,text=True)
        print(r2.stdout)
        r3 = subprocess.run(['system_profiler', 'SPSoftwareDataType'],capture_output=True,text=True)
        print(r3.stdout)
    elif(system_info.system=='Linux'):
        print('\n-------Linux----------')
        r1 = subprocess.run(['lshw'],capture_output=True,text=True)
        print(r1.stdout)
        r2 = subprocess.run(['lsb_release','-a'],capture_output=True,text=True)
        print(r2.stdout)
    elif(system_info.system=='Windows'):
        
        prefix_exe='powershell.exe'
        print("\nPython is running in:", check_windows_shell())

        r1 = subprocess.run([prefix_exe,'Get-WmiObject','Win32_Processor'],capture_output=True,text=True)
        print(r1.stdout)
        r2 = subprocess.run([prefix_exe,'Get-WmiObject','Win32_PhysicalMemory'],capture_output=True,text=True)
        print(r2.stdout)
        r3 = subprocess.run([prefix_exe,'Get-WmiObject','Win32_VideoController'],capture_output=True,text=True)
        print(r3.stdout)
        r4 = subprocess.run([prefix_exe,'(Get-WmiObject Win32_OperatingSystem).Caption'],capture_output=True,text=True)
        print(r4.stdout)


except:
    print("error!")
