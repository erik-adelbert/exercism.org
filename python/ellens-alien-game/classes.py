"""Solution to Ellen's Alien Game exercise."""


class Alien:
    """An Alien object has location x_coordinate and y_coordinate.

    Attributes
    ----------
    (class)total_aliens_created: int
    x_coordinate: int - Position on the x-axis.
    y_coordinate: int - Position on the y-axis.
    health: int - Number of health points.

    Methods
    -------
    hit(): Decrement Alien health by one point.
    is_alive(): Return a boolean for if Alien is alive (if health is > 0).
    teleport(new_x_coordinate, new_y_coordinate): Move Alien object to new coordinates.
    collision_detection(other): Implementation TBD.
    """

    total_aliens_created = 0

    def __init__(self, xpos, ypos):
        self.x_coordinate = xpos
        self.y_coordinate = ypos
        self.health = 3

        Alien.total_aliens_created += 1

    def hit(self):
        """
        hit decrements the alien's health
        """

        self.health -= 1

    def is_alive(self):
        """
        is_alive checks if the alien has health left in it
        """
        return self.health > 0

    def teleport(self, xpos, ypos):
        """
        teleport changes the alien's coordinates according to `xpos` and `ypos`
        """
        self.x_coordinate = xpos
        self.y_coordinate = ypos

    def collision_detection(self, other):
        """
        collision_detection TBD
        """


def new_aliens_collection(start_positions):
    """
    new_aliens_collection creates a list of Alien() objects,
    given a list of positions (as tuples)
    """

    return list(map(lambda pos: Alien(pos[0], pos[1]), start_positions))
