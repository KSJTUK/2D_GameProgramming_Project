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


def remove_object(object):
    for layer in game_objects:
        if object in layer:
            layer.remove(object)
            return
    # 지우려는 오브젝트가 월드내에 없다면 경고 발생
    raise ValueError('Try to delete Not exist object')

def clear():
    for layer in game_objects:
        layer.clear()
