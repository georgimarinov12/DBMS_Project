from database import SQLite
from errors import ApplicationError

class Character(object):

    def __init__(self, name, image, anime, VA, character_id=None):
        self.char_id = character_id
        self.name = name
        self.anime = anime
        self.VA = VA
        self.image = image

    def to_dict(self):
        char_data = self.__dict__
        return char_data

    def convertToBinaryData(self, filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        file.close()
        return blobData

    def writeTofile(self, data, filename):
        with open(filename, 'wb') as file:
            file.write(data)
        file.close()

    def save(self):
        query = "{} INTO characters {} VALUES {}"
        
        if self.char_id == None:
            query = query.format("INSERT", "(name, image, anime, VA)", "(?, ?, ?, ?)")
            args = (self.name, self.convertToBinaryData(self.image), self.anime, self.VA)
        else:
            query = query.format("REPLACE", "(character_id, name, image, anime, VA)", "(?, ?, ?, ?, ?)")
            args = (self.char_id, self.name, self.convertToBinaryData(self.image), self.anime, self.VA)
        
        path = "./templates/images" + self.name + ".jpg"
        self.writeTofile(self.convertToBinaryData(self.image), path)
        
        with SQLite() as db:
            cursor = db.execute(query, args)
            self.char_id = cursor.lastrowid
        return self

    @staticmethod
    def delete(name):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM characters WHERE name = ?", name)
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)

    @staticmethod
    def find_by_anime(anime):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT * FROM characters WHERE anime = ?", anime)
        characters = result.fetchall()
        if characters is None:
            raise ApplicationError(
                    "No characters found", 404)
        return [Character(*row) for row in characters]

    @staticmethod
    def find_by_name(name):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT * FROM characters WHERE name = ?", name)
        character = result.fetchone()
        if character is None:
            raise ApplicationError(
                    "No character found", 404)
        return Character(*character)
    
    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT * FROM characters").fetchall()
            return [Character(*row) for row in result]

