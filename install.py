#!/usr/bin/env python
__author__ = 'Josh Windsor'
__copyright__ = "Copyright 2015"
__credits__ = ["Josh Windsor"]
__license__ = "TBD"
__maintainer__ = "Josh Windsor"
__email__ = "ging.sor@gmail.com"
__status__ = "Prototype"


import subprocess
import urllib2
import argparse
import sys
import os
import re


class Colors:
    # Reset
    Color_Off = '\x1b[0m'       # Text Reset

    # Regular Colors
    Black = '\x1b[0;30m'        # Black
    Red = '\x1b[0;31m'          # Red
    Green = '\x1b[0;32m'        # Green
    Yellow = '\x1b[0;33m'       # Yellow
    Blue = '\x1b[0;34m'         # Blue
    Purple = '\x1b[0;35m'       # Purple
    Cyan = '\x1b[0;36m'         # Cyan
    White = '\x1b[0;37m'        # White

    # Bold
    BBlack = '\x1b[1;30m'       # Black
    BRed = '\x1b[1;31m'         # Red
    BGreen = '\x1b[1;32m'       # Green
    BYellow = '\x1b[1;33m'      # Yellow
    BBlue = '\x1b[1;34m'        # Blue
    BPurple = '\x1b[1;35m'      # Purple
    BCyan = '\x1b[1;36m'        # Cyan
    BWhite = '\x1b[1;37m'       # White

    # Underline
    UBlack = '\x1b[4;30m'       # Black
    URed = '\x1b[4;31m'         # Red
    UGreen = '\x1b[4;32m'       # Green
    UYellow = '\x1b[4;33m'      # Yellow
    UBlue = '\x1b[4;34m'        # Blue
    UPurple = '\x1b[4;35m'      # Purple
    UCyan = '\x1b[4;36m'        # Cyan
    UWhite = '\x1b[4;37m'       # White

    # Background
    On_Black = '\x1b[40m'       # Black
    On_Red = '\x1b[41m'         # Red
    On_Green = '\x1b[42m'       # Green
    On_Yellow = '\x1b[43m'      # Yellow
    On_Blue = '\x1b[44m'        # Blue
    On_Purple = '\x1b[45m'      # Purple
    On_Cyan = '\x1b[46m'        # Cyan
    On_White = '\x1b[47m'       # White

    # High Intensity
    IBlack = '\x1b[0;90m'       # Black
    IRed = '\x1b[0;91m'         # Red
    IGreen = '\x1b[0;92m'       # Green
    IYellow = '\x1b[0;93m'      # Yellow
    IBlue = '\x1b[0;94m'        # Blue
    IPurple = '\x1b[0;95m'      # Purple
    ICyan = '\x1b[0;96m'        # Cyan
    IWhite = '\x1b[0;97m'       # White

    # Bold High Intensity
    BIBlack = '\x1b[1;90m'      # Black
    BIRed = '\x1b[1;91m'        # Red
    BIGreen = '\x1b[1;92m'      # Green
    BIYellow = '\x1b[1;93m'     # Yellow
    BIBlue = '\x1b[1;94m'       # Blue
    BIPurple = '\x1b[1;95m'     # Purple
    BICyan = '\x1b[1;96m'       # Cyan
    BIWhite = '\x1b[1;97m'      # White

    # High Intensity backgrounds
    On_IBlack = '\x1b[0;100m'   # Black
    On_IRed = '\x1b[0;101m'     # Red
    On_IGreen = '\x1b[0;102m'   # Green
    On_IYellow = '\x1b[0;103m'  # Yellow
    On_IBlue = '\x1b[0;104m'    # Blue
    On_IPurple = '\x1b[0;105m'  # Purple
    On_ICyan = '\x1b[0;106m'    # Cyan
    On_IWhite = '\x1b[0;107m'   # White

partitions = []

def createPartition():
    #TODO - Need to write a description of function

    regexs = re.compile(r'/dev([/_a-zA-Z0-9])+')
    diskInfo = subprocess.check_output(['fdisk', '-l']).decode(encoding='UTF-8')
    diskInfoList = diskInfo.split('\n')
    diskInfoFomated = ''
    devices = []
    for line in diskInfoList:
        device = ''
        match = regexs.search(line)
        if match:
            device = line[match.start():match.end()]
            devices.append(device)
            line = line.replace(device, Colors.Red + device + Colors.Color_Off)
        diskInfoFomated += line.replace('Disk', '\n\nDisk')
    print('{0}'.format(diskInfoFomated))

    selectedDevice = raw_input("Enter device: ")
    while( selectedDevice not in devices):
        selectedDevice = raw_input("Enter device: ")

    numOfPartitions = input("Enter Number of Partitions: ")
    for itr in range(1,int(numOfPartitions)+1):
        sizeRe = re.compile(r'\+\d+(MB|G)')
        pSize = raw_input("Enter in size (+<size><MB,G>)")
        match = sizeRe.search(pSize)

        while( not match ):
            pSize = input("Enter in size (+<size><MB,G>)")
            match = sizeRe.search(pSize)

        createPartitionCmd = '({e} n; {e} p; {e} {0}; {e} ; {e} {1}; {e} w) | fdisk {2}'.format(str(itr), pSize, selectedDevice, e="echo")
        #createPartitionCmd = '(echo n; echo p; echo ' + str(itr) +'; echo ; echo ' + pSize + '; echo w) | fdisk ' + selectedDevice
        output = subprocess.check_output(createPartitionCmd, shell=True)
        print(output)
        partitions.append(selectedDevice + str(itr))

    for parti in partitions:
        formatCmd = ''
        if parti != partitions[len(partitions)-1]:
            formatCmd = 'mkfs.ext4 {0}'.format(parti)
        else:
            formatCmd = 'mkswap {0}  &&  swapon {1}'.format(parti, parti)
        print(subprocess.check_output(formatCmd, shell=True))

# def setKeymap():
#     #TODO - Need to write a description of function
#     """
#     """
#     output = subprocess.check_output('localectl list-keymaps', shell=True)
#     keymaps = output.split('\n')

def setEditor():
    #TODO - Need to write a description of function
    """
    """
    editorList = ["emacs", "nano", "vi", "vim", "zile"]
    selectedEditor = raw_input("Enter default editor ({0}): ".format(editorList))
    while selectedEditor not in editorList:
        selectedEditor = raw_input("Did not enter a valid editor. Try again: ({0}): ".format(editorList))

    print(subprocess.check_output('yes \n | pacman -S {0}'.format(selectedEditor), shell=True))


def configureMirrorlist():
    #TODO - Need to write a description of function
    """
    """

    Countries = {
        "All"           : "all",
        "Australia"     : "AU",
        "Austria"       : "AT",
        "Bangladesh"    : "BD",
        "Belarus"       : "BY",
        "Belgium"       : "BE",
        "Brazil"        : "BR",
        "Bulgaria"      : "BG",
        "Canada"        : "CA",
        "Chile"         : "CL",
        "China"         : "CN",
        "Colombia"      : "CO",
        "Croatia"       : "HR",
        "CzechRepublic" : "CZ",
        "Denmark"       : "DK",
        "Ecuador"       : "EC",
        "Estonia"       : "EE",
        "France"        : "FR",
        "Germany"       : "DE",
        "Greece"        : "GR",
        "Hungary"       : "HU",
        "Iceland"       : "IS",
        "India"         : "IN",
        "Indonesia"     : "ID",
        "Iran"          : "IR",
        "Ireland"       : "IE",
        "Israel"        : "IL",
        "Italy"         : "IT",
        "Japan"         : "JP",
        "Kazakhstan"    : "KZ",
        "Latvia"        : "LV",
        "Lithuania"     : "LT",
        "Luxembourg"    : "LU",
        "Macedonia"     : "MK",
        "Netherlands"   : "NL",
        "NewCaledonia"  : "NC",
        "NewZealand"    : "NZ",
        "Norway"        : "NO",
        "Philippines"   : "PH",
        "Poland"        : "PL",
        "Portugal"      : "PT",
        "Romania"       : "RO",
        "Russia"        : "RU",
        "Serbia"        : "RS",
        "Singapore"     : "SG",
        "Slovakia"      : "SK",
        "SouthAfrica"   : "ZA",
        "SouthKorea"    : "KR",
        "Spain"         : "ES",
        "Sweden"        : "SE",
        "Switzerland"   : "CH",
        "Taiwan"        : "TW",
        "Turkey"        : "TR",
        "Ukraine"       : "UA",
        "UnitedKingdom" : "GB",
        "UnitedStates"  : "US",
        "Vietnam"       : "VN"
    }
    
    #https://www.archlinux.org/mirrorlist/?country=US&country=&protocol=https&ip_version=4&ip_version=6&use_mirror_status=on
    archlinuxMirrorUrl = 'https://www.archlinux.org/mirrorlist/?'
    archassaultMirrorUrl = 'https://archassault.org/mirrorlist/?'

    table = []
    for c in Countries.iteritems():
       if len(table)  == 4:
           print("{0}".format(table))
           table = []

    selectedContries = raw_input("Select Contries for mirrorlist (Comma sperated): ")
    selectedContries = selectedContries.split(",")

    countryUrl = ''
    for country in selectedContries:
        if country == '':
            pass
        else:
            try:
                countryUrl += "country={0}&".format(Countries[country])
            except:
                pass

    
   
    ###protocols to use 
    protocolUrl = ''
    useHttp = raw_input("Use http? ([Y/n]): ")
    while useHttp.lower() != 'y' and useHttp.lower() != 'n' and useHttp.lower() != 'yes' and useHttp.lower() != 'no':
        useHttp = raw_input("Opps you did not say y or n. Use http? ([Y/n]): ")

    if useHttp.lower() == 'yes' or useHttp.lower() == 'y':
        protocolUrl += 'protocol=http&'
    
    useHttps = raw_input("Use https? ([Y/n]): ")
    while useHttps.lower() != 'y' and useHttps.lower() != 'n' and useHttps.lower() != 'yes' and useHttps.lower() != 'no':
        useHttps = raw_input("Opps you did not say y or n. Use https? ([Y/n]): ")

    if useHttps.lower() == 'yes' or useHttps.lower() == 'y':
        protocolUrl += 'protocol=https&'
     
    #protocol=https&ip_version=4&ip_version=6&use_mirror_status=on  
    ###ip to use
    ipUrl = ''
    useIpv4 = raw_input("Use Ipv4? ([Y/n]): ")
    while useIpv4.lower() != 'y' and useIpv4.lower() != 'n' and useIpv4.lower() != 'yes' and useIpv4.lower() != 'no':
        useIpv4 = raw_input("Opps you did not say y or n. Use Ipv4? ([Y/n]): ")
        
    if useIpv4.lower() == 'yes' or useIpv4.lower() == 'y':
        ipUrl += 'ip_version=4&'

    useIpv4 = raw_input("Use Ipv6? ([Y/n]): ")
    while useIpv6.lower() != 'y' and useIpv6.lower() != 'n' and useIpv6.lower() != 'yes' and useIpv6.lower() != 'no':
        useIpv6 = raw_input("Opps you did not say y or n. Use Ipv6? ([Y/n]): ")

    if useIpv6.lower() == 'yes' or useIpv6.lower() == 'y':
        ipUrl += 'ip_version=6&'

    statusUrl = ''
    useStatus = raw_input("Use status? ([Y/n]): ")
    while useStatus.lower() != 'y' and useStatus.lower() != 'n' and useStatus.lower() != 'yes' and useStatus.lower() != 'no':
        useStatus = raw_input("Opps you did not say y or n. Use status? ([Y/n]): ")

    if useStatus.lower() == 'yes' or useStatus.lower() == 'y':
        statusUrl += 'use_mirror_status=on'

    archlinuxMirrorUrl += "{0}{1}{2}{3}".format(countryUrl,ipUrl,protocolUrl,statusUrl)
    archassaultMirrorUrl += "{0}{1}{2}".format(countryUrl,ipUrl,protocolUrl)

    #get archlinux mirrorlist
    response = urllib2.urlopen(archlinuxMirrorUrl)
    mirrorlist = response.read()
    mirrorFile = open('/etc/pacman.d/mirrorlist', 'w')
    mirrorFile.write(mirrorlist)
    mirrorFile.close()

    #get archassault mirrorlist
    response = urllib2.urlopen(archassaultMirrorUrl)
    mirrorlist = response.read()
    mirrorFile = open('/etc/pacman.d/archassault-mirrorlist', 'w')
    mirrorFile.write(mirrorlist)
    mirrorFile.close()

def mountPartitions():
    #TODO - Need to write a description of function
    """
    """
    #TODO - Need to make this more usable
    mountLoc = ['/mnt', '/mnt/home', '/mnt/var']
    mkout = subprocess.check_output('mkdir -p /mnt/home /mnt/var', shell=True)
    for parti in partitions:
        if parti != partitions[len(partitions)-1]:
            # mount /dev/sda1 /mnt
            # mkdir /mnt/home
            # mkdir /mnt/var
            # mount /dev/sda2 /mnt/home
            # mount /dev/sda3 /mnt/var
            mntCmd = "mount {0} {1}".format(parti, mountLoc[0])
            subprocess.check_output(mntCmd, shell=True)
            mountLoc = mountLoc[1:]
        else:
            pass

def installBase():
    #TODO - Need to write a description of function
    """
    """
    subprocess.check_output('pacstrap /mnt base base-devel', shell=True)

def genFstab():
    #TODO - Need to write a description of function
    """
    """
    output = subprocess.check_output('genfstab -U -p /mnt /mnt/etc/fstab', shell=True)

def movePacmanConf():
    #TODO - Need to write a description of function
    """
    """
    subprocess.check_output('cp /etc/pacman.conf /mnt/etc', shell=True)
    subprocess.check_output('cp /etc/pacman.d/mirrorlist /mnt/etc/pacman.d/', shell=True)
    subprocess.check_output('cp /etc/pacman.d/archassault-mirrorlist /mnt/etc/pacman.d/', shell=True)

def updatePackages():
    #TODO - Need to write a description of function
    """
    """
    subprocess.check_output('arch-chroot "pacman -Syu"', shell=True)
    subprocess.check_output('arch-chroot "pacman -S archassault-keyring"', shell=True)
    subprocess.check_output('arch-chroot "pacman -Syyu"', shell=True)
    subprocess.check_output('arch-chroot "pacman -S archassault"', shell=True)

def setHostname():
    #TODO - Need to write a description of function
    """
    """
    hostname = raw_input("Enter hostname: ")
    hostnameCmd = 'echo "{0}" > /mnt/etc/hostname'.format(hostname)
    subprocess.check_output(hostnameCmd, shell=True)

    hostsCmd = 'arch_chroot "sed -i \'s/127.0.0.1/s/$/ \' \'{0}\'/ /etc/hosts"'.format(hostname)
    subprocess.check_output(hostsCmd, shell=True)


def setTimezone():
    #TODO - Need to write a description of function
    """
    """
    raise Exception("setTimezone not implimented")

def setRootPassword():
    #TODO - Need to write a description of function
    """
    """
    raise Exception("setRootPassword not implimented")

def umount():
    #TODO - Need to write a description of function
    """
    """
    output = subprocess.check_output('umount -R /mnt', shell=True)

def main():
    configureMirrorlist()
    createPartition()
    mountPartitions()
    installBase()
    movePacmanConf()
    updatePackages()
    setHostname()
    umount()


if __name__ == "__main__":
    main()


