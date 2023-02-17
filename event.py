class Event:
    def __init__(self, obj1, obj2, collision_time, v1, v2):
        self.obj1 = obj1 # Только Атом
        self.obj2 = obj2 # Атом или бокс
        self.time = collision_time
        self.newv1 = v1
        self.newv2 = v2
            # Событие между двумя объектами и их новые скорости