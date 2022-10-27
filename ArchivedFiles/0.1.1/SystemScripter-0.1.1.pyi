from typing import Union


class Prerequisites:
    def get_size(self, bytes, suffix: str = ...): ...

class cpu:
    def Cpu(self) -> str: ...
    def CpuBrand(self) -> str: ...
    def CpuModel(self) -> str: ...
    def CpuFamily(self) -> str: ...
    def CpuBits(self) -> str: ...
    def CpuCount(self) -> str: ...
    def CpuArch(self) -> str: ...
    def CpuL1InstructionCache(self) -> str: ...
    def CpuL1dataCache(self) -> str: ...
    def CpuL2Cache(self) -> str: ...
    def CpuL3Cache(self) -> str: ...
    def CpuCorePhysical(self) -> int: ...
    def CpuCoreLogical(self) -> int: ...
    def CpuCurrentFrequency(self) -> float: ...
    def CpuMinFrequency(self) -> float: ...
    def CpuMaxFrequency(self) -> float: ...
    def CpuCurrentUtil(self) -> float: ...
    def CpuPerCurrentUtil(self) -> float: ...

class ram:
    def TotalRam(self, bytes: bool) -> float: ...
    def AvailableRam(self, bytes: bool) -> float: ...
    def UsedRam(self, bytes: bool) -> float: ...
    def UsedRamPercentage(self) -> float: ...

class NetworkOptions:
    NAME: str
    ADDRESS: str
    NETMASK: str
    BROADCAST: str
    BYTESSENT: str
    BYTESRECEIVED: str
    ALL: str

class Network:
    def NetInfo(self, options: str, tab: bool) -> Union[str, tuple]: ...
    def GetIP(self) -> str: ...
    def GetDefault(self) -> str: ...

class StorageOptions:
    DEVICE: str
    TOTAL: str
    USED: str
    FREE: str
    PERCENT: str
    FSTYPE: str
    MOUNTPOINT: str
    ALL: str

class Storage:
    def StorageSize(self, DriveLetter) -> int: ...
    def get_disk_info(self, options: str) -> Union[str, int, float, list]: ...

class GPUOptions:
    IDONLY: str
    NAMEONLY: str
    LOADONLY: str
    FREEMEMONLY: str
    USEDMEMONLY: str
    TOTALMEMONLY: str
    TEMPONLY: str
    SHOWALL: str

class GPUExceptions(Exception):
    def WrongType(GPUExceptions) -> None: ...

class GPU:
    def GPUInfo(self, options: str, tab: bool) -> Union[str, list]: ...

class WindowsCommands:
    def Shutdown(self, force: bool = ...) -> None: ...
    def Restart(self, force: bool = ...) -> None: ...
    def Start(self, Path: str) -> None: ...

class OSoptions:
    OSNAME: str
    RELEASE: str
    ALL: str

def OS(options: str, tab: bool) -> Union[str, tuple]: ...
def Motherboard_Name() -> str: ...
def Motherboard_Manufacturer() -> str: ...
def Motherboard_Serial() -> str: ...
def Motherboard_Version() -> str: ...
def SystemName() -> str: ...
def ActiveUser() -> str: ...
def Change_Computer_Name(NewName: str, username: str, password: str, RestartPreference: bool = ...) -> None: ...