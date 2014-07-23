OpenIndiana-disk
================

List disk infomation, may help to create zpool.


Usage:

# disk --help
Usage:
        /usr/bin/disk                # List disk info
        /usr/bin/disk -h or --help   # Show this help info
Note:
        This command will list disk info in current system, include below message:

        DEVICE:
                Display device names in descriptive format. For example: cXtYdZ
        ALISA:
                Device Name
        VENDOR: 
                Vendor Name 
        PRODUCT: 
                Product ID
        SERIALNO: 
                Serial No.
        SIZE: 
                Size of this device
        FREE: 
                Is free or not, value(yes, no)


Example:

# disk
DEVICE                  ALISA   VENDOR     PRODUCT        SERIALNO         SIZE         FREE  
c1d0                    cmdk0   unknow     unknow         20130513AA00000  4.01GB       no    
c7t5000C50043FCDEB7d0   sd1     SEAGATE    ST3300657SS    6SJ3V1VG         300.00GB     no    
c7t5000C50047008657d0   sd2     SEAGATE    ST3300657SS    6SJ3VRTN         300.00GB     yes   
c7t5000C50043FEE96Bd0   sd3     SEAGATE    ST3300657SS    6SJ3X0VW         300.00GB     no    
c7t5000C50043FE7BDFd0   sd4     SEAGATE    ST3300657SS    6SJ3X2XS         300.00GB     no    
c7t5000C5004F60370Bd0   sd5     ATA        ST1000NM0011   Z1N3C8PR         1000.20GB    yes   
c6t50015B21680AAA22d0   sd9     ATA        ST3500630NS    9QG39H3B         500.11GB     yes
