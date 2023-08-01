[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2016-2022 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
### ePO's Default Permission Set

ePO ships with four default permission sets that provide permissions to ePO functionality. The
default permission sets available are:

-   Executive Reviewer
-   Global Reviewer
-   Group Admin
-   Group Reviewer

For all the actions to execute without any dispute any of the following combinations of permissions
will work :

-   ( Executive Reviewer , Group Admin )
-   ( Global Reviewer , Group Admin )
-   ( Executive Reviewer , Global Reviewer , Group Admin )
-   ( Executive Reviewer , Global Reviewer , Group Admin , Group Reviewer )

----------------------------------------------------------------------------------------------------

***Note*** : *All the permission sets mentioned above are for non-admin users. Incase you are an
admin, your permission set is by default set to 'administrator' and have all the access rights.
Administrator can execute all the actions without any additional permissions.*

----------------------------------------------------------------------------------------------------
