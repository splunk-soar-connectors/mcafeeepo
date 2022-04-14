[comment]: # "Auto-generated SOAR connector documentation"
# McAfee ePO

Publisher: Splunk  
Connector Version: 2\.0\.5  
Product Vendor: McAfee  
Product Name: McAfee ePO  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.2\.0  

This app implements various endpoint based investigative and containment actions by integrating with McAfee ePO

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a McAfee ePO asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**username** |  required  | string | Username
**password** |  required  | password | Password
**ip\_hostname** |  required  | string | Host of ePO Instance
**port** |  required  | string | Port Number
**quarantine\_tag** |  optional  | string | Quarantine Tag
**verify\_server\_cert** |  optional  | boolean | Verify Server Certificate

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate connectivity to McAfee ePO  
[add tag](#action-add-tag) - Add a tag to an endpoint  
[remove tag](#action-remove-tag) - Remove a tag from the endpoint  
[get device info](#action-get-device-info) - Get information about an endpoint  
[quarantine device](#action-quarantine-device) - Send the quarantine tag to the endpoint  
[unquarantine device](#action-unquarantine-device) - Remove the quarantine tag on the endpoint  

## action: 'test connectivity'
Validate connectivity to McAfee ePO

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'add tag'
Add a tag to an endpoint

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip\_hostname** |  required  | Endpoint to apply tag to | string |  `ip`  `host name` 
**tag** |  required  | Tag to add | string |  `mfeepo tag` 
**wakeup\_agent** |  optional  | Wakeup Agent after adding tag | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.ip\_hostname | string |  `ip`  `host name` 
action\_result\.parameter\.tag | string |  `mfeepo tag` 
action\_result\.parameter\.wakeup\_agent | boolean | 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove tag'
Remove a tag from the endpoint

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip\_hostname** |  required  | Endpoint to remove tag from | string |  `ip`  `host name` 
**tag** |  required  | Tag to remove | string |  `mfeepo tag` 
**wakeup\_agent** |  optional  | Wakeup Agent after removing tag | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.ip\_hostname | string |  `ip`  `host name` 
action\_result\.parameter\.tag | string |  `mfeepo tag` 
action\_result\.parameter\.wakeup\_agent | boolean | 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get device info'
Get information about an endpoint

Type: **investigate**  
Read only: **True**

If a quarantine tag is specified, this will return whether or not the device is currently quarantined\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip\_hostname** |  required  | Endpoint to get info from | string |  `ip`  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.ip\_hostname | string |  `ip`  `host name` 
action\_result\.data\.\*\.EPOBranchNode\_AutoID | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_CPUSerialNum | string | 
action\_result\.data\.\*\.EPOComputerProperties\_CPUSpeed | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_CPUType | string | 
action\_result\.data\.\*\.EPOComputerProperties\_ComputerName | string | 
action\_result\.data\.\*\.EPOComputerProperties\_DefaultLangID | string | 
action\_result\.data\.\*\.EPOComputerProperties\_Description | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_DomainName | string |  `domain` 
action\_result\.data\.\*\.EPOComputerProperties\_FreeDiskSpace | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_FreeMemory | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_IPAddress | string | 
action\_result\.data\.\*\.EPOComputerProperties\_IPHostName | string |  `host name`  `ip` 
action\_result\.data\.\*\.EPOComputerProperties\_IPSubnet | string | 
action\_result\.data\.\*\.EPOComputerProperties\_IPSubnetMask | string | 
action\_result\.data\.\*\.EPOComputerProperties\_IPV4x | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_IPV6 | string | 
action\_result\.data\.\*\.EPOComputerProperties\_IPXAddress | string | 
action\_result\.data\.\*\.EPOComputerProperties\_IsPortable | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_LastAgentHandler | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_NetAddress | string | 
action\_result\.data\.\*\.EPOComputerProperties\_NumOfCPU | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_OSBitMode | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_OSBuildNum | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_OSOEMID | string | 
action\_result\.data\.\*\.EPOComputerProperties\_OSPlatform | string | 
action\_result\.data\.\*\.EPOComputerProperties\_OSServicePackVer | string | 
action\_result\.data\.\*\.EPOComputerProperties\_OSType | string | 
action\_result\.data\.\*\.EPOComputerProperties\_OSVersion | string | 
action\_result\.data\.\*\.EPOComputerProperties\_ParentID | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_SubnetAddress | string | 
action\_result\.data\.\*\.EPOComputerProperties\_SubnetMask | string | 
action\_result\.data\.\*\.EPOComputerProperties\_SystemDescription | string | 
action\_result\.data\.\*\.EPOComputerProperties\_SysvolFreeSpace | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_SysvolTotalSpace | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_TimeZone | string | 
action\_result\.data\.\*\.EPOComputerProperties\_TotalDiskSpace | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_TotalPhysicalMemory | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_UserName | string |  `user name` 
action\_result\.data\.\*\.EPOComputerProperties\_UserProperty1 | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_UserProperty2 | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_UserProperty3 | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_UserProperty4 | numeric | 
action\_result\.data\.\*\.EPOComputerProperties\_Vdi | numeric | 
action\_result\.data\.\*\.EPOLeafNode\_AgentGUID | string | 
action\_result\.data\.\*\.EPOLeafNode\_AgentVersion | string | 
action\_result\.data\.\*\.EPOLeafNode\_ExcludedTags | string | 
action\_result\.data\.\*\.EPOLeafNode\_LastUpdate | string | 
action\_result\.data\.\*\.EPOLeafNode\_ManagedState | numeric | 
action\_result\.data\.\*\.EPOLeafNode\_Tags\.\*\.Tag | string |  `mfeepo tag` 
action\_result\.data\.\*\.EPO\_IP/Hostname | string |  `host name`  `ip` 
action\_result\.data\.\*\.EPO\_Port | string |  `port` 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'quarantine device'
Send the quarantine tag to the endpoint

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip\_hostname** |  required  | Endpoint to quarantine | string |  `ip`  `host name` 
**wakeup\_agent** |  optional  | Wakeup Agent after applying quarantine tag | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.ip\_hostname | string |  `ip`  `host name` 
action\_result\.parameter\.wakeup\_agent | boolean | 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'unquarantine device'
Remove the quarantine tag on the endpoint

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip\_hostname** |  required  | Endpoint to unquarantine | string |  `ip`  `host name` 
**wakeup\_agent** |  optional  | Wakeup Agent after removing quarantine tag | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.ip\_hostname | string |  `ip`  `host name` 
action\_result\.parameter\.wakeup\_agent | boolean | 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 