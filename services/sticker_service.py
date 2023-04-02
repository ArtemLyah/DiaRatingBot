from databases.models import Stickers
from loader import db_session

class StickerService():
    def add_sticker(self, file_id, rating):
        sticker = Stickers(file_id=file_id, rating=rating)
        db_session.add(sticker)
        db_session.commit()
        
    def delete_sticker(self, file_id):
        sticker = self.get_sticker_by_fid(file_id)
        db_session.delete(sticker)
        db_session.commit()

    def get_stickers(self) -> list[Stickers]:
        return db_session.query(Stickers).all()
    
    def get_sticker_by_fid(self, file_id):
        return db_session.query(Stickers).filter(Stickers.file_id == file_id).first()

    def is_sticker_in_set(self, file_id):
        return bool(self.get_sticker_by_fid(file_id))

