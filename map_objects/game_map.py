import tcod as libtcod
from typing import List
from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter

from entity import Entity
from item_functions import heal, cast_lightning, cast_fireball
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from render_functions import RenderOrder
from components.item import Item
from game_messages import Message


class GameMap:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self) -> List[List[Tile]]:
        """Initialize the map with wall tiles"""
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def make_map(self, max_rooms: int, room_min_size: int, room_max_size: int,
                map_width: int, map_height: int, player, entities,
                max_monsters_per_room, max_items_per_room) -> None:
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Random position without going out of the bounds of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
                # paint it to the map
                self.create_room(new_room)

                # Center coords of the new room
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first
                    # connect it to the previous room with a tunnel

                    # center coords of previous room
                    (prev_x, prev_y) = rooms[num_rooms -1].center()

                    # flip a coin (random number that 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # First move vertically
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

            # Add some monsters
            self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1

    def create_room(self, room: Rect) -> None:
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1: int, x2: int, y: int) -> None:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1: int, y2: int, x: int) -> None:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                fighter_component = Fighter(hp=10, defence=0, power=3)
                ai_component = BasicMonster()

                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                else:
                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_chance = randint(0, 100)

                if item_chance < 70:
                    item_component = Item(use_function=heal, amount=4)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                            item=item_component)
                elif item_chance < 85:
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                            'Left-click a target tile for the fireball, or right_click to cancel.', libtcod.light_cyan),
                            damage=12, radius=3)
                    item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM, item=item_component)
                else:
                    item_component = Item(use_function=cast_lightning, damage=20, maximum_range=5)
                    item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                            item=item_component)

                entities.append(item)


    def is_blocked(self, x: int, y: int) -> bool:
        """Check to see if the tile at x@y is blocking or not"""
        if self.tiles[x][y].blocked:
            return True

        return False
