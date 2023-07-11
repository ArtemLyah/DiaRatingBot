from databases import Rusak
from loader import db_session
import aiofiles
import random
from typing import Tuple, Union

class RusakService():
    file_names = "data/rusak_names.txt"
    file_photos = "data/rusak_photos.txt"
    async def generate_rusak(self) -> dict:
        async with aiofiles.open(self.file_names, "r", encoding="utf-8") as f_names:
            async with aiofiles.open(self.file_photos, "r", encoding="utf-8") as f_photos:
                names = await f_names.readlines()
                photos = await f_photos.readlines()

        name_list = random.choice(names).split()
        name = random.choice(name_list)
        photo_id = random.randrange(1, len(photos))
        intellect = random.randint(0, 200)
        strength = random.randint(30, 300)
        rashism = random.randint(10, 100)
        health = random.randint(30, 100)
        return {
            "name" : name, 
            "photo_id" : photo_id, 
            "intellect" : intellect, 
            "strength" : strength, 
            "rashism" : rashism, 
            "health" : health
        }
    
    async def get_photo(self, photo_id) -> str:
        async with aiofiles.open(self.file_photos, "r") as f_photos:
            photos = await f_photos.readlines()
        if photo_id > len(photos):
            return None
        return photos[photo_id] 

    async def add_rusak(self, user_id) -> Tuple[Rusak, str]:
        stats = await self.generate_rusak()
        rusak = Rusak(user_id=str(user_id), **stats)
        db_session.add(rusak)
        db_session.commit()
        return rusak, await self.get_photo(stats["photo_id"])
    
    async def get_rusak(self, user_id) -> Tuple[Rusak, str]:
        rusak = db_session.query(Rusak)\
            .filter(Rusak.user_id == str(user_id))\
                .first()
        if not rusak:
            return None
        return rusak, await self.get_photo(rusak.photo_id)
    
    def delete_rusak(self, user_id) -> Union[None, Rusak]:
        rusak = db_session.query(Rusak)\
            .filter(Rusak.user_id == str(user_id))\
                .first()
        if not rusak:
            return None
        db_session.query(Rusak)\
            .filter(Rusak.user_id == str(user_id))\
                .delete()
        db_session.commit()
        return rusak