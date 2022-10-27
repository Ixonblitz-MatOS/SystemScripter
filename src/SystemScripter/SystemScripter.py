#Ixonblitz-MatOS
import platform
from platform import uname
if(platform.platform().__contains__("Windows")):pass
else: raise OSError("SystemScripter is only compatible with windows(tested on 10)")
import os
import time
try:import netifaces
except ImportError as e:
    if(os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install netifaces")
        import netifaces
    else: raise ImportError from e
try: from psutil import virtual_memory,disk_usage,net_io_counters,net_if_addrs,cpu_count,cpu_freq,cpu_percent,disk_partitions
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install psutil")
        from psutil import virtual_memory,disk_usage,net_io_counters,net_if_addrs,cpu_count,cpu_freq,cpu_percent,disk_partitions
from os import name
try:from wmi import WMI
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install wmi")
        from wmi import WMI
import subprocess
try:from cpuinfo import get_cpu_info
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install py-cpuinfo")
        from cpuinfo import get_cpu_info
from os import getlogin
try:import GPUtil
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install GPUtil")
        import GPUtil
try:from tabulate import tabulate
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install tabulate")
        from tabulate import tabulate
try:from colorama import Fore
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install colorama")
        from colorama import Fore
import socket
import tkinter as tk
from tkinter.messagebox import askyesno
class Prerequisites:
    def get_size(self,bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
class cpu():
    def Cpu(self)->str:
        """
        :return: Full CPU Info
        """
        return get_cpu_info()['brand_raw']
    def CpuBrand(self)->str:
        """
        :return: CPU Brand
        """
        return get_cpu_info()['brand']
    def CpuModel(self)->str:
        """
        :return: CPU Model
        """
        return get_cpu_info()['model']
    def CpuFamily(self)->str:
        """
        :return: CPU Family
        """
        return get_cpu_info()['family']
    def CpuBits(self)->str:
        """
        :return: CPU Bits
        """
        return get_cpu_info()['bits']
    def CpuCount(self)->str:
        """
        :return: CPU Count
        """
        return get_cpu_info()['count']
    def CpuArch(self)->str:
        """
        :return: CPU Architecture
        """
        return get_cpu_info()['raw_arch_string']
    def CpuL1InstructionCache(self)->str:
        """
        :return: CPU L1 Instruction Cache size
        """
        return get_cpu_info()['l1_instruction_cache_size']
    def CpuL1dataCache(self)->str:
        """
        :return: CPU L1 data cache size
        """
        return get_cpu_info()['l1_data_cache_size']
    def CpuL2Cache(self)->str:
        """
        :return: CPU L2 Data Cache Size
        """
        return get_cpu_info()['l2_cache_size']
    def CpuL3Cache(self)->str:
        """
        CPU L3 Data Cache Size
        :return:
        """
        return get_cpu_info()['l3_cache_size']
    def CpuCorePhysical(self)->int:
        """
        :return: physical core count
        """
        return cpu_count(logical=False)
    def CpuCoreLogical(self)->int:
        """
        :return: logical core count
        """
        return cpu_count(logical=True)
    def CpuCurrentFrequency(self)->float:
        """
        :return: returns current frequency
        """
        return cpu_freq().current
    def CpuMinFrequency(self)->float:
        """
        :return: returns Minimum Frequency
        """
        return cpu_freq().min
    def CpuMaxFrequency(self)->float:
        """
        :return: returns Max Frequency
        """
        return cpu_freq().max
    def CpuCurrentUtil(self)->float:
        """
        :return: Current CPU current utilization
        """
        return cpu_percent(interval=1)
    def CpuPerCurrentUtil(self)->float:
        """
        :return: Current Per CPU utilization
        """
        return cpu_percent(interval=1, percpu=True)
class ram():
    def TotalRam(self,bytes:bool)->float:
        """
        :return: Memory Size
        """
        if bytes == None:
            return virtual_memory().total
        elif bytes:
            return virtual_memory().total
        else:
            return round(virtual_memory().total/1000000000, 2)
    def AvailableRam(self, bytes:bool)->float:
        """
        :return: Available Ram
        """
        if bytes == None:
            return virtual_memory().available
        elif bytes:
            return virtual_memory().available
        else:
            return round(virtual_memory().available / 1000000000, 2)
    def UsedRam(self,bytes:bool)->float:
        """
        :return: Used Ram
        """
        if bytes == None:
            return virtual_memory().used
        elif bytes:
            return virtual_memory().used
        else:
            return round(virtual_memory().used/1000000000, 2)
    def UsedRamPercentage(self)->float:
        """
        :return: Ram Percentage
        """
        return virtual_memory().percent
class NetworkOptions:
    NAME="NAME"
    ADDRESS="ADDRESS"
    NETMASK="NETMASK"
    BROADCAST="BROADCAST"
    BYTESSENT="BYTESSENT"
    BYTESRECEIVED="BYTESRECIEVED"
    ALL="ALL"
class Network:
    def NetInfo(self,options:str,tab:bool)->str | tuple:
        """
        :parameter tab: Tabulate if True
        :return: all network info separated in vars
        """
        if_addrs = net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            global address
            for address in interface_addresses:
                pass
                if str(address.family) == 'AddressFamily.AF_INET':
                    pass
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                   pass
            global net_io
            net_io = net_io_counters()
            if options == None or options == NetworkOptions.ALL:
                if tab:
                    tabArr = []
                    tabArr.append(interface_name)
                    tabArr.append(address.address)
                    tabArr.append(address.netmask)
                    tabArr.append(address.broadcast)
                    s = Prerequisites()
                    tabArr.append(Prerequisites.get_size(s,net_io.bytes_sent))
                    tabArr.append(Prerequisites.get_size(s,net_io.bytes_recv))
                    return(tabulate(tabArr,headers=("Name","Address","Netmask","Broadcast","Bytes Sent","Bytes Received")))
                else:
                    s = Prerequisites()
                    return (interface_name, address.address, address.netmask, address.broadcast,
                        Prerequisites.get_size(s,net_io.bytes_sent), Prerequisites.get_size(s,net_io.bytes_recv))
            elif options == NetworkOptions.NAME:
                if tab:
                    return(tabulate(interface_name,headers="Name"))
                else:
                    return interface_name
            elif options == NetworkOptions.NETMASK:
                if tab:
                    return(tabulate(address.netmask,headers="Netmask"))
                else:
                    return address.netmask
            elif options == NetworkOptions.ADDRESS:
                if tab:
                    return(tabulate(address.address,headers="Address"))
                else:
                    return address.address
            elif options == NetworkOptions.BROADCAST:
                if tab:
                    return(tabulate(address.broadcast,headers="Broadcast"))
                else:
                    return address.broadcast
            elif options == NetworkOptions.BYTESSENT:
                if tab:
                    s = Prerequisites()
                    return(tabulate(Prerequisites.get_size(s,net_io.bytes_sent), headers="Bytes Sent"))
                else:
                    s = Prerequisites()
                    return Prerequisites.get_size(s,net_io.bytes_sent)
            elif options == NetworkOptions.BYTESRECEIVED:
                if tab:
                    s = Prerequisites()
                    return(tabulate(Prerequisites.get_size(s,net_io.bytes_recv), headers="Bytes Received"))
                else:
                    s = Prerequisites()
                    return Prerequisites.get_size(s,net_io.bytes_recv)
            else:
                if tab:
                    tabArr = []
                    tabArr.append(interface_name)
                    tabArr.append(address.address)
                    tabArr.append(address.netmask)
                    tabArr.append(address.broadcast)
                    s = Prerequisites()
                    tabArr.append(Prerequisites.get_size(s,net_io.bytes_sent))
                    tabArr.append(Prerequisites.get_size(s,net_io.bytes_recv))
                    return(tabulate(tabArr,headers=("Name","Address","Netmask","Broadcast","Bytes Sent","Bytes Received")))
                else:
                    s = Prerequisites()
                    return (interface_name, address.address, address.netmask, address.broadcast,
                        Prerequisites.get_size(s,net_io.bytes_sent), Prerequisites.get_size(s,net_io.bytes_recv))
    def GetIP(self)->str:
        """
        :return: gets IP NO CIDR
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = (s.getsockname()[0])
        return ip
    def GetDefault(self)->str:
        """
        :return: default gateway
        """
        gateways = netifaces.gateways()
        default_gateway = gateways['default'][netifaces.AF_INET][0]
        return default_gateway
class StorageOptions():
    DEVICE="DEVICE"
    TOTAL="TOTAL"
    USED="USED"
    FREE="FREE"
    PERCENT="PERCENT"
    FSTYPE="FSTYPE"
    MOUNTPOINT="MOUNTPOINT"
    ALL="ALL"
class Storage:
    def StorageSize(self,DriveLetter)->int:
        """
        :return: Storage Size of Designated Drive
        """
        if DriveLetter == None:
            return disk_usage(f'C:/').total
        else:
            return disk_usage(f'{DriveLetter}/').total
    def get_disk_info(self, options:str)->str|int|float|list:
        """
        :return: Disk Info {Device, Total, Used, Free, Percent, FSType, Mountpoint}
        """
        disk_info = []
        for part in disk_partitions(all=False):
            if name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            usage = disk_usage(part.mountpoint)
            disk_info.append({
                'device':  part.device,
                'total':  usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent,
                'fstype': part.fstype,
                'mountpoint': part.mountpoint
            })
        if options == StorageOptions.ALL: return disk_info
        elif options == StorageOptions.FREE: return disk_info[0]['free']
        elif options == StorageOptions.USED: return disk_info[0]['used']
        elif options == StorageOptions.TOTAL: return disk_info[0]['total']
        elif options == StorageOptions.DEVICE: return disk_info[0]['device']
        elif options == StorageOptions.FSTYPE: return disk_info[0]['fstype']
        elif options == StorageOptions.MOUNTPOINT: return disk_info[0]['mountpoint']
        elif options == StorageOptions.PERCENT: return disk_info[0]['percent']
        else: return disk_info
class GPUOptions:
    IDONLY="IDONLY"
    NAMEONLY="NAMEONLY"
    LOADONLY="LOADONLY"
    FREEMEMONLY="FREEMEMONLY"
    USEDMEMONLY="USEDMEMONLY"
    TOTALMEMONLY="TOTALMEMONLY"
    TEMPONLY="TEMPONLY"
    SHOWALL="SHOWALL"
class GPUExceptions(Exception):
    def _err(GPUExceptions,message):
        print(Fore.RED,message)
        quit()
    def WrongType(GPUExceptions):
        GPUExceptions._err("Wrong type provided")
class GPU:
    def GPUInfo(self, options:str, tab:bool)->str|list:
        """
        :return: tabulated info or diff by options
        """
        if(type(options) == None): options = GPUOptions.SHOWALL
        elif(type(options) != GPUOptions):
            z=GPUExceptions()
            GPUExceptions.WrongType(z)
        elif options == GPUOptions.SHOWALL:
            gpus = GPUtil.getGPUs()
            list_gpus = []
            for gpu in gpus:
                gpu_id = gpu.id
                gpu_name = gpu.name
                gpu_load = f"{gpu.load * 100}%"
                gpu_free_memory = f"{gpu.memoryFree}MB"
                gpu_used_memory = f"{gpu.memoryUsed}MB"
                gpu_total_memory = f"{gpu.memoryTotal}MB"
                gpu_temperature = f"{gpu.temperature} °C"
                gpu_uuid = gpu.uuid
                list_gpus.append((
                    gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                    gpu_total_memory, gpu_temperature, gpu_uuid
                ))
            if tab:
                return(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                "temperature", "uuid")))
            else:
                return list_gpus
        elif options == GPUOptions.IDONLY:
            gpus = GPUtil.getGPUs()
            list_gpus = ""
            for gpu in gpus:
                gpu_id = gpu.id
                list_gpus = gpu_id
            if tab:
                return(tabulate(list_gpus,headers=("id")))
            else:
                return list_gpus
        elif options == GPUOptions.NAMEONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_name = gpu.name
                list_gpu = gpu_name
            if tab:
                return(tabulate(list_gpu,headers="name"))
            else:
                return list_gpu
        elif options == GPUOptions.TEMPONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_temp = gpu.temperature
                list_gpu = gpu_temp
            if tab:
                return(tabulate(list_gpu,headers="Temperature"))
            else:
                return list_gpu
        elif options == GPUOptions.LOADONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_load = gpu.load
                list_gpu = gpu_load
            if tab:
                return(tabulate(list_gpu,headers="Load"))
            else:
                return list_gpu
        elif options == GPUOptions.FREEMEMONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_freemem = gpu.memoryFree
                list_gpu = gpu_freemem
            if tab:
                return(tabulate(list_gpu,headers="Free Memory"))
            else:
                return list_gpu
        elif options == GPUOptions.TOTALMEMONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_total = gpu.memoryTotal
                list_gpu = gpu_total
            if tab:
                return(tabulate(list_gpu,headers="Total Memory"))
            else:
                return list_gpu
        elif options == GPUOptions.USEDMEMONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_used = gpu.memoryUsed
                list_gpu = gpu_used
            if tab:
                return(tabulate(list_gpu,headers="Used Memory"))
            else:
                return list_gpu
        else:
            gpus = GPUtil.getGPUs()
            list_gpus = []
            for gpu in gpus:
                gpu_id = gpu.id
                gpu_name = gpu.name
                gpu_load = f"{gpu.load * 100}%"
                gpu_free_memory = f"{gpu.memoryFree}MB"
                gpu_used_memory = f"{gpu.memoryUsed}MB"
                gpu_total_memory = f"{gpu.memoryTotal}MB"
                gpu_temperature = f"{gpu.temperature} °C"
                gpu_uuid = gpu.uuid
                list_gpus.append((
                    gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                    gpu_total_memory, gpu_temperature, gpu_uuid
                ))
            if tab:
                return (tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                                     "temperature", "uuid")))
            else:
                return list_gpus
class WindowsCommands:
    def Shutdown(self,force:bool=False)->None:
        """
        :param force: Force Shutdown
        :return: None
        """
        if force:os.system("shutdown –s –f")
        else:os.system("shutdown /s /t 1")
    def Restart(self,force:bool=False)->None:
        """
        :param force: Force Restart
        :return: None
        """
        if force:os.system("shutdown –r –f")
        else:os.system("shutdown /r /t 1")
    def Start(self,Path:str)->None:
        """
        :param Path: Path of file to start
        :return: None
        """
        os.system(f"start {Path}")
class OSoptions:
    OSNAME="OSNAME"
    RELEASE="RELEASE"
    ALL="ALL"
def OS(options:str,tab:bool)->str|tuple:
    """
    :return: Operating System Information
    """
    import platform
    if options == OSoptions.OSNAME:
        return platform.system()
    elif options == OSoptions.RELEASE:
        return platform.release()
    elif options == OSoptions.ALL or options == None:
        if tab:
            final = [platform.system(),platform.release()]
            return(tabulate(final,headers=("Operating System", "Release Number")))
        else:
            return (platform.system(),platform.release())
def Motherboard_Name()->str:
    """
    :return: Motherboard model name
    """
    s=subprocess.Popen(['wmic', 'baseboard','get','product'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = s.communicate()
    return out.__str__().split("\n")[0].split(r"\n")[1].split(r"\\r")[0].replace(r"\r","")
def Motherboard_Manufacturer()->str:
    """
    :return:Motherboard Manufacturer
    """
    s=subprocess.Popen(['wmic','baseboard','get','Manufacturer'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=s.communicate()
    return out.__str__().split("\n")[0].split(r"\n")[1].split(r"\\r")[0].replace(r"\r","")
def Motherboard_Serial()->str:
    """
    :return: Motherboard Serial Number
    """
    s=subprocess.Popen(['wmic','baseboard','get','serialnumber'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=s.communicate()
    return out.__str__().split("\n")[0].split(r"\n")[1].split(r"\\r")[0].replace(r"\r", "")
def Motherboard_Version()->str:
    """
       :return: Motherboard Version
       """
    s = subprocess.Popen(['wmic', 'baseboard', 'get', 'version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = s.communicate()
    return out.__str__().split("\n")[0].split(r"\n")[1].split(r"\\r")[0].replace(r"\r", "")
def SystemName()->str:
    """
    :return: PC NAME
    """
    return uname().node
def ActiveUser()->str:
    """
    :return: Gets the Active user
    """
    return getlogin()
def Change_Computer_Name(NewName:str,username:str,password:str,RestartPreference:bool=None)->None:
    c = WMI()
    for system in c.Win32_ComputerSystem():
        system.Rename(NewName, username, password)
    r=tk.Tk()
    r.withdraw()
    if RestartPreference == None:pass
    else:
        if(RestartPreference):
            os.system("shutdown /r /t 1")
        elif not RestartPreference:
            return
        else:pass
    if(askyesno(title="Restart Required",message="The PC has been renamed and needs to restart to apply")==tk.YES):
        os.system("shutdown /r /t 1")
    else:
        r.destroy()
        return
    r.mainloop()