import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from app import models
from app.utils.hash import Hash
from app.user.schemas import User
import enum
from typing import ClassVar
import geocoder

cred = credentials.Certificate("D:\e-hab\\app\\resources\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

class Enum(enum.Enum):
    Users = "Users"
    Facilitator = "Faciliotators"
    SupportGroups = "SupportGroups"
    RehabCentres = "RehabCentres"


class CRUD(BaseModel):
    db: ClassVar[firestore.client] = firestore.client()

    @classmethod
    def add_User(self, document: dict) -> dict:
        """
            document: {name, username, email, password, contact_no}
        """

        if CRUD.get_User_by_email(document["email"]):
            return {"error": "User with same email already exists!"}
        if CRUD.get_User_by_username(document["username"]):
            return {"error": "Username already taken"}
        
        document["password"] = Hash.hash_pswd(document["password"])
        document["latitude"] = geocoder.ip("me").latlng[0]
        document["longitude"] = geocoder.ip("me").latlng[1]

        CRUD.db.collection("Users").add(document)
        return document
    
    
    @classmethod
    def add_Facilitator(self, document: dict) -> dict:
        """
            document: {username}
        """

        CRUD.db.collection(Enum.Facilitator).add(document)
        return document
    

    @classmethod
    def add_SupportGroups(self, document: dict) -> dict:
        """
            document: {name, email, contact_no}
        """

        CRUD.db.collection(Enum.SupportGroups).add(document)
        return document
    

    @classmethod
    def add_RehabCentres(self, document: dict) -> dict:
        """
            document: {name, email, contact_no}
        """

        CRUD.db.collection(Enum.RehabCentres).add(document)
        return document
    

    @classmethod
    def get_User_by_email(self, email: str) -> models.Users:
        res = CRUD.db.collection("Users").where("email", "==", email).get()
        for users in res:
            user = models.Users(id=users.id, **users.to_dict())
            return user
        return None
    

    @classmethod
    def get_User_by_username(self, username: str) -> models.Users:
        res = CRUD.db.collection("Users").where("username", "==", username).get()
        for users in res:
            user = User(id=users.id, **users.to_dict())
            return user
        return None
