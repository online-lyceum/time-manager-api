from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import exc, select

from time_manager.db import tables
from time_manager.services.base import BaseService


class TgUserService(BaseService):
    async def get(self, tg_user_id: int, raise_exception: bool = True) -> tables.TgUser | None:
        query = select(tables.TgUser)
        query = query.filter_by(id=tg_user_id)
        tg_user = await self.session.scalar(query)
        if tg_user is None:
            if not raise_exception:
                return
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return tg_user

    async def get_list(self, user_id: int):
        query = select(tables.TgUser)
        query = query.filter_by(user_id=user_id)
        return await self.session.scalars(query)

    async def create(self, user_id: int, tg_user_id: int) -> tables.TgUser:
        tg_user = tables.TgUser(id=tg_user_id, user_id=user_id)
        self.session.add(tg_user)
        await self.session.commit()
        self.response.status_code = status.HTTP_201_CREATED
        return tg_user

    async def delete(self, tg_user_id: int):
        query = select(tables.TgUser)
        query = query.filter_by(id=tg_user_id)
        tg_user = await self.session.scalar(query)
        await self.session.delete(tg_user)
        await self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
