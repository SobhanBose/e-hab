from app.facilitator.schemas import Facilitator

class showFacilitator(Facilitator):
    class Config():
        orm_mode = True