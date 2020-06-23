from database import SQLite
from errors import ApplicationError

class VA(object):

    def __init__(self, name, image, va_id=None, mapped_names=None, mapped_images=None, path=None):
        self.va_id = va_id
        self.name = name
        self.image = image
#        self.characters = characters
#        self.anime = anime
        self.mapped_names = mapped_names
        self.mapped_images = mapped_images
        self.path = path

    def to_dict(self):
        va_data = self.__dict__
        return va_data

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
        
        query = "{} INTO VAs {} VALUES {}"
        
        if self.va_id == None:
            query = query.format("INSERT", "(name, image)", "(?, ?)")
            args = (self.name, self.convertToBinaryData(self.image))
        else:
            query = query.format("REPLACE", "(VA_id, name, image)", "(?, ?, ?)")
            args = (self.va_id, self.name, self.convertToBinaryData(self.image))
        
        path = "./templates/images" + self.name + ".jpg"
        self.writeTofile(self.convertToBinaryData(self.image), path)
        
        with SQLite() as db:
            cursor = db.execute(query, args)
            self.va_id = cursor.lastrowid
        return self

    @staticmethod
    def delete(name):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM VAs WHERE name = ?", name)
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)



    @staticmethod
    def find_by_name(name):
        result = None
        mapped_names = {} 
        mapped_images = {}
        
        with SQLite() as db:
            result = db.execute(
                    "SELECT * FROM VAs WHERE name = ?", name)
        va = result.fetchone()
        if va is None:
            raise ApplicationError(
                    "No character found", 404)
                    
        with SQLite() as db:
            characters = db.execute("SELECT characters.name, characters.image FROM VAs JOIN characters ON VAs.name = characters.VA WHERE VAs.name = ?", name).fetchall()
            
            anime = db.execute("SELECT anime.title, anime.image FROM VAs JOIN characters ON VAs.name = characters.VA JOIN anime ON anime.title = characters.anime WHERE VAs.name = ?", name).fetchall()
        
        f = 0
        
        for i, j in zip(characters, anime):
            for i1, j1 in zip(i, j):
                if f == 1:
                    mapped_images[i1] = j1
                    break
                mapped_names[i1] = j1
                f = 1
        
        filename = ''.join(name)
        path = "./images/" + filename + ".jpg" 
        
        return VA(*va, mapped_names, mapped_images, path)
    
    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT * FROM VAs").fetchall()
            return [VA(*row) for row in result]

