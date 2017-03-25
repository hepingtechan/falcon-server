import sys, os, types
import socket, fcntl, struct

def getLocalHostAddrOld():
    localHostAddr = os.popen("ifconfig eth0 | grep 'inet addr' \
                             | awk '{print $2}' | awk -F: '{print $2}'").readlines()
    localHostAddr = localHostAddr[0].split()
    return localHostAddr[0]

def getLocalHostAddr():
    addr = getIPAdrr('eth0')
    return addr

def getIPAdrr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


if __name__ == '__main__':
    addr = getLocalHostAddr()
    print addr
