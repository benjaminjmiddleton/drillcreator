from Drillset import Drillset
from Performer import Performer, INSTRUMENTS

class Show:
    def __init__(self, performers, drillsets=[]):
        """
        @param marchers: list of Performer objects that will be used in the show
        @param drillsets: list of drillsets the show will have
        """
        self.performers = performers
        self.drillsets = drillsets
    
    def insert_drillset(self, drillset, index):
        self.drillsets.insert(drillset, index)
        for i in range(index+1, len(self.drillsets)):
            self.drillsets[i].page += 1

    def toDict(self):
        return {
            "performers": [ p.toDict() for p in self.performers ],
            "drillsets": [ d.toDict() for d in self.drillsets ]
        }

    def fromDict(dict, performers_only=False):
        performers = [ Performer.fromDict(p) for p in dict["performers"] ]
        if not performers_only:
            drillsets = [ Drillset.fromDict(d) for d in dict["drillsets"] ]
            return Show(performers, drillsets)
        else:
            return Show(performers)