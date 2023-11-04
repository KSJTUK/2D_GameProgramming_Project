game_objects = [[] for _ in range(4)]


def add_object(object, layer):
    game_objects[layer].append(object)


def update():
    for layer in game_objects:
        for object in layer:
            object.update()


def render():
    for layer in game_objects:
        for object in layer:
            object.render()

def clear():
    game_objects.clear()