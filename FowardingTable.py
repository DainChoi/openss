import struct

class FowardingTable:
    def __init__(self, name):
        self.name = name
        self.fowardingtable = []

    def getTable(self):
        return self.fowardingtable

    def search(self, dst_ip):
        print('search start : ', dst_ip)
        for i in range(len(self.fowardingtable)):
            address = self.fowardingtable[i][0]
            netmask = self.fowardingtable[i][1]

            print('address : ', address, 'netmask : ', netmask)
            if self.byte_and_operator(dst_ip, netmask) == address:
                print('same tuple : ', i)
                return i

        print('search fail')
        return None

    def byte_and_operator(self,address, netmask):
        (addr0, addr1, addr2, addr3) = struct.unpack('!4B', address)
        (net0, net1, net2, net3) = struct.unpack('!4B', netmask)

        ret_val = struct.pack('!4B', addr0 & net0, addr1 & net1, addr2 & net2, addr3 & net3)
        print ('return value : ', ret_val)
        return ret_val

    def insert(self, dst_ip, netmask, gateway_ip, flag, interface, metric):
        print('ROUTING TABLE_INSERT')
        self.fowardingtable.appen([dst_ip, netmask, gatewqy_ip, flag, interface, metric])
        print(self.fowardingtable)