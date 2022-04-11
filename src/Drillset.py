from Coordinate import Coordinate


class Drillset:
    def __init__(self, performers_coords, page, counts, notes=""):
        """
        @param performers_coords: Dictionary - String (performer label): Coordinate
        @param page: page number, Integer
        @param counts: number of counts in the set, Integer
        @param notes: any notes about the set to display, String
        """
        self.performers_coords = performers_coords
        self.page = page
        self.counts = counts
        self.notes = notes
    
    def get_coord(self, label):
        return self.performers_coords[label]

    def toDict(self):
        coords = { key: value.toDict() for (key, value) in self.performers_coords.items() }
        return {
            "performers_coords": coords,
            "page": self.page,
            "counts": self.counts,
            "notes": self.notes
        }

    def fromDict(dict):
        performers_coords = { key: Coordinate.fromDict(value) for (key, value) in dict["performers_coords"].items() }
        page = dict["page"]
        counts = dict["counts"]
        notes = dict["notes"]
        return Drillset(performers_coords, page, counts, notes)
