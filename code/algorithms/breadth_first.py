from .depth_first import DepthFirst #. gebruik je omdat het uit dezelfde folder komt. moet ivm main.py vanuit de root.

class BreadthFirst(DepthFirst):
    def get_next_station(self):
        return self.stack.pop(0)

        """ Resultaten laden kan heel lang duren, komt doordat het stapje voor
        stapje het ding afgaat en helemaal op het eind alles ineens naar buiten gooit"""