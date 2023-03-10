from app.support_groups.schemas import supportGroups

class showSupportGroups(supportGroups):
    name: str
    facilitator: str
    latitude: float
    longitude: float

    class Config():
        orm_mode = True