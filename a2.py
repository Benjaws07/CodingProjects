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
        self._health = health
        self._shield = shield

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
        self._shield += shield
        return self._shield

    def apply_health(self, health: int):
        """
        Applies the given amount of health.
        """
        self._health += health

    def apply_damage(self, damage: int):
        """
        Applies the given amount of damage.
        The entity’s health never drops below 0 and 
        any excess damage is discarded.
        """

        if self._shield > damage:
            self._shield -= damage
        else:
            remaining = damage - self._shield
            self._shield = 0
            self._health = max(0, self._health - remaining)
        return self._health

    def is_alive(self) -> bool:
        """
        Returns if this entity is alive or not.
        """
        if self._health <= 0:
            return False
        if isinstance(self, Hero):
            return not self._deck.is_empty()
        return True


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
    def __init__(self, health, shield):
        """
        Instantiate a new Minion with the specified health and shield value.
        """
        # Call out the values from the base classes
        Entity.__init__(self, health, shield)
        Card.__init__(self)
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
        return self.__class__(1, 0)


class Wyrm(Minion):
    def __init__(self, health: int, shield: int):
        Entity.__init__(self, health, shield)
        Card.__init__(self)

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
        # [ally_hero] + ally_minions

        # if ally_hero.is_alive():
        #     combatants.append((ally_hero.get_health(), ally_hero))

        # for minion in ally_minions:
        #     if minion.is_alive():
        #         combatants.append((minion.get_health(), minion))

        # if not combatants:
        #     return ally_hero

        min_health = min(ent.get_health() for ent in combatants)

        lowest_health_entities = [ent for ent in combatants
                                  if ent.get_health == min_health]

        if ally_hero in lowest_health_entities:
            return ally_hero
        return lowest_health_entities[0]

    def summon(self) -> 'Wyrm':
        return Wyrm(1, 0)


class Raptor(Minion):
    def __init__(self, health: 1, shield: 0):
        super().__init__(health, shield)
        self._name = RAPTOR_NAME
        self._desc = RAPTOR_DESC
        self._symbol = RAPTOR_SYMBOL
        self._cost = 2
        self._effect = {}
        self._is_permanent = True

    # def __repr__(self) -> str:
    #     return Entity.__repr__(self)

    def get_effect(self):
        return {DAMAGE: self.get_health()}

    def choose_target(self, ally_hero: Entity, enemy_hero: Entity,
                      ally_minions: list[Entity],
                      enemy_minions: list[Entity]) -> Entity:
        if not enemy_minions:
            return enemy_hero

        # Finds minion with highest health
        max_health = max(minion.get_health() for minion in enemy_minions)
        # Returns the leftmost minion with that health
        for minion in enemy_minions:
            if minion.get_health() == max_health:
                return minion
            # In case everything fails
        return enemy_hero

    def summon(self) -> 'Raptor':
        return Raptor(1, 0)


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
        self._active_player_minions = active_player_minions.copy()
        self._enemy = enemy
        self._active_enemy_minions = active_enemy_minions.copy()

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
            f"{(player_minions)}|"
            f"{enemy_str}|"
            f"{enemy_minions}"
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
        return (not self._player.is_alive()
                or self._player.get_deck().is_empty())

    def _apply_effects(self, target: Entity, effects: dict[str, int]):
        """
        Applies effects based on the status of target
        """
        for effect, amount in effects.items():
            if effect == DAMAGE:
                target.apply_damage(amount)
            elif effect == SHIELD:
                target.apply_shield(amount)
            elif effect == HEALTH:
                target.apply_health(amount)

        print(f"Applying effects: {effects} to {target}")

    def _cleanup_minions(self):
        """
        Removes dead minions when checking whether its alive or not
        """
        self._active_player_minions = [
            m for m in self._active_player_minions if m.is_alive()]
        self._active_enemy_minions = [
            m for m in self._active_enemy_minions if m.is_alive()]

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
        if not self._player.spend_energy(card.get_cost()):
            return False

        # Remove *that* card from the real hand
        self._player.get_hand().remove(card)

        if card.is_permanent():
            if isinstance(card, Minion):
                minion = card.summon()
                if len(self._active_enemy_minions) >= MAX_MINIONS:
                    self._active_enemy_minions.pop(0)
            self._active_player_minions.append(minion)
            self._apply_effects(target, card.get_effect())
            # Clean up any dead minions
            self._cleanup_minions()
            return True
        elif isinstance(target, Entity) and target.is_alive():
            self._apply_effects(target, card.get_effect())
            # Clean up any dead minions
            self._cleanup_minions()
            return True
        else:
            return False

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

        # 1) Player's minions attack
        for minion in list(self._active_player_minions):
            target = minion.choose_target(
                ally_hero=self._player,
                enemy_hero=self._enemy,
                ally_minions=self._active_player_minions,
                enemy_minions=self._active_enemy_minions
            )
            self._apply_effects(target, minion.get_effect())
        # remove dead after player-minion attacks
        self._cleanup_minions()

        # 2) Enemy hero start‑of‑turn
        self._enemy.new_turn()

        if not self._enemy.is_alive():
            return played  # game over, nothing more

        # 3) Enemy plays cards from hand (in order)
        #    a) Permanent cards (minions) fill slots 0–4, shifting if full
        #    b) Spells and non‑permanent effects
        i = 0
        hand = self._enemy.get_hand()
        while i < len(hand):
            card = hand[i]
            if not self._enemy.spend_energy(card.get_cost()):
                i += 1
                continue
            hand.pop(i)
            played.append(card.get_name())
        # for card in list(self._enemy._hand):   # note: _hand is the real list
        #     if not self._enemy.spend_energy(card.get_cost()):
        #         continue
        #     self._enemy._hand.remove(card)

        #     # play it
            if card.is_permanent() and isinstance(card, Minion):
                # new_minion = card.__class__(health=1, shield=0)
                minion = card.summon()
                if len(self._active_enemy_minions) >= MAX_MINIONS:
                    self._active_enemy_minions.pop(0)
                self._active_enemy_minions.append(minion)
                # effects = card.get_effect()
            else:
                effects = card.get_effect()
                target = None
                # choose a target for spells
                if DAMAGE in effects:
                    target = self._player
                elif SHIELD in effects or HEALTH in effects:
                    target = self._enemy
                else:
                    target = None
                if target and target.is_alive():
                    self._apply_effects(target, effects)
            i = 0
        # # remove dead after enemy‑card effects
        self._cleanup_minions()

        # 4) Enemy's minions attack
        for minion in list(self._active_enemy_minions):
            target = minion.choose_target(
                ally_hero=self._enemy,
                enemy_hero=self._player,
                ally_minions=self._active_enemy_minions,
                enemy_minions=self._active_player_minions
            )
            self._apply_effects(target, minion.get_effect())
        # remove dead after enemy‑minion attacks
        self._cleanup_minions()
        # 5) Player new turn setup (fireballs, draw, energy)
        self._player.new_turn()
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


def main() -> None:
    pass
    # play_game('levels/level1.txt')


# def test_raptor_targeting():
#     # Create a model instance
#     deck1 = CardDeck([])
#     hand1 = []
#     player = Hero(10, 6, 5, deck1, hand1)

#     deck2 = CardDeck([])
#     hand2 = []
#     enemy = Hero(20, 5, 5, deck2, hand2)

#     model = HearthModel(player, [], enemy, [])

#     # Create enemy minion: Raptor with health=4
#     raptor = Raptor(health=4, shield=0)
#     print("Raptor effect:", raptor.get_effect())
#     model._active_enemy_minions.append(raptor)

#     model._active_player_minions.clear()

#     # Print initial healths
#     print("Before Raptor attack:")
#     print("Player hero health:", model._player.get_health())

#     # Let Raptor attack
#     target = raptor.choose_target(
#         ally_hero=model._enemy,
#         enemy_hero=model._player,
#         ally_minions=model._active_enemy_minions,
#         enemy_minions=model._active_player_minions
#     )
#     print("Target is:", target.get_health(), target.get_shield())
#     print(f"Player hero shield before: {model._player.get_shield()}")
#     model._apply_effects(target, raptor.get_effect())
#     print("Target is model._player:", target is model._player)
#     print(f"Player hero shield after: {model._player.get_shield()}")
#     print(f"Player hero health after: {model._player.get_health()}")

#     # Print healths after attack
#     print("After Raptor attack:")
#     print("Player hero health:", model._player.get_health())
#     # print("Minion 1 Health:", minion1.get_health())
#     # print("Minion 2 Health:", minion2.get_health())
#     assert model._player.get_shield() == 2, "Shield should absorb 4 damage"
#     assert model._player.get_health() == 10, "Health should be unchanged due to shield"

if __name__ == "__main__":
    pass

deck1 = CardDeck([Shield(), Heal(), Fireball(1), Raptor(1, 0), Wyrm(1, 0), Shield(), Heal(),
                  Fireball(0), Fireball(0), Raptor(1, 0), Shield(), Heal(),
                  Fireball(0), Fireball(0), Raptor(1, 0), Shield(),
                  Heal(), Fireball(0), Fireball(0), Raptor(1, 0)])
hand1 = [Raptor(1, 0), Wyrm(1, 0), Fireball(3), Shield(), Heal()]
player = Hero(10, 10, 5, deck1, hand1)
# ['R', 'W', 'S', 'H', 'R', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9'])
deck2 = CardDeck([Raptor(1, 0), Wyrm(1, 0), Shield(), Heal(), Raptor(1, 0), Fireball(9), Fireball(9),
                  Fireball(9), Fireball(9), Fireball(9), Fireball(9),
                  Fireball(9), Fireball(9), Fireball(9), Fireball(9)])
hand2 = [Wyrm(1, 0), Wyrm(1, 0), Heal(), Fireball(0), Shield()]
enemy = Hero(20, 5, 5, deck2, hand2)
player_minions = [Wyrm(1, 0), Raptor(1, 0)]
enemy_minions = [Raptor(1, 0), Raptor(
    1, 0), Raptor(1, 0), Raptor(1, 0), Raptor(1, 0)]
model = HearthModel(player, player_minions, enemy, enemy_minions)

card = player.get_hand()[0]
target = Entity(0, 0)  # Minions don't need target
model.play_card(card, target)
print(model)

card = player.get_hand()[1]
target = enemy  # Fireball the enemy hero
model.play_card(card, target)
print(enemy)

played = model.end_turn()  # Hand refilled, and enemy places minions
new_state = str(model)
print(new_state)
# Free up hand space for fireball card
card = player.get_hand()[2]
target = player
model.play_card(card, target)
print(new_state)

played = model.end_turn()  # Player damaged by Fireball, enemy buffed
new_state = str(model)
print(new_state)

played = model.end_turn()  # Player's fireball card should tick up
new_state = str(model)
print(new_state)
