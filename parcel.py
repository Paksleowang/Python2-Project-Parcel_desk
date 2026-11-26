from dataclasses import dataclass,field
import secrets
import string

@dataclass
class Parcel():
    date : str
    reciever : str
    items : list[tuple[str, str]] = field(default_factory=list)

    def pID(self)-> str:
        """This function returns a random unique parcel id """
        alphanumeric = string.ascii_letters + string.digits
        existing_pids = {code for code, _ in self.items}

        while True:
            pid = "".join(secrets.choice(alphanumeric) for _ in range(8))
            if pid not in existing_pids:
                return pid

    def add_item(self, item: str)-> None:
        """This funtion returns a tuple (pid,item)"""
        _pid = self.pID()
        self.items.append((_pid,item))
        return None



        
                
        