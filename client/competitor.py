import random

# Competitor class

class Competitor:
    username = "jack" # Change this!

    def __init__(self):
        # initialize a counter for the round number
        self.round_number = 0


        # strategy guide (opening)
        # in the first two rounds, load up on ammo since opponent is most likely going to load up on ammo as well
        # since there is no healing, the goal is to try to predict whether the opoonent is going to shield or attack
        # i will aim for aggressive strategy for bot 3 to eliminate the opponent's bot 3 on round 3
        # if bot 3 is not killed, i have no ammo, then I will prepare for midgame
        
        # strategy guide (defense tactics)
        # every turn, check 
        #   if any bot is vulernable to attack (if opponent has enough ammo from three bots to kill a bot, then shield that bot)
        #       shield that bot
        #   else, if the bots are not vulernable to attack, then load up on ammo
    
        # strategy guide (attacks)
        # the ultimate goal is to attack, its hard to predict when bots shield, so to guarantee damage, 
        # I will employ targeting one bot at a time with all my man power
        # no matter what happens, if i can kill with 6 bullets, do it, because its instant kill or two shot with shields
        # in any turn, 
        # if my total ammo is more than 4, 
        #   then I will start attacking the opponent's bot with the least health
        #   first I will determine which bot is attackable and has the least health
        #   then I will attack that bot with all the bots, but if the bot is killed, then I will load up with the rest of the bots
    def play_turn(self, controller):
        self.round_number += 1

        # get the amount of ammo for your team's bot
        ammo_one = controller.get_my_bot_ammo(0)
        ammo_two = controller.get_my_bot_ammo(1)
        ammo_three = controller.get_my_bot_ammo(2)
        total_ammo = ammo_one + ammo_two + ammo_three

        # get the team health for your team's bot
        health_one = controller.get_my_bot_health(0)
        health_two = controller.get_my_bot_health(1)
        health_three = controller.get_my_bot_health(2)
        total_health = health_one + health_two + health_three

        # get the opponent health for the opponent's bot
        opponent_health_one = controller.get_opponent_bot_health(0)
        opponent_health_two = controller.get_opponent_bot_health(1)
        opponent_health_three = controller.get_opponent_bot_health(2)
        total_opponent_health = opponent_health_one + opponent_health_two + opponent_health_three

        # get the opponent ammo for the opponent's bot
        opponent_ammo_one = controller.get_opponent_bot_ammo(0)
        opponent_ammo_two = controller.get_opponent_bot_ammo(1)
        opponent_ammo_three = controller.get_opponent_bot_ammo(2)
        total_opponent_ammo = opponent_ammo_one + opponent_ammo_two + opponent_ammo_three

        # determine weakest bot while considering that bots with 0 health is not considered (so only compare bots with health greater than 0)
        weakest_bot = 0
        # create a dictionary with the bot number and the health of the bots
        bot_health = {0: health_one, 1: health_two, 2: health_three}
        # remove all the bots with 0 health
        bot_health = {key: value for key, value in bot_health.items() if value > 0}
        # get the bot value of the first item in the dictionary and set that as the weakest opponent bot
        weakest_bot = list(bot_health.keys())[0]
        # iterate through the dictionary to determine the weakest bot
        for bot, health in bot_health.items():
            if health < bot_health[weakest_bot] and health > 0:
                weakest_bot = bot

        # determine weakest opponent bot while considering that bots with 0 health is not considered
        weakest_opponent_bot = 0
        # create a dictionary with the bot number and the health of the bots
        opponent_bot_health = {0: opponent_health_one, 1: opponent_health_two, 2: opponent_health_three}
        # remove all the nots with 0 health
        opponent_bot_health = {key: value for key, value in opponent_bot_health.items() if value > 0}
        # get the bot value of the first item in the dictionary and set that as the weakest opponent bot
        weakest_opponent_bot = list(opponent_bot_health.keys())[0]
        # iterate through the dictionary to determine the weakest opponent bot (and please start with the bot that has non zero health)
        for bot, health in opponent_bot_health.items():
            if health < opponent_bot_health[weakest_opponent_bot] and health > 0:
                weakest_opponent_bot = bot


        print("Round Number: ", self.round_number)
        print("Total Ammo: ", total_ammo)
        print("Total Health: ", total_health)
        print("Total Opponent Health: ", total_opponent_health)
        print("Total Opponent Ammo: ", total_opponent_ammo)
        print("Weakest Bot: ", weakest_bot)
        print("Weakest Opponent Bot: ", weakest_opponent_bot)
    
        # opening
        if self.round_number == 1:
            # load up on ammo
            controller.load(0)
            controller.load(1)
            controller.load(2)
        elif self.round_number == 2:
            # load up on ammo
            controller.load(0)
            controller.load(1)
            controller.load(2)
        elif self.round_number == 3:
            # attack opponent's bot 3
            controller.attack(0, 2, 2)
            controller.attack(1, 2, 2)
            controller.attack(2, 2, 1)

        
        # attack tactics (how do you ensure that i am not attacking a dead bot?)
        if total_ammo >= 4:
            # determine how many bots I need to finish the bot (without shielding)
            num_bot_required = 0
            if ammo_one >= controller.get_opponent_bot_health(weakest_opponent_bot):
                num_bot_required += 1
            elif ammo_one + ammo_two >= controller.get_opponent_bot_health(weakest_opponent_bot):
                num_bot_required += 2
            elif ammo_one + ammo_two + ammo_three >= controller.get_opponent_bot_health(weakest_opponent_bot):
                num_bot_required += 3

            # attack the weakest opponent bot
            if num_bot_required == 1:
                controller.attack(0, weakest_opponent_bot, ammo_one)
                controller.load(1)
                controller.load(2)
            elif num_bot_required == 2:
                controller.attack(0, weakest_opponent_bot, ammo_one)
                controller.attack(1, weakest_opponent_bot, ammo_two)
                controller.load(2)
            elif num_bot_required == 3:
                controller.attack(0, weakest_opponent_bot, ammo_one)
                controller.attack(1, weakest_opponent_bot, ammo_two)
                controller.attack(2, weakest_opponent_bot, ammo_three)
             # in the case that the opponent is likely to attack (determined if the total opponent ammo is greater than the health of all bots) (load from the strongest bot with most health and shield with other bots)
        else:
            if total_opponent_ammo >= total_health:
                # shield the weakest bot and load up the other bots
                controller.shield(weakest_bot)
                if weakest_bot == 0:
                    controller.load(1)
                    controller.shield(2)
                elif weakest_bot == 1:
                    controller.shield(0)
                    controller.load(2)
                elif weakest_bot == 2:
                    controller.load(0)
                    controller.shield(1)
            else:
                # load up on ammo if ammo is less than 2, or else shield
                if ammo_one < 2:
                    controller.load(0)
                else:
                    controller.shield(0)
                if ammo_two < 2:
                    controller.load(1)
                else:
                    controller.shield(1)
                if ammo_three < 2:
                    controller.load(2)
                else:
                    controller.shield(2)

        