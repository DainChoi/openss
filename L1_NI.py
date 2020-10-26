from scapy.sendrecv import sendp
from Dictionary import *
import struct
import pcap
import threading


class L1_NI:
    def __init__(self, name):
        self.name = name
        self.underLayer = None
        self.upperLayer = None
        self.device = None
        self.ifnum = -1

    def coonectLayers(self, underLayer,upperLayer):
        self.underLayer = underLayer
        self.upperLayer = upperLayer

    def getAdapterList(self):
        print('[Layer ' + self.name + '] Called setAdapter()')
        print('TODO: use Sniifer and set networt adapter')

        self.devices = pcap.findalldevs()
        i=0
        buf = ''
        for dev in self.devices:
            buf = nuf + (str(i) + ') ' + dev + ', ')
            i = i+1
        print(buf)

    def setAdapter(self, ifnum):
        self.ifnum = ifnum
        print("Selected " + ifnum + "the device: " + self.devices[int(self.ifnum)])

    def execute(self):
        print(threading.current_Thread().getName(), self.name)
        packets = pcap.pcap(name=self.devices[int(self.ifnum)], promisc=True, immediate=True, timeout_ms=50)

        for ts, ppayload in packets:
            self.receive(ppayload)

    def startAdapter(self):
        my_thread = threading.Thread(target=self.execute, args=())
        my_thread.start()

    def receive(self, ppayload):
        self.upperLayer.receive(ppayload)

    def send(self, data):
        sendp(data, iface = delf.devices[int(self.ifnum)])
        pass