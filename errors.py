from abc import Exception

class PIDNotFoundError(Exception):
    super().__init__(f"The parcel ID is not available")

class TennantNotFoundError(Exception):
    def __init__(self,name:str):
        super().__init__(f"There is no tennant {name}")
        self.name = name

class ParcelNotFoundError(Exception):
    super().__init__(f"Parcel not found.")


