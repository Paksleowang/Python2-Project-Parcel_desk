"""This class is to store and record the parcels recieved."""
from parcel import Parcel
class Desk():
    def __init__(self, name: str, room:int, parcel : Parcel):
        self.name = name
        self.room = room
        self.parcel = parcel