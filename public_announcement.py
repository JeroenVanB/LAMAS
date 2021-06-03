from enum import Enum

class AnnouncementType(Enum):
    card_played = 0
    does_not_have_suit = 1
    pass


class PublicAnnouncement:
    def __init__(self,sender,  announcement_type: AnnouncementType, card=None) -> None:
        self.sender = sender
        self.type = announcement_type
        self.card = card

