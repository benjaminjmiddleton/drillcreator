from Performer import Performer, INSTRUMENTS

class Show:
    def __init__(self, performers, drillsets=[]):
        """
        @param marchers: list of Performer objects that will be used in the show
        @param drillsets: list of drillsets the show will have
        """
        self.performers = performers
        self.drillsets = drillsets
    
    @staticmethod
    def load_performers(pf_file):
        performers = []
        pf_file = open(pf_file)
        for line in pf_file.readlines():
            line = line.split(' ')
            for i in range(0, int(line[1])):
                performers.append(Performer(line[0], i+1))
        return performers
    
    def insert_drillset(self, drillset, index):
        self.drillsets.insert(drillset, index)
        for i in range(index+1, len(self.drillsets)):
            self.drillsets[i].page += 1

    def toDict(self):
        return {
            "performers": [ p.toDict() for p in self.performers ],
            "drillsets": [ d.toDict() for d in self.drillsets ]
        }
