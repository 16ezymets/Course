class Event:
    # Событие между двумя объектами и их новые скорости

    def __init__(self, obj1, obj2, collision_time, v1, v2):
        self.obj1 = obj1  # Только Атом
        self.obj2 = obj2  # Атом или стенка
        self.time = collision_time
        self.newv1 = v1
        self.newv2 = v2
