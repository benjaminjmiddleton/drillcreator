class Show:
    def __init__(self, performers, drillsets):
        """
        @param marchers: list of Performer objects that will be used in the show
        @param drillsets: list of drillsets the show will have (can be empty for construction)
        """
        self.performers = performers
        self.drillsets = drillsets