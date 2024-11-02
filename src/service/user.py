import bcrypt
from fastapi import Depends

from src.models.repository import UserRepository
from src.models.user import User


class UserService:
    def __init__(self, user_repo: UserRepository = Depends(UserRepository)):
        self.encoding = "UTF-8"
        self.user_repo = user_repo

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding), hashed_password.encode(self.encoding)
        )

    async def get_user_info(self, user_id: int) -> User:
        return await self.user_repo.get_user_by_id(user_id=user_id)
