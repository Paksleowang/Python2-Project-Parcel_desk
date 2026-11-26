from dataclasses import dataclass,field
import secrets

@dataclass
class Parcel():
    date : str
    reciever : str
    parcel = field(default_factory=list)

    def pID(self)-> str:
        """This function returns a random unique parcel id """
        alphaNumeric = "abcdefghijklmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ12345677890"
        pid = "".join(secrets.choices(alphaNumeric) for _ in range(8))
        for item in self.parcel["items"]:
            for code in item.keys():
                if pid in code:
                    pid = "".join(secrets.choices(alphaNumeric) for _ in range(8))
        
                
        