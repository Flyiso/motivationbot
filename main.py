from bots import MotiBot
import pickle


print('.'*100)
problem = input('what do you need help with?\n')
print('.'*100)
print('')

b_name = 'jon'
toughness = 100
intensity = 90
meanness = 80
seriousness = 10
critic_level = 70
user_belief = 5

custom_bot = MotiBot(b_name, toughness, intensity, meanness, seriousness, critic_level, user_belief)
with open(f"custom_models/{b_name}.pkl", "rb") as f:
    loaded_bot = pickle.load(f)

loaded_bot.get_audio_motivation(problem)

#custom_bot.get_audio_motivation(problem)

#b_name = 'noj'
#toughness = 90
#intensity = 95
#meanness = 95
#seriousness = 90
#critic_level = 95
#user_belief = 5

#print('')
#print('#'*100)
#print('')
#custom_bot = MotiBot(b_name, toughness, intensity, meanness, seriousness, critic_level, user_belief)
#custom_bot.get_audio_motivation(problem)
#print('')
#print('#'*100)