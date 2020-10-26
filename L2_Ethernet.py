from Dictionary import *
import struct


class L2_Ethernet:
    def __init__(self, name, src):
        self.name = name
        self.underLayer = None
        self.upperLayer = None

        self._dst = None
        self._src = src
        self._type = None
        self._data = None

    def coonectLayers(self, underLayer, upperLayers):
        self.underLayer = underLayer
        self.upperLayers = upperLayers

    def set_dst(self, ARP_MAC_address):
        self._dst = ARP_MAC_address

    def receive(self, ppayload):
        self.extractHeader(ppayload)
        print("received packet: ", ppayload)

        if self._pdst == ETH_ADDR_BROADCAST or self._src == self._pdst:
            if self._src == self._psrc:
                return
        if self._ptype == ETHERNET_TYPE_IP:
            self.upperLayers[0].receive(self._pdata)

        if self._ptype == ETHERNET_TYPE_ARP:
            self.upperLayers[1].receive(self._pdata)

    def send(self, data, type, opt=None):

        if type == ETHERNET_TYPE_IP:
            self._type = ETHERNET_TYPE_IP
        if type == ETHERNET_TYPE_ARP:
            self._type = ETHERNET_TYPE_ARP

        self.underLayers.send(self.generatePayload(data))

    def extractHeader(self, raw):
        self._pdst = raw[:6]
        self._psrc = raw[6:12]
        self._ptype = raw[12:14]
        self._pdata = raw[14:]
        self._pheader = raw[:14]

    def generatePayload(self, data):
        self._data = data
        return self._dst + self._src + self._type + self._data