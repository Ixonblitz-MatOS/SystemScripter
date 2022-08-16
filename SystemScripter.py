#Ixonblitz-MatOS
import netifaces
from psutil import virtual_memory,disk_usage,net_io_counters,net_if_addrs,cpu_count,cpu_freq,cpu_percent,disk_partitions
from os import name,popen
from wmi import WMI
import subprocess
from cpuinfo import get_cpu_info
from platform import uname
from os import getlogin
import GPUtil
from tabulate import tabulate
from colorama import Fore
import socket
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
    def Cpu(self):
        """
        :return: Full CPU Info
        """
        return get_cpu_info()['brand_raw']
    def Cpubrand(self):
        """
        :return: CPU Brand
        """
        return get_cpu_info()['brand']
    def CpuModel(self):
        """
        :return: CPU Model
        """
        return get_cpu_info()['model']
    def CpuFamily(self):
        """
        :return: CPU Family
        """
        return get_cpu_info()['family']
    def CpuBits(self):
        """
        :return: CPU Bits
        """
        return get_cpu_info()['bits']
    def CpuCount(self):
        """
        :return: CPU Count
        """
        return get_cpu_info()['count']
    def CpuArch(self):
        """
        :return: CPU Architecture
        """
        return get_cpu_info()['raw_arch_string']
    def CpuL1InstructionCache(self):
        """
        :return: CPU L1 Instruction Cache size
        """
        return get_cpu_info()['l1_instruction_cache_size']
    def CpuL1dataCache(self):
        """
        :return: CPU L1 data cache size
        """
        return get_cpu_info()['l1_data_cache_size']
    def CpuL2Cache(self):
        """
        :return: CPU L2 Data Cache Size
        """
        return get_cpu_info()['l2_cache_size']
    def CpuL3Cache(self):
        """
        CPU L3 Data Cache Size
        :return:
        """
        return get_cpu_info()['l3_cache_size']
    def CpuCorePhysical(self):
        """
        :return: physical core count
        """
        return cpu_count(logical=False)
    def CpuCoreLogical(self):
        """
        :return: logical core count
        """
        return cpu_count(logical=True)
    def CpuCurrentFrequency(self):
        """
        :return: returns current frequency
        """
        return cpu_freq().current
    def CpuMinFrequency(self):
        """
        :return: returns Minimum Frequency
        """
        return cpu_freq().min
    def CpuMaxFrequency(self):
        """
        :return: returns Max Frequency
        """
        return cpu_freq().max
    def CpuCurrentUtil(self):
        """
        :return: Current CPU current utilization
        """
        return cpu_percent(interval=1)
    def CpuPerCurrentUtil(self):
        """
        :return: Current Per CPU utilization
        """
        return cpu_percent(interval=1, percpu=True)
class ram():
    def TotalRam(self,bytes:bool):
        """
        :return: Memory Size
        """
        if bytes == None:
            return virtual_memory().total
        elif bytes:
            return virtual_memory().total
        else:
            return round(virtual_memory().total/1000000000, 2)
    def AvailableRam(self, bytes:bool):
        """
        :return: Available Ram
        """
        if bytes == None:
            return virtual_memory().available
        elif bytes:
            return virtual_memory().available
        else:
            return round(virtual_memory().available / 1000000000, 2)
    def UsedRam(self,bytes:bool):
        """
        :return: Used Ram
        """
        if bytes == None:
            return virtual_memory().used
        elif bytes:
            return virtual_memory().used
        else:
            return round(virtual_memory().used/1000000000, 2)
    def UsedRamPercentage(self):
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
    def NetInfo(self,options:NetworkOptions,tab:bool):
        """
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
    def GetIP(self):
        """
        :return: gets IP NO CIDR
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = (s.getsockname()[0])
        return ip
    def GetDefault(self):
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
    def StorageSize(self,DriveLetter):
        """
        :return: Storage Size of Designated Drive
        """
        if DriveLetter == None:
            return disk_usage(f'C:/').total
        else:
            return disk_usage(f'{DriveLetter}/').total
    def get_disk_info(self, options:StorageOptions):
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
    def GPUInfo(self, options:GPUOptions, tab:bool):
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
class OSoptions:
    def OSNAME(self):
        """
        :return: Operating System Name
        """
        return "OSNAME"
    def RELEASE(self):
        """
        :return: Operating System Release
        """
        return "RELEASE"
    def ALL(self):
        """"
        :return: All Choices
        """
        return "ALL"
def OS(options:OSoptions,tab:bool):
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
def Motherboard_Name():
    """
    :return: Motherboard
    """
    s=subprocess.Popen(['wmic', 'baseboard','get','product'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = s.communicate()
    return out.__str__().split("\n")[0].split(r"\n")[1].split(r"\\r")[0].replace(r"\r","")
def SystemName():
    """
    :return: PC NAME
    """
    return uname().node
def ActiveUser():
    """
    :return: Gets the Active user
    """
    return getlogin()
