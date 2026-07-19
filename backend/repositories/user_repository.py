from backend.models.user import User
from backend.repositories.base import BaseRepository
from backend.schemas.auth import UserBase, UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User, UserCreate, UserBase]):
    async def get_by_username(
        self, session: AsyncSession, *, username: str
    ) -> User | None:
        result = await session.execute(
            select(self.model).filter(self.model.username == username)
        )
        return result.scalars().first()

    async def get_by_email(self, session: AsyncSession, *, email: str) -> User | None:
        result = await session.execute(
            select(self.model).filter(self.model.email == email)
        )
        return result.scalars().first()


user_repo = UserRepository(User)
