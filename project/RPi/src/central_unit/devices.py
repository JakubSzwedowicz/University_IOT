from ...database.scripts.utils import DatabaseData

class AuthorizedDevices(DatabaseData.Definitions.Device):
    def __init__(self, access_level, deviceId: int, mac_address: str) -> None:
        super().__init__(deviceId, mac_address)
        self.access_level = access_level
    

class AuthorizedCards(DatabaseData.Definitions.Card):
    def __init__(self, access_level, id: int, rfid_tag: int, employee_id: int, card_status_id: int) -> None:
        super().__init__(id, rfid_tag, employee_id, card_status_id)
        self.access_level = access_level
        