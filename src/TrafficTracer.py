import threading

import scapy.all
from scapy.all import Packet


class TrafficTracer:
    def __init__(self):
        self.packets = []
        self.tracking_thread = None
        self.running = False

    def start_track(self) -> None:
        self.running = True
        self.tracking_thread = threading.Thread(target=self._track_network)
        self.tracking_thread.start()

    def _track_network(self) -> None:
        self.packets = []
        while self.running:
            scapy.all.sniff(prn=self.__packet_callback, stop_filter=self.__stop)

    def stop_track(self) -> None:
        if self.tracking_thread:
            self.running = False
            self.tracking_thread.join()

    def __stop(self, packet: Packet) -> bool:
        return not self.running

    def __packet_callback(self, packet: Packet) -> None:
        self.packets.append(packet)

    # def start_track(self) -> None:
    #     scapy.all.sniff(prn=self.__packet_callback)
