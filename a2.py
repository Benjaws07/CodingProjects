# DO NOT modify or add any import statements
from support import *
from display import HearthView

# Name: Benjamin Tze Chien Law
# Student Number: S49270446
# Favorite Building: Sydney Opera House
# ----------------------------------------------------------------------------

# Define your classes and functions here


class Card():
    def __init__(self, **kwargs):
        self._name = CARD_NAME
        self._desc = CARD_DESC
        self._symbol = CARD_SYMBOL
        self._cost = 1
        self._effect = {}
        self._is_permanent = False

    def __str__(self) -> str:
        """
        Returns the card name and card description

        Parameters:

        returns:
        card name and card description
        """
        return f"{self._name}: {self._desc}"

    def __repr__(self) -> str:
        """
        Returns attributes that make up a card

        Parameters:

        returns:
        attributes of the card

        """
        return (f"{self.__class__.__name__}()")

    def get_symbol(self) -> str:
        """
        Returns the card symbol of a single character

        Parameters:

        returns:
        Symbol of the card
        """
        return self._symbol

    def get_name(self) -> str:
        return self._name

    def get_cost(self) -> int:
        return self._cost

    def get_effect(self) -> dict[str, int]:
        return self._effect.copy()

    def is_permanent(self) -> bool:
        return self._is_permanent


class Shield(Card):
    def __init__(self, **kwargs):
        """
        Set default values of shield cards

        Parameters:

        returns:

        """
        super().__init__(**kwargs)
        self._name = SHIELD_NAME
        self._desc = SHIELD_DESC
        self._symbol = SHIELD_SYMBOL
        self._cost = 1
        self._effect = {SHIELD: 5}
        self._is_permanent = False


class Heal(Card):
    def __init__(self, **kwargs):
        """
        Set default values of the card

        Parameters:

        returns:

        """
        super().__init__(**kwargs)
        self._name = HEAL_NAME
        self._desc = HEAL_DESC
        self._symbol = HEAL_SYMBOL
        self._cost = 2
        self._effect = {HEALTH: 2}
        self._is_permanent = False


class Fireball(Card):
    """
    Fireball is a card that applies 3 damage to a target entity 
    plus 1 point of additional damage for 
    each turn they have spent in a hero’s hand.
    Fireball cards cost 3. 
    These cards are not represented by a single letter,
    but instead their symbol is the number of turns they have spent in hand.
    """

    def __init__(self, turns_in_hand, **kwargs):
        """
        Set default values of the card

        Parameters:

        """
        super().__init__(effect=None, permanent=False)
        self._name = FIREBALL_NAME
        self._desc = FIREBALL_DESC
        self._cost = 3
        self._symbol = f'{int(turns_in_hand)}'
        self._turns_in_hand = turns_in_hand
        self._effect = {DAMAGE: 3 + self._turns_in_hand}

    def __str__(self) -> str:
        return (
            f"{self._name}: {self._desc} Currently dealing "
            f"{3 + self._turns_in_hand} damage."
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self._turns_in_hand})"

    def increment_turn(self):
        self._turns_in_hand += 1
        self._symbol = str(self._turns_in_hand)
        self._effect = {DAMAGE: 3 + self._turns_in_hand}

    def get_symbol(self) -> str:
        return self._symbol

    def get_cost(self) -> int:
        return self._cost

    def get_effect(self) -> dict[str, int]:
        return {DAMAGE: 3 + self._turns_in_hand}


class CardDeck():

    def __init__(self, cards: list[Card]):
        """
        Initialise a deck of cards containing the given cards.
        Cards are provided in order,
        with the first card in the list being the topmost card of the deck,
        and the last card in the list being the bottom most card of the deck.
        """
        self._cards = cards.copy()

    def __str__(self) -> str:
        """
        Returns a comma separated list of the symbols 
        representing each card in the deck.
        Symbols should appear in order, from top to bottom.
        """
        symbols = [str((card.get_symbol()))for card in self._cards]
        return ','.join(symbols)

    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into
        a REPL to construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}({repr(self._cards)})"

    def is_empty(self) -> bool:
        """
        Returns if this CardDeck is empty or not.
        """
        return not self._cards

    def remaining_count(self) -> int:
        """
        Returns how many cards are currently in this CardDeck.
        """
        return len(self._cards)

    def draw_cards(self, num: int) -> list[Card]:
        """
        Draws the specified number of cards from the top of the deck.
        Cards should be returned in the order they are drawn.
        If there are not enough cards remaining in the deck,
        as many cards as possible should be drawn.
        """
        if not self._cards:
            return []
        drawn_cards = self._cards[:num]
        self._cards = self._cards[num:]
        return drawn_cards

    def add_card(self, card: Card):
        """
        Adds the given card to the bottom of the deck.
        """
        self._cards.append(card)


class Entity():
    """
    Entity is an abstract class from 
    which all instantiated types of entity inherit.

    This class provides default entity behavior,
    which can be inherited or overridden by specific types of entities.

    Each entity has a health and shield value,
    and are alive if and only if their health value is above 0.

    """

    def __init__(self, health: int, shield: int):
        """
        Initialise a new entity with the given health and shield value.
        """
        super().__init__()
        self._health = max(0, health)
        self._shield = max(0, shield)

    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL
        to construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}({self._health}, {self._shield})"

    def __str__(self) -> str:
        """
        Returns this hero’s health and shield, comma separated.
        """
        return f"{self._health},{self._shield}"

    def get_health(self) -> int:
        """
        Returns this entity’s health.
        """
        return self._health

    def get_shield(self) -> int:
        """
        Returns this entity’s shield.
        """
        return self._shield

    def apply_shield(self, shield: int):
        """
        Applies the given amount of shield.
        """
        if shield < 0:
            return self._shield
        self._shield += shield
        return self._shield

    def apply_health(self, health: int):
        """
        Applies the given amount of health.
        """
        if health < 0:
            return
        self._health += health

    def apply_damage(self, damage: int):
        """
        Applies the given amount of damage.
        The entity’s health never drops below 0 and 
        any excess damage is discarded.
        """
        print(
            f"Applying {damage} damage to {self}, before: health={self._health}, shield={self._shield}")
        if damage <= 0:
            return self._health
        if self._shield >= damage:
            self._shield -= damage
        else:
            remaining = damage - self._shield
            self._shield = 0
            self._health = max(0, self._health - remaining)
        self._shield = max(0, self._shield)
        self._health = max(0, self._health)
        print(f"After: health={self._health}, shield={self._shield}")
        return self._health

    def is_alive(self) -> bool:
        """
        Returns if this entity is alive or not.
        """
        return self._health > 0


class Hero(Entity):
    def __init__(self, health: int, shield: int, max_energy: int,
                 deck: CardDeck, hand: list[Card]):
        """
        Instantiate a new Hero with the given health,
        shield, energy_capacity, deck, and hand.
        """
        super().__init__(health, shield)
        self._hand_size = MAX_HAND
        self._energy_capacity = max_energy
        self._energy = max_energy
        self._deck = deck
        self._hand = list(hand)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self._health}, {self._shield}, {self._energy_capacity}, "
            f"{repr(self._deck)}, {repr(self._hand)})"
        )

    def __str__(self) -> str:
        """
        Returns a string containing the following:
        This hero’s health, shield, and energy capacity,
        comma separated; followed by a semi-colon;
        followed by the string representation of this hero’s deck;
        followed by another semicolon;
        followed finally by the symbols of each card
        in this heros hand in order, comma separated.
        """
        # return f"Hero(hp={self.get_health()}),(shield={self.get_shield()})"
        status = f"{self._health},{self._shield},{self._energy_capacity}"
        deck_str = str(self._deck)
        hand_str = ','.join(str(card.get_symbol()) for card in self._hand)
        return f"{status};{deck_str};{hand_str}"

    def get_energy(self) -> int:
        """
        Returns this hero’s current energy level.
        """
        return self._energy

    def spend_energy(self, energy: int) -> bool:
        """
        Attempts to spend the specified amount of this hero’s energy.
        If this hero does not have sufficient energy, then nothing happens.
        Returns whether the energy was spent or not.
        """
        if energy <= 0:
            return False
        if self._energy >= energy:
            self._energy -= energy
            return True
        return False

    def get_max_energy(self) -> int:
        """
        Returns this hero’s energy capacity.
        """
        return self._energy_capacity

    def get_deck(self) -> CardDeck:
        """
        Returns this hero’s deck.
        """
        return self._deck

    def get_hand(self) -> list[Card]:
        """
        Returns this hero’s hand, in order.
        """
        return self._hand

    def get_hand_size(self) -> int:
        """
        Returns the maximum hand size for this hero.
        """
        return self._hand_size

    def is_alive(self) -> bool:
        return self._health > 0 and not self._deck.is_empty()

    def new_turn(self):
        """
        Registers a new turn of all fireball cards in this hero’s hand,
        draws from their deck into their hand,
        expands their energy capacity by 1,
        and refills their energy level
        """

        for card in self._hand:
            if isinstance(card, Fireball):
                card.increment_turn()

        draw_n = self._hand_size - len(self._hand)
        if draw_n > 0:
            drawn = self._deck.draw_cards(draw_n)
            self._hand.extend(drawn)

        self._energy_capacity += 1
        self._energy = self._energy_capacity


class Minion(Card, Entity):
    def __init__(self, health: int, shield: int):
        """
        Instantiate a new Minion with the specified health and shield value.
        """
        # Call out the values from the base classes
        Card.__init__(self)
        Entity.__init__(self, health, shield)
        # Set the approriate default values for minion cards
        self._name = MINION_NAME
        self._desc = MINION_DESC
        self._symbol = MINION_SYMBOL
        self._cost = 2
        self._effect = {}
        self._is_permanent = True

    def __repr__(self) -> str:
        """
        Returns output according to Entity parent class.
        """
        return Entity.__repr__(self)

    def __str__(self) -> str:
        """
        Returns the name and description of this card
        """
        # return (f"Minion({self.__class__.__name__},hp={self.get_health()} ,"
        #         f"shield={self.get_shield()})")
        return Card.__str__(self)

    def choose_target(self, ally_hero: Entity, enemy_hero: Entity,
                      ally_minions: list[Entity],
                      enemy_minions: list[Entity]) -> Entity:
        """
        Select this minion’s target out of the given entities.
        Note that here, the allied hero and
        minions will be those friendly to this minion,
        not neccessarily to the player.
        This logic extends to the specified enemy hero and minions.
        Minions should be provided in the order they appear
        in their respective minion slots,
        from left to right.
        """
        effect = self.get_effect()
        if DAMAGE in effect:
            return enemy_hero
        return self

    def summon(self) -> 'Minion':
        new_minion = self.__class__(1, 0)
        # print(f"Summoned new minion: {new_minion}")
        return new_minion


class Wyrm(Minion):
    """
    A Wyrm is a minion that has 2 cost, 
    is represented by the symbol W, 
    and whose effect is to apply 1 heal and 1 shield.
    When selecting a target entity, a Wyrm will choose the 
    allied entity with the lowest health.
    If multiple entities have the lowest health,
    if one of the tied entities is the allied hero,
    the allied hero should be selected.
    Otherwise, the leftmost tied minion should be selected.
    """

    def __init__(self, health: int, shield: int):
        super().__init__(health, shield)
        self._name = WYRM_NAME
        self._desc = WYRM_DESC
        self._symbol = WYRM_SYMBOL
        self._cost = 2
        self._effect = {HEALTH: 1, SHIELD: 1}
        self._is_permanent = True

    def choose_target(self, ally_hero: Entity, enemy_hero: Entity,
                      ally_minions: list[Entity],
                      enemy_minions: list[Entity]) -> Entity:
        combatants = [ally_hero] + ally_minions
        if not combatants:
            return ally_hero
        # Step 1: Find target with minimum health
        min_health = min(ent.get_health() for ent in combatants)

        # Step 2: Get all with minimum health
        lowest_health_entities = [ent for ent in combatants
                                  if ent.get_health() == min_health]

        # Step 3: Prefer heroes over minions
        if ally_hero in lowest_health_entities:
            print(f"Wyrm targeting ally hero {ally_hero}")
            return ally_hero
        else:
            print(f"Wyrm targeting minion {lowest_health_entities[0]}")
            return lowest_health_entities[0]

    def summon(self) -> 'Wyrm':
        new_minion = self.__class__(1, 0)
        # print(f"Summon a new minion {new_minion}")
        return new_minion


class Raptor(Minion):
    def __init__(self, health: int, shield: int):
        super().__init__(health, shield)
        self._name = RAPTOR_NAME
        self._desc = RAPTOR_DESC
        self._symbol = RAPTOR_SYMBOL
        self._cost = 2
        # self._effect = {}
        self._is_permanent = True

    def __repr__(self) -> str:
        return Entity.__repr__(self)

    def get_effect(self):
        return {DAMAGE: self.get_health()}

    def choose_target(self, ally_hero: Entity, enemy_hero: Entity,
                      ally_minions: list[Entity],
                      enemy_minions: list[Entity]) -> Entity:
        if enemy_minions:
            # Finds minion with highest health
            max_health = max(m.get_health() for m in enemy_minions)
            # Returns the leftmost minion with that health
            for m in enemy_minions:
                if m.get_health() == max_health:
                    return m
        return enemy_hero

    def summon(self) -> 'Raptor':
        new_minion = self.__class__(1, 0)
        # print(f"Summon new minion: {new_minion}")
        return new_minion


class HearthModel():
    def __init__(self, player: Hero, active_player_minions: list[Minion],
                 enemy: Hero, active_enemy_minions: list[Minion]):
        """
        Instantiates a new HearthModel using the
        given player, enemy, and active minions.
        Each respective list of minions is given in the order
        they appear in their corresponding minion slots, from left to right.
        """
        self._player = player
        self._active_player_minions = active_player_minions
        self._enemy = enemy
        self._active_enemy_minions = active_enemy_minions

    def __str__(self) -> str:
        """
        Return the following in order, separated by the pipe character (|):
        The string representation of the player’s hero;
        a semicolon separated list of the players active minions
        (symbol, health, and shield, comma separated);
        the string representation of the enemy hero;
        and a semicolon separated list of the active enemy minions
        (symbol, health, and shield, comma separated).
        """
        player_str = str(self._player)
        player_minions = ';'.join(
            f"{m.get_symbol()},{m.get_health()},{m.get_shield()}"
            for m in self._active_player_minions)
        enemy_str = str(self._enemy)
        enemy_minions = ';'.join(
            f"{m.get_symbol()},{m.get_health()},{m.get_shield()}"
            for m in self._active_enemy_minions)
        return (
            f"{player_str}|"
            f"{player_minions if player_minions else ''}|"
            f"{enemy_str}|"
            f"{enemy_minions if enemy_minions else ''}"
        )

    def __repr__(self) -> str:
        """
        Returns a string which could be copied
        and pasted into a REPL to construct
        a new instance identical to self.
        """
        return (
            f"{self.__class__.__name__}("
            f"{repr(self._player)}, "
            f"{repr(self._active_player_minions)}, "
            f"{repr(self._enemy)}, "
            f"{repr(self._active_enemy_minions)})"
        )

    def get_player(self) -> Hero:
        """
        Return this model’s player hero instance.
        """
        return self._player

    def get_enemy(self) -> Hero:
        """
        Return this model’s enemy hero instance.
        """
        return self._enemy

    def get_player_minions(self) -> list[Minion]:
        """
        Return the player’s active minions.
        Minions should appear in order from leftmost minion
        slot to rightmost minion slot.
        """
        return self._active_player_minions.copy()

    def get_enemy_minions(self) -> list[Minion]:
        """
        Return the enemy’s active minions.
        Minions should appear in order from leftmost minion
        slot to rightmost minion slot.
        """
        return self._active_enemy_minions.copy()

    # 5. Win/Loss conditions
    def has_won(self) -> bool:
        """
        Return true if and only if the player has won the game.
        """
        return self._player.is_alive() and (
            not self._enemy.is_alive() or
            self._enemy.get_deck().is_empty())

    def has_lost(self) -> bool:
        """
        Return true if and only if the player has lost the game.
        """
        # return not self._player.is_alive()
        return not self._player.is_alive()

    def _apply_effects(self, target: Entity, effects: dict[str, int]):
        """
        Applies effects based on the status of target
        """
        # print(f"Applying effects {effects} to target {target}")

        for effect, amount in effects.items():
            if amount <= 0:
                continue
            if effect == DAMAGE and target.is_alive():
                target.apply_damage(amount)
            elif effect == SHIELD:
                # print(
                #     f"Applying {amount} shield to {target}, had {target.get_shield()} shield")
                target.apply_shield(amount)
                # print(f"Now {target.get_shield()} shield")
            elif effect == HEALTH:
                # print(
                #     f"Applying {amount} health to {target}, had {target.get_health()} health")
                target.apply_health(amount)
                # print(f"Now has {target.get_health()} health")

    def _cleanup_minions(self):
        """
        Removes dead minions when checking whether its alive or not
        """
        # print("CLEANUP: Player minions before:", [
        #       (id(m), m.get_symbol(), m.get_health()) for m in self._active_player_minions])
        # print("CLEANUP: Enemy minions before:", [
        #       (id(m), m.get_symbol(), m.get_health()) for m in self._active_enemy_minions])
        self._active_player_minions = [
            m for m in self._active_player_minions if m.is_alive()]
        self._active_enemy_minions = [
            m for m in self._active_enemy_minions if m.is_alive()]
        # print("CLEANUP: Player minions after:", [
        #       (id(m), m.get_symbol(), m.get_health()) for m in self._active_player_minions])
        # print("CLEANUP: Enemy minions after:", [
        #       (id(m), m.get_symbol(), m.get_health()) for m in self._active_enemy_minions])

    # 6. Play a card for the player

    def play_card(self, card: Card, target: Entity) -> bool:
        """
        Attempts to play the specified card on the player’s behalf.
        Returns whether the card was successfully played or not.
        The target argument will be ignored if the specified card is permanent.
        If a minion is defeated, it should be removed from the game,
        and any remaining minions within the respective minion slots should be moved one slot left if able.
        """

        if card not in self._player.get_hand():
            return False
        if not card.is_permanent():
            if not isinstance(target, Entity) or not target.is_alive():
                return False
        if not self._player.spend_energy(card.get_cost()):
            return False
        # Remove *that* card from the real hand
        self._player.get_hand().remove(card)

        if card.is_permanent() and isinstance(card, Minion):
            # minion = card.summon()
            if len(self._active_player_minions) >= MAX_MINIONS:
                self._active_player_minions.pop(0)
            self._active_player_minions.append(card)
            # target ignored for permanents
            # self._apply_effects(self._player, card.get_effect())
        else:
            self._apply_effects(target, card.get_effect())
        # Clean up any dead minions
        self._cleanup_minions()
        # print(
        #     f"Player hero after: {self._player.get_health()}, {self._player.get_shield()}")
        # print(f"After playing card {card.get_name()}: {str(self)}")
        return True

    def discard_card(self, card: Card):
        """
        Discards the given card from the players hand.
        The discarded card should be added to
        the bottom of the player’s deck.
        """
        hand = self._player.get_hand()
        if card in hand:
            hand.remove(card)
            self._player.get_deck().add_card(card)

    def _minion_attack_phase(self, attackers: list[Minion],
                             ally_hero: Hero, enemy_hero: Hero,
                             ally_minions: list[Minion],
                             enemy_minions: list[Minion]) -> None:
        """
        Defines how the minion should attack when end of turn
        """
        # print("== START MINION ATTACK PHASE ==")
        # print("Attacker list:", [
        #       (id(m), m.get_symbol(), m.get_health(), m.get_shield()) for m in attackers])
        # print("Ally minions:", [
        #       (id(m), m.get_symbol(), m.get_health(), m.get_shield()) for m in ally_minions])
        # print("Enemy minions:", [
        #       (id(m), m.get_symbol(), m.get_health(), m.get_shield()) for m in enemy_minions])
        for minion in list(attackers):
            if not minion.is_alive():
                continue
            target = minion.choose_target(
                ally_hero=ally_hero,
                enemy_hero=enemy_hero,
                ally_minions=ally_minions,
                enemy_minions=enemy_minions
            )
            # if isinstance(minion, Raptor):
            #     print(
            #         f"[DEBUG] Raptor about to attack: {minion} -> Target: {target}")
            #     print(f"[DEBUG] Raptor effect: {minion.get_effect()}")
            #     print(
            #         f"[DEBUG] Target before: health={target.get_health()}, shield={target.get_shield()}")
            if target.is_alive():
                self._apply_effects(target, minion.get_effect())
                # print(
                #     f"AFTER EFFECTS: {target}: health={target.get_health()}, shield={target.get_shield()}")
        #         if isinstance(minion, Raptor):
        #             print(
        #                 f"[DEBUG] Target after: health={target.get_health()}, shield={target.get_shield()}")
        # #     # remove dead after player-minion attacks
        # self._cleanup_minions()
        # print("[DEBUG] Player minions after cleanup:", [(m.get_symbol(
        # ), m.get_health(), m.get_shield()) for m in self._active_player_minions])
        # print("[DEBUG] Enemy minions after cleanup:", [(m.get_symbol(
        # ), m.get_health(), m.get_shield()) for m in self._active_enemy_minions])

    def end_turn(self) -> list[str]:
        """
        Follows the instructions for the end turn command in Table 2,
        excluding the last instruction (saving the game to autosave.txt).
        Returns the names of the cards played by the enemy hero (in order).
        If a minion is defeated at any point,
        it should be removed from the game,
        and any remaining minions within the respective minion slots
        should be moved one slot left if able.
        If the enemy hero is not alive after it has drawn cards,
        it should not take a turn,
        and the player should not subsequently update its own status.
        """
        played = []

        # print("[DEBUG] Before player minion attack:",
        #       self._active_player_minions)
        # print("Player minions ids:", [id(m)
        #       for m in self._active_player_minions])
        # 1) Player's minions attack
        self._minion_attack_phase(
            attackers=self._active_player_minions,
            ally_hero=self._player,
            enemy_hero=self._enemy,
            ally_minions=self._active_player_minions,
            enemy_minions=self._active_enemy_minions
        )
        self._cleanup_minions()

        # print("[DEBUG] After player minion attack:",
        #       self._active_player_minions)
        # 2) Enemy hero start‑of‑turn
        self._enemy.new_turn()

        # game over, nothing more
        if not self._player.is_alive() or not self._enemy.is_alive():
            return played

        # 3) Enemy plays cards from hand (in order)
        #    a) Permanent cards (minions) fill slots 0–4, shifting if full
        #    b) Spells and non‑permanent effects
        # print(
        #     f"Enemy hero before: {self._enemy.get_health()}, {self._enemy.get_shield()}")
        i = 0
        while i < len(self._enemy.get_hand()):
            card = self._enemy.get_hand()[i]
            if not self._enemy.spend_energy(card.get_cost()):
                i += 1
                continue
            self._enemy.get_hand().remove(card)
            played.append(card.get_name())

            if card.is_permanent():
                if len(self._active_enemy_minions) >= MAX_MINIONS:
                    self._active_enemy_minions.pop(0)
                self._active_enemy_minions.append(card)
            else:
                effect = card.get_effect()
                if DAMAGE in effect and self._player.is_alive():
                    self._apply_effects(self._player, {DAMAGE: effect[DAMAGE]})
                if HEALTH in effect and self._enemy.is_alive():
                    self._apply_effects(self._enemy, {HEALTH: effect[HEALTH]})
                if SHIELD in effect and self._enemy.is_alive():
                    self._apply_effects(self._enemy, {SHIELD: effect[SHIELD]})
        # print(
        #     f"Enemy hero after: {self._enemy.get_health()}, {self._enemy.get_shield()}")
        # print("Enemy minions ids:", [id(m)
        #       for m in self._active_enemy_minions])
        # print("[DEBUG] Before enemy minion attack:",
        #       self._active_enemy_minions)

        # 4. Enemy minions attack
        self._minion_attack_phase(
            attackers=self._active_enemy_minions,
            ally_hero=self._enemy,
            enemy_hero=self._player,
            ally_minions=self._active_enemy_minions,
            enemy_minions=self._active_player_minions
        )
        self._cleanup_minions()
        if not self._enemy.is_alive() or not self._player.is_alive():
            return played

        # print("[DEBUG] After enemy minion attack:", self._active_enemy_minions)

        # print("Enemy minions ids:", [id(m)
        #       for m in self._active_enemy_minions])

        # 6. Player new turn
        self._player.new_turn()

        # print("Player minions ids:", [id(m)
        #       for m in self._active_player_minions])
        # print("DEBUG: Player minions at end of end_turn:",
        #       self._active_player_minions)

        return played


# class HearthStone():
#     def __init__(self, file: str):
#         """
#         Instantiates the controller.
#         Creates view and model instances.
#         The model should be instantiated with the game state specified
#         by the data within the file with the given name.

#         Minions that are not currently in a minion slot should be
#         instantiated with 1 health and 0 shield.

#         You should not handle the case where the file with the
#         specified name does not exist, nor should you handle the case
#         where the file does not contain a valid game state.

#         That is to say, you should not check for an invalid file/game state,
#         and you should not handle any errors that may occur because of one.
#         You should make use of the provided HearthView class.
#         """
#         self._file = file
#         with open(file, 'r') as f:
#             model_str = f.readline().strip()
#             self._model = eval(model_str)
#         self._view = HearthView()

#     def __str__(self) -> str:
#         """
#         Returns a human readable string stating
#         that this is a game of Hearthstone using the current file path.
#         """
#         return f"{CONTROLLER_DESC}{self._file}"

#     def __repr__(self) -> str:
#         """
#         Returns a string which could be copied and pasted into a
#         REPL to construct a new instance identical to self.
#         """
#         return f"{self.__class__.__name__}({repr(self._file)})"

#     def update_display(self, messages: list[str]):
#         """
#         Update the display by printing out the current game state.
#         The display should contain (from top to bottom):
#         A banner containing the game name;
#         A depiction of the enemy hero, with (from left to right) their health (HP),
#         shield, number of remaining cards, and energy level;
#         The enemy’s minion slots (with minion health (HP) and shield);
#         The player’s minion slots (with minion health (HP) and shield);
#         The player’s current hand;
#         A depiction of the player hero,
#         with (from left to right) their health (HP),
#         shield, number of remaining cards, and energy level;
#         A list of messages to the player.
#         Minions and heros are labelled with the character/number
#         that should be entered to target them.
#         Messages are arranged such that earlier messages in the
#         provided list appear above later ones.
#         """
#         self._view.update(
#             player=self._model.get_player(),
#             enemy=self._model.get_enemy(),
#             player_minions=self._model.get_player_minions(),
#             enemy_minions=self._model.get_enemy_minions(),
#             messages=messages
#         )

#     def get_command(self) -> str:
#         """
#         Repeatedly prompts the user until they enter a valid command.
#         Returns the first valid command entered by the user.
#         The possible valid commands are given in Table 2.
#         Whenever the user enters an invalid command,
#         the display should be updated with the INVALID_COMMAND message
#         from support.py before the user is prompted again.
#         The player’s command will be case insensitive,
#         but the returned command should be lower case.
#         Note also that card positions will be entered one-indexed
#         (that is, starting at 1, not 0).
#         """
#         valid = {PLAY_COMMAND, DISCARD_COMMAND, END_TURN_COMMAND,
#                  LOAD_COMMAND, HELP_COMMAND}
#         while True:
#             cmd = input(COMMAND_PROMPT).strip().lower()
#             if cmd in valid:
#                 return cmd
#             else:
#                 self.update_display([INVALID_COMMAND])

#     def get_target_entity(self) -> str:
#         """
#         Repeatedly prompts the user until they enter a valid entity.
#         A valid entity is one of the following:
#         PLAYER_SELECT or ENEMY_SELECT
#         to select the player or enemy hero respectively;
#         an integer between 1 and 5 inclusive,
#         to select the minion in the enemy’s minion
#         slot at the respective position;
#         or an integer between 6 and 10 inclusive,
#         to select the minion in the player’s minion slot at the position
#         given by the subtracting 5 from the integer.

#         If a minion does not currently exist at a specified position,
#         then the identifier is treated as invalid.

#         If a hero is selected, the identifier should be returned directly.
#         If an enemy’s minion is selected,
#         the (zero-indexed) index of the minion in the enemy’s minion slots
#         should be returned prepended by ENEMY_SELECT.

#         If an player’s minion is selected,
#         the (zero-indexed) index of the minion in the player’s minion slots
#         should be returned prepended by PLAYER_SELECT.

#         Input should be case-insensitive,
#         but the returned identifier should be upper-case.
#         Whenever the user enters an invalid identifier,
#         the display should be updated with the
#         INVALID_ENTITY message before the user is prompted again.
#         """
#         while True:
#             sel = input(ENTITY_PROMPT).strip().upper()
#             if sel == PLAYER_SELECT or sel == ENEMY_SELECT:
#                 return sel
#             if sel.isdigit():
#                 index = int(sel)
#                 if (1 <= index <= 5 and index-1
#                         < len(self._model.get_enemy_minions())):
#                     return ENEMY_SELECT + str(index - 1)
#                 if (6 <= index <= 10 and index-6
#                         < len(self._model.get_player_minions())):
#                     return PLAYER_SELECT + str(index-6)
#             self.update_display([INVALID_ENTITY])

#     def save_game(self):
#         """
#         Writes the string representation of this controllers
#         HearthModel instance to autosave.txt.
#         If autosave.txt does not exist, it should be created.
#         If autosave.txt already has content in it, it should be overwritten.
#         """
#         with open(SAVE_LOC, "w") as f:
#             f.write(str(self._model) + "\n")

#     def load_game(self, file: str):
#         """
#         Replaces the current model instance with a new one loaded
#         from the data within the file with the given name.
#         Minions that are not currently in a minion slot should be
#         instantiated with 1 health and 0 shield.
#         You should not handle the case where the file with the
#         specified name does not exist,
#         nor should you handle the case where the file does not
#         contain a valid game state.
#         That is to say, you should not check for an invalid file/game state,
#         and you should not handle any errors that may occur because of one.
#         """
#         with open(file, 'r') as f:
#             line = f.readline().strip()
#         self._model = eval(line)

#     def play(self):
#         """
#         Conducts a game of Hearthstone from start to finish
#         """
#         messages: list[str] = []
#         while True:
#             self.update_display(messages)
#             if self._model.has_won() or self._model.has_lost():
#                 break
#             cmd = self.get_command()
#             messages = []
#             if cmd == PLAY_COMMAND:
#                 hand = self._model.get_player().get_hand()
#                 idx = int(input(f"{PLAY_COMMAND}"(1-{len(hand)})).strip()) - 1
#                 card = hand[idx]

#                 tgt = self.get_target_entity()
#                 if tgt == PLAYER_SELECT:
#                     target = self._model.get_player()
#                 elif tgt == ENEMY_SELECT:
#                     target = self._model.get_enemy()
#                 elif tgt.startswith(ENEMY_SELECT):
#                     i = int(tgt[len(ENEMY_SELECT):])
#                     target = self._model.get_enemy_minions()[i]
#                 else:
#                     i = int(tgt[len(PLAYER_SELECT):])
#                     target = self._model.get_player_minions()[i]

#                 ok = self._model.play_card(card, target)
#             if ok:
#                 messages = [PLAY_MESSAGE + card.get_name()]
#             else:
#                 messages = [ENERGY_MESSAGE]
#                 if not self._model.play_card(card, target):
#                     messages = [INVALID_COMMAND]

#                 elif cmd == DISCARD_COMMAND:
#                     hand = self._model.get_player().get_hand()
#                     idx = int(
#                         input(f"{DISCARD_COMMAND} (1–{len(hand)}): ").strip()) - 1
#                     card = hand[idx]
#                     self._model.discard_card(card)
#                     messages = [DISCARD_MESSAGE + card.get_name()]

#                 elif cmd == END_TURN_COMMAND:
#                     played = self._model.end_turn()
#                     if played:
#                         messages = [ENEMY_PLAY_MESSAGE +
#                                     name for name in played]

#                 elif cmd == LOAD_COMMAND:
#                     fname = input("Filename to load").strip()
#                     self.load_game(fname)
#                     messages = [GAME_LOAD_MESSAGE + fname]

#                 elif cmd == HELP_COMMAND:
#                     messages = HELP_MESSAGES.copy()

#         # final display + outcome
#         self.update_display(messages)
#         if self._model.has_won():
#             print(WIN_MESSAGE)
#         elif self._model.has_lost():
#             print(LOSS_MESSAGE)


# def play_game(file: str):
#     try:
#         controller = HearthStone(file)
#     except (ValueError, FileNotFoundError):
#         controller = HearthStone(SAVE_LOC)


# def main() -> None:
#     pass
#     # play_game('levels/level1.txt')

# if __name__ == "__main__":
#     pass


# deck1 = CardDeck([Shield(), Heal(), Fireball(1), Raptor(1, 0), Wyrm(1, 0), Shield(), Heal(),
#                   Fireball(0), Fireball(0), Raptor(1, 0), Shield(), Heal(),
#                   Fireball(0), Fireball(0), Raptor(1, 0), Shield(),
#                   Heal(), Fireball(0), Fireball(0), Raptor(1, 0)])
# hand1 = [Raptor(1, 0), Wyrm(1, 0), Fireball(3), Shield(), Heal()]
# player = Hero(10, 10, 5, deck1, hand1)
# # ['R', 'W', 'S', 'H', 'R', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9'])
# deck2 = CardDeck([Raptor(1, 0), Wyrm(1, 0), Shield(), Heal(), Raptor(1, 0), Fireball(9), Fireball(9),
#                   Fireball(9), Fireball(9), Fireball(9), Fireball(9),
#                   Fireball(9), Fireball(9), Fireball(9), Fireball(9)])
# hand2 = [Wyrm(1, 0), Wyrm(1, 0), Heal(), Fireball(0), Shield()]
# enemy = Hero(20, 5, 5, deck2, hand2)
# player_minions = [Wyrm(1, 0), Raptor(1, 0)]
# enemy_minions = [Raptor(1, 0), Raptor(
#     1, 0), Raptor(1, 0), Raptor(1, 0), Raptor(1, 0)]
# model = HearthModel(player, player_minions, enemy, enemy_minions)

# card = player.get_hand()[0]
# target = Entity(0, 0)  # Minions don't need target
# model.play_card(card, target)
# print(model)

# card = player.get_hand()[1]
# target = enemy  # Fireball the enemy hero
# model.play_card(card, target)
# print(enemy)

# played = model.end_turn()  # Hand refilled, and enemy places minions
# new_state = str(model)
# print(new_state)
# # Free up hand space for fireball card
# card = player.get_hand()[2]
# target = player
# model.play_card(card, target)
# print(new_state)

# played = model.end_turn()  # Player damaged by Fireball, enemy buffed
# new_state = str(model)
# print(new_state)

# played = model.end_turn()  # Player's fireball card should tick up
# new_state = str(model)
# print(new_state)

# # Upon new turn, player's energy should be filled
# if player.get_energy() == player.get_max_energy():
#     print("True")
# else:
#     raise AssertionError(
#         "Player energy values does not match the expected values")
