from passlib.context import CryptContext

class Hash:
    pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_pswd(password: str) -> str:
        return Hash.pswd_context.hash(password)

    def verify_hash(hashed_pswd: str, plain_pswd: str) -> bool:
        return Hash.pswd_context.verify(plain_pswd, hashed_pswd)