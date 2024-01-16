class Station:
    
    def __init__(self, id, name, latitude, longitude) -> None:
        """
        Initialize a station as an object with an id, coordinates and a name

        post: Initialized station object and empty list of connections
        """
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.connections = []

    def add_connection(self, connection, distance) -> None:
        """
        Add connection to station object

        post: Initialized station object and empty list of connections
        """
        self.connections.append((connection, distance))
    
    def __str__(self):
        return f"{self.name}"
