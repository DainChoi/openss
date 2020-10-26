from Dictionary iport *
import struct
import ARPCacheTable import *

class L3_ARP:
    def __init__(self, name, my_mac, my_ip):
        self.name = name
        self.underLayer = None
        self.upperLayer = None

        self._hard_type = b'\x00\x01'
        self._proto_type = b'\x08\x00'
        self._hard_len = b'\x06'
        self._proto_len = b'\x04'
        self.opcode = None
        self._sender_mac = my_mac
        self._sender_ip = my_ip
        self._target_mac = None
        self._target_ip = None

        self.arptable = None

    def connectTable(self, arptable):
        self.arptable = arptable

    def coonectLayers(self, underLayer, upperLayer):
        self.underLayer = underLayer
        self.upperLayer = upperLayer

    def receive(self, ppayload):
        print('[Layer ' + self.name +'] Called receive()')

        self.extractHeader(ppayload)

        proxy_i = self.arptable.proxysearch(self._ptarget_ip)
        if proxy_i != None:
            self.sendPARPReply(self.arptable.proxy_get_ip(proxy_i))

        if self._ptarget_ip != self._sender_ip:
            return

        if self._psender_ip == self._sender_ip:
            return

        if self._popcode == ARP_OPCODE_REQUEST:
            index = self.arptable.search(self._psender_ip)
            if index == None:
                self.arptable.insert(self._psender_ip, self._psender_mac)
            else:
                self.arptable.update(index, self._psender_mac)

            if self._psender_ip != self._ptarget_ip:
                self.sendARPReply()

        if self.popcode == ARP_OPCODE_REPLY:
            index = self.arptavle.search(self._psender_ip)
            if index == None:
                self.arptable.insert(self._psender_ip, self._psender_mac)
            else:
                self.arptable.update(index, self._psender_mac)

    def send(self, data):
        print('[Layer ' + self.name + '] Called send()')
        self.underLayer.send(data, ETHERNET_TYPE_ARP)


    def extractHeader(self, raw):
        self._phard_type = raw[:2]
        self._pproto_type = raw[2:4]
        self._phard_len = raw[4:5]
        self._pproto_len = raw[5:6]
        self._popcode = raw[6:8]
        self._psender_mac = raw[8:14]
        self._psender_ip = raw[14:18]
        self._ptarget_mac = raw[18:24]
        self._ptarget_ip = raw[24:28]
        self._pheader = raw[:28]

    def checkARPCacheTable(self, ipdst):
        print('TODO: ARP cache table check', ipdst)
        index = self.arptable.search(ipdst)
        if ndex != None:
            print('[Layer ' + self.name + '] ARP cache entry search success')
            eth_dst = self.arptable.get_mac(index)
            self.underLayer.set_dst(eth_dst)
            return True
        else:
            print('[Layer ' + self.name +'] ARP cache entry search fail')
            self.sendARPRequest(ipdst)
            return False


    def sendARPRequest(self, ipdst):
        print('[Layer ' + self.name + '] Called sendARPRequest()')
        self._hard_type = b'\x00\x01'
        self._proto_type = b'\x08\x00'
        self._hard_len = b'\x06'
        self._proto_len = b'\x04'
        self._opcode = ARP_OPCODE_REQUEST
        self._target_mac = b'\x00\x00\x00\x00\x00\x00'
        self._target_ip = ipdst

        self.underLayer.set_dst(b'\xff\xff\xff\xff\xff\xff')
        print(self.generatePayload())

        self.send(self.generatePayload())

    def sendARPReply(self):
        print('[Layer ' + self.name + '] Called sendARPReply()')
        self._hard_type = self._phard_type
        self._proto_type = self._pproto_type
        self._hard_len = self._phard_len
        self._proto_len = self._pproto_len
        self._opcode = ARP_OPCODE_REPLY
        self._target_mac = self._psender_mac
        self._target_ip = self._psender_ip

        self.underLayer.set_dst(self._psender_mac)

        self.send(self.generatePayload())

    def generatePayload(self):
        return self._hard_type + self._proto_type + self._hard_len + self._proto_len + self._opcode + self._sender_mac \
                + self._sender_ip + self._target_mac + self._target_ip
