import platform
import psutil
import GPUtil
import subprocess
import os
import uuid
import base64

def get_total_memory_size():
    memory_info = psutil.virtual_memory()
    return (memory_info.total/(2**(10*3)))

def get_system_info():
    #print("System Information:")
    system_info = platform.uname()
    ans={}
    ans['system'] = f"{system_info.system}"
    ans['node_name'] = f"{system_info.node}"
    ans['release'] = f"{system_info.release}"
    ans['version'] = f"{system_info.version}"
    ans['machine'] = f"{system_info.machine}"
    ans['processor'] = f"{system_info.processor}"
    return ans

def get_cpu_info():
    cpu_info = platform.processor()
    cpu_count = psutil.cpu_count(logical=False)
    logical_cpu_count = psutil.cpu_count(logical=True)

    #print("\nCPU Information:")
    ans = {}
    ans['processor'] = f"{cpu_info}"
    ans['physical_cores'] = f"{cpu_count}"
    ans['logical_cores'] = f"{logical_cpu_count}"
    return ans

def get_memory_info():
    memory_info = psutil.virtual_memory()

    #print("\nMemory Information: Unit : bytes")
    ans={}
    ans['total_memory'] = f"{memory_info.total}"
    ans['available_memory'] = f"{memory_info.available}"
    ans['used_memory'] = f"{memory_info.used}"
    ans['memory_utilization'] = f"{memory_info.percent:.2f}%"
    return ans

def get_disk_info():
    disk_info = psutil.disk_usage('/')

    #print("\nDisk Information: Unit : bytes")
    ans={}
    ans['total_disk_space'] = f"{disk_info.total}"
    ans['used_disk_space'] = f"{disk_info.used}"
    ans['free_disk_space'] = f"{disk_info.free}"
    ans['disk_space_utilization'] = f" {disk_info.percent:.2f}%"

#Only Nvidia GPU on Windows and Linux
def get_gpu_info():    

    ans={}
    if (get_system_info()['system']=='Darwin'):
        ans['0'] = "no_gpu"
        return ans
    else:
        gpus = GPUtil.getGPUs()
    
    if not gpus:
        print("\nNo GPU detected.")
        ans['0'] = "no_gpu"
    else:
        ans['0'] = "there_is_gpu"

        for i, gpu in enumerate(gpus):
            #print(f"\nGPU {i + 1} Information:")
            ans[f'{i+1}'] = {}
            ans[f'{i+1}']['id'] = f"{gpu.id}"
            ans[f'{i+1}']['name'] = f"{' '.join(gpu.name.splitlines())}"
            ans[f'{i+1}']['driver'] = f"{gpu.driver}"
            ans[f'{i+1}']['gpu_memory_total'] = f"{gpu.memoryTotal} MB"
            ans[f'{i+1}']['gpu_memory_free'] = f"{gpu.memoryFree} MB"
            ans[f'{i+1}']['gpu_memory_used'] = f"{gpu.memoryUsed} MB"
            ans[f'{i+1}']['gpu_load'] = f"{gpu.load*100}%"
            ans[f'{i+1}']['gpu_temperature'] = f"{gpu.temperature}°C"
    
    return ans

def check_windows_shell():
    parent_pid = os.getppid()
    shell_name = psutil.Process(parent_pid).name().lower()
    if 'cmd' in shell_name:
        return 'CMD'
    elif 'powershell' in shell_name:
        return 'PowerShell'
    else:
        return 'Unknown'


def get_extra():
    system_info = platform.uname()
    ans={}
    ans['system'] = f"{system_info.system}"
    ans['memory'] = get_total_memory_size()
    ans['cpu'] = f"unknown"
    ans['gpu'] = f"unknown"
    ans['os_version'] = f"unknown"

    try:
        if(system_info.system=='Darwin'):
            ans['system_name'] = "macOS"

            print('----------Apple Mac---------')
            r1 = subprocess.run(['system_profiler', 'SPHardwareDataType'],capture_output=True,text=True)
            #ans['hardware'] = f"{r1.stdout}"
            for line in r1.stdout.split('\n'):
                if('Model Identifier' in line):
                    ans['model']=f"{line[24:]}"
                    

            for line in r1.stdout.split('\n'):
                if ('Chip' in line):
                    ans['cpu']=f"{line[12:]}"
            
            if(ans['cpu'].startswith('Apple')):
                ans['gpu'] = ans['cpu']
            else:
                ans['gpu'] = 'no_gpu'
            
            #r2 = subprocess.run(['system_profiler', 'SPDisplaysDataType'],capture_output=True,text=True)
            #ans['display'] = f"{r2.stdout}"
            r3 = subprocess.run(['system_profiler', 'SPSoftwareDataType'],capture_output=True,text=True)
            #ans['software'] = f"{r3.stdout}"

            for line in r3.stdout.split('\n'):
                if ('System Version' in line):
                    ans['os_version']=f"{line[22:]}"
            return ans
        elif(system_info.system=='Linux'):
            ans['system_name'] = "Linux"

            print('-------Linux----------')

            try:     
                r2 = subprocess.run(['lsb_release','-a'],capture_output=True,text=True)
                software = f"{r2.stdout}"
                for line in software.split('\n'):
                    if ('Description' in line):
                        ans['os_version']=f"{line[12:]}".strip()
            except:
                r2 = subprocess.run(['cat','/etc/os-release'],capture_output=True,text=True)
                software = f"{r2.stdout}"
                for line in software.split('\n'):
                    if ('PRETTY_NAME' in line):
                        ans['os_version']=f"{line[12:]}".strip()
            
            try:
                r1 = subprocess.run(['lshw','-C','cpu'],capture_output=True,text=True)
                for line in r1.stdout.split('\n'):
                    if ('product' in line):
                        ans['cpu']=f"{line[16:]}"
            except:
                cmd = ['lscpu']
                ps = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                cmd = ['grep', 'Model name']
                grep = subprocess.Popen(cmd, stdin=ps.stdout, stdout=subprocess.PIPE,
                        encoding='utf-8')
                ps.stdout.close()
                output, _ = grep.communicate()
                python_processes = output.split('\n')
                ans['cpu'] = python_processes[0][16:].strip() 

            if (get_gpu_info()['0']=='no_gpu'):
                try:
                    r2 = subprocess.run(['lshw','-C','display'],capture_output=True,text=True)
                    for line in r2.stdout.split('\n'):
                        if ('product' in line):
                            ans['gpu']=f"{line[16:]}"
                except:
                    ans['gpu']="no_gpu"
            else :
                print(f"{get_gpu_info()['1']}")
                try:
                     print(get_gpu_info()['2'])
                     print('At least two GPU cards')
                except:
                     print('Only one GPU card')
                #List only the first gpu name
                ans['gpu']=get_gpu_info()['1']['name']

                                        
            return ans
            
        elif(system_info.system=='Windows'):
            ans['system_name'] = "Windows"

            prefix_exe='powershell.exe'
            #print("Python is running in:", check_windows_shell(), "on Windows")
            ans['run_in'] = f"{check_windows_shell()}"           
                        
            r1 = subprocess.run([prefix_exe,'Get-WmiObject','Win32_Processor'],capture_output=True,text=True)
            #print(r1.stdout)
            r_cpu = subprocess.run([prefix_exe,'(Get-WmiObject Win32_Processor).Name'],capture_output=True,text=True)
            #print(r_cpu.stdout)
            ans['cpu']=r_cpu.stdout.strip()
            r2 = subprocess.run([prefix_exe,'Get-WmiObject','Win32_PhysicalMemory'],capture_output=True,text=True)
            #print(r2.stdout)
            r3 = subprocess.run([prefix_exe,'Get-WmiObject','Win32_VideoController'],capture_output=True,text=True)
            #print(r3.stdout)
            r_gpu = subprocess.run([prefix_exe,'(Get-WmiObject Win32_VideoController).Caption'],capture_output=True,text=True)
            str_gpu = r_gpu.stdout.strip()
            str_gpu = ' '.join(str_gpu.splitlines())
            #print(r_gpu)
            ans['gpu'] = str_gpu
            r4 = subprocess.run([prefix_exe,'(Get-WmiObject Win32_OperatingSystem).Caption'],capture_output=True,text=True)
            #print(r4.stdout)
            ans['os_version'] = f"{r4.stdout}"
        
        return ans

    except:
        print("error! when retrieving os_version, cpu, or gpu !")
    
    return ans

def get_uuid():
    sys_info = get_extra()
    system_name = sys_info['system_name']
    cpu = sys_info['cpu']
    gpu  = sys_info['gpu']
    memory = f"{sys_info['memory']:.2f}"

    id_str = f"{system_name}|{cpu}|{gpu}|{memory}"
    #print(id_str)
    uuid5 = uuid.uuid5(uuid.NAMESPACE_X500, id_str)
    return uuid5    

if __name__ == "__main__":
    #sysinfo = get_extra()
    uuid5 = get_uuid()
    print("UUID version 5:", uuid5)
    

