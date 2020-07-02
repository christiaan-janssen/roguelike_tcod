import tcod as libtcod

from game_messages import Message


class Fighter:
    def __init__(self, hp, defence, power):
        self.max_hp = hp
        self.hp = hp
        self.defence = defence
        self.power = power

    def take_damage(self, amount):
        result = []

        self.hp -= amount

        if self.hp <= 0:
            result.append({'dead': self.owner})

        return result

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defence

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            print(target)
            results.extend(target.fighter.take_damage(damage))
            #results.extend({'message': 'Whut?!'})

        else:
            results.append({'message': Message('{0} attacks {1} but does no damage'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})

        return results
