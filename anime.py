from database import SQLite
from errors import ApplicationError


class Anime(object):
    
    def __init__(self, title, image, studio, episodes, seasons, anime_id=None, mapped_names=None, mapped_images=None):
        self.anime_id = anime_id
        self.title = title
        self.image = image
        self.studio = studio
        self.episodes = episodes
        self.seasons = seasons
#        self.characters = characters
#        self.VAs = VAs
        self.mapped_names = mapped_names
        self.mapped_images = mapped_images
        
    def to_dict(self):
        return self.__dict__

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
        query = "{} INTO anime {} VALUES {}"
    
        if self.anime_id == None:
            query = query.format("INSERT", "(title, image, studio, episodes, seasons)", "(?, ?, ?, ?, ?)")
            args = (self.title, self.convertToBinaryData(self.image), self.studio, self.episodes, self.seasons) 
        else:
            query = query.format("REPLACE", "(anime_id, title, image, studio, episodes, seasons)", "(?, ?, ?, ?, ?, ?)")
            args = (self.anime_id, self.title, self.convertToBinaryData(self.image), self.studio, self.episodes, self.seasons)
        
        path = "./templates/images" + self.title + ".jpg"
        self.writeTofile(self.convertToBinaryData(self.image), path)
        
        with SQLite() as db:
            cursor = db.execute(query, args)
            self.anime_id = cursor.lastrowid
        return self

    @staticmethod
    def delete(title):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM anime WHERE title = ?", title)
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)

    @staticmethod
    def find_by_title(title):
        result = None
        mapped_names = {}
        mapped_images = {}
        
        with SQLite() as db: 
                result = db.execute("SELECT * FROM anime WHERE title = ?", title)
                        
        anime = result.fetchone()
        
        if anime is None:
            raise ApplicationError(
                    "Anime not found", 404)
        
        with SQLite() as db:
            characters = db.execute("SELECT characters.name, characters.image FROM anime JOIN characters ON anime.title = characters.anime WHERE title = ?", title).fetchall()

#            characters = db.execute("SELECT characters.name, characters.image FROM characters WHERE anime = ?", title).fetchall()
            
            VAs = db.execute("SELECT VAs.name, VAs.image FROM anime JOIN characters ON anime.title = characters.anime JOIN VAs ON VAs.name = characters.VA WHERE title = ?", title).fetchall()
        
        f = 0
        
        for i, j in zip(characters, VAs):
            for i1, j1 in zip(i, j):
                if f == 1:
                    mapped_images[i1] = j1
                    break
                mapped_names[i1] = j1
                f = 1
        
        return Anime(*anime, mapped_names, mapped_images)
    
    @staticmethod
    def find_by_studio(studio):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT * FROM anime WHERE studio = ?",
                    (studio,))
        
        anime = result.fetchall()
        if anime is None:
            raise ApplicationError(
                    "Anime not found", 404)
        return anime
    
    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT * FROM anime").fetchall()
            return [Anime(*row) for row in result]

