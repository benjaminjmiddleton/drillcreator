class Drillset:
    def __init__(self, performers_coords, page, counts, notes=""):
        """
        @param performers_coords: Dictionary - Performer: Coordinate
        @param page: page number, String
        @param counts: number of counts in the set, Integer
        @param notes: any notes about the set to display, String
        """
        self.performers_coords = performers_coords
        self.page = page
        self.counts = counts
        self.notes = notes
    
    def get_coord(self, label):
        return self.performers_coords[label]