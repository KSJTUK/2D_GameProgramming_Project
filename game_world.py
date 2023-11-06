game_objects = [[] for _ in range(4)]

# 물리 세계 (충돌세계) 생성
collision_pairs = {}

def add_collision_pair(groub, object1=None, object2=None):
    if groub not in collision_pairs:
        print(f'Add new groub {groub}')
        collision_pairs[groub] = [[], []]
    if object1 and object1 not in collision_pairs[groub][0]:
        collision_pairs[groub][0].append(object1)
    if object2 and object2 not in collision_pairs[groub][1]:
        collision_pairs[groub][1].append(object2)


def remove_collision_object(object):
    for pairs in collision_pairs.values():
        if object in pairs[0]:
            pairs[0].remove(object)
        if object in pairs[1]:
            pairs[1].remove(object)

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
            remove_collision_object(object)
            del object
            return
    # 지우려는 오브젝트가 월드내에 없다면 경고 발생
    raise ValueError('Try to delete Not exist object')


def clear():
    for layer in game_objects:
        layer.clear()


def collide_aabb(object1, object2):
    left_a, bottom_a, right_a, top_a = object1.get_bb()
    left_b, bottom_b, right_b, top_b = object2.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def handle_collision():
    for groub, pairs in collision_pairs.items():
        for object1 in pairs[0]:
            for object2 in pairs[1]:
                if collide_aabb(object1, object2):
                    object1.handle_collision(groub, object2)
                    object2.handle_collision(groub, object1)
