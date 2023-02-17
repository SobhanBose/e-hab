from app.support_groups.schemas import supportGroups

class showSupportGroups(supportGroups):
    facilitator: str
    class Config():
        orm_mode = True