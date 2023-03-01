<h1>SystemScripter</h1>
<h2>Classes:</h2>
<h3>Prerequisites:</h3>
<h4>This class is only used for the get_size() which is used by other classes, not intended for user use</h4>
<h3>CPU:</h3>
<h4>This class uses the following functions:</h4>
<ul>
<li><code>Cpu()</code>:Used to return all CPU info</li>
<li><code>CpuBrand()</code>:Returns the brand of the CPU</li>
<li><code>CpuModel</code>: Returns the model of the CPU</li>
<li><code>CpuFamily()</code>: Returns the Family of the CPU</li>
<li><code>CpuBits()</code>: Returns the bits of the CPU</li>
<li><code>CpuCount()</code>: Returns the count of CPUs</li>
<li><code>CpuArch()</code>: Returns the Architecture of the CPU</li>
<li><code>CpuL1InstructionCache()</code>: Returns L1 Instruction Cache</li>
<li><code>CpuL1dataCache()</code>: Returns L1 Data Cache</li>
<li><code>CpuL2Cache()</code>: Returns L2 Data Cache(If Applicable)</li>
<li><code>CpuL3Cache()</code>: Returns L3 Data Cache(If Applicable)</li>
<li><code>CpuCorePhysical()</code>: Returns Physical Core Count</li>
<li><code>CpuCoreLogical()</code>: Returns Logical Core Count</li>
<li><code>CpuCurrentFrequency()</code>: Returns the current CPU frequency</li>
<li><code>CpuMinFrequency()</code>: Returns the Minimum CPU frequency</li>
<li><code>CpuMaxFrequency()</code>: Returns the max CPU frequency</li>
<li><code>CpuCurrentUtil()</code> Returns the current CPU utilization</li>
<li><code>CpuPerCurrentUtil()</code>: Returns the current CPU utilization per CPU</li>
</ul>
<br>
<h3>RAM:</h3>
<h4>This class has the following functions:</h4>
<ul>
<li><code>TotalRam(bytes:bool)</code>: Returns the total memory size</li>
<li><code>AvailableRam(bytes:bool)</code>: Returns available amount of memory at current time of call</li>
<li><code>UsedRam(bytes:bool)</code>: Returns the amount of used memory at current time of call</li>
<li><code>UsedRamPercentage()</code>: Returns the percentage of memory being currently used</li>
</ul>
<br>
<h3>Network:</h3>
<h4>This class has the following functions:</h4>
<ul>
<li><code>NetInfo(options:str,tab:bool)</code>: Returns info based on options provided and can be returned in <code>list</code> or <code>str</code> from<code>Tabulate</code></li>
<li><code>GetIP()</code>: Returns the IP of the computer at current time</li>
<li><code>GetDefault()</code>: Returns the default gateway of the computer</li>
</ul>
<h4>You can use the <code>NetworkOptions</code> class to help use this class.</h4>
<h3>NetworkOptions:</h3>
<h4>The following variables are listed below:</h4>
<ul>
<li><code>NAME</code></li>
<li><code>ADDRESS</code></li>
<li><code>NETMASK</code></li>
<li><code>BROADCAST</code></li>
<li><code>BYTESSENT</code></li>
<li><code>BYTESRECEIVED</code></li>
<li><code>ALL</code></li>
</ul>
<br>
<h3>Storage:</h3>
<h4>This class has the following functions:</h4>
<ul>
<li><code>StorageSize(DriveLetter)</code>: Returns the size of the current drive letter and if left as none then will return the size of Root Drive(C:)</li>
<li><code>get_disk_info(options:str)</code>: Returns disk info depending on the options given or if none are given, will return all of them in a set</li>


</ul>
<h4>This class also can use the <code>StorageOptions</code> class to assist you.</h4>
<h4>StorageOptions:</h4>
<h3>This class has these variables:</h3>
<ul>
<li><code>DEVICE</code></li>
<li><code>TOTAL</code></li>
<li><code>USED</code></li>
<li><code>FREE</code></li>
<li><code>PERCENT</code></li>
<li><code>FSTYPE</code></li>
<li><code>MOUNTPOINT</code></li>
<li><code>ALL</code></li>
</ul>
<br>
<h3>GPU:</h3>
<h4>This class has the following functions:</h4>
<ul>
<li><code>GPUInfo(options:str,tab:bool)</code>: Returns GPU Info depending on options and can be returned with <code>Tabulate</code>, if no options are specified it will return the same as if you used <code>GPUOptions.SHOWALL</code></li>
</ul>
<h4>This class also has the <code>GPUOptions</code> class to assist you.</h4>
<h3>GPUOptions</h3>
<h4>This class has the following variables:</h4>
<ul>
<li><code>IDONLY</code></li>
<li><code>NAMEONLY</code></li>
<li><code>LOADONLY</code></li>
<li><code>FREEMEMONLY</code></li>
<li><code>USEDMEMONLY</code></li>
<li><code>TOTALMEMONLY</code></li>
<li><code>TEMPONLY</code></li>
<li><code>SHOWALL</code></li>
</ul>
<br>
<h4>WindowsCommands:</h4>
<h3>This class  includes the following:</h3>
<ul>
<li><code>Shutdown(force:bool=False)</code>:Sends Windows Shutdown Signal(Forced if needed)</li>
<li><code>Restart(force:bool=False)</code>:Sends Windows Restart Signal(Forced if needed)</li>
<li><code>Start(Path:str)</code>:Sends Windows Start Signal to run a file using path</li>
</ul>
<br>
<h4><code>OS(options:str,tab:bool):</code></h4>
<h5>This function is used to get information about the operating system.</h5>
<h4>This functions also has the <code>OSoptions</code> class to help.</h4>
<h3>OSoptions:</h3>
<h4>This class has the following variables:</h4>
<ul>
<li><code>OSNAME</code></li>
<li><code>RELEASE</code></li>
<li><code>ALL</code></li>
</ul>
<br>
<h4><code>Motherboard_Name():</code></h4>
<h5>Returns the name of the motherboard.</h5>
<br>
<h4><code>Motherboard_Manufacturer():</code></h4>
<h5>Returns the Manufacturer of the motherboard</h5>
<br>
<h4><code>Motherboard_Serial():</code></h4>
<h5>Returns the motherboard serial number </h5>
<br>
<h4><code>Motherboard_Version()</code>:</h4>
<h5>Returns the Version of the Motherboard</h5>
<br>
<h4><code>SystemName():</code></h4>
<h5>Returns the name of the PC</h5>
<br>
<h4><code>ActiveUser():</code></h4>
<h5>Returns the active user that is logged in.</h5>
<br>
<h4><code>Change_Computer_Name(NewName:str,username:str,password:str):</code></h4>
<h5>Renames the PC and requests to restart to apply. </h5>
