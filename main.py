from ollama import create, chat

class MotiBot:
    def __init__(self, 
                 bot_name: str = 'Rolf',
                 toughness:int = 75, intensity: int = 80,
                 meanness:int = 40, seriousness:int = 20,
                 critic_level:int = 90, user_belief:int = 90):
        self.bot_name = bot_name
        self.toughness = self._get_toughness(toughness)
        self.intensity = self._get_intensity(intensity)
        self.meanness = self._get_meanness(meanness)
        self.seriousness = self._get_seriousness(seriousness)
        self.critic_level = self._get_critic_level(critic_level)
        self.user_belief = self._get_user_beief(user_belief)
        self.personality = self._get_personality()
        self.system_prompt = \
        f'You are a coach who deliver motivational speaches through text. {self.personality}'
        #print(f'{"*"*20}\n Model personality prompt:\n{self.system_prompt}\n{"*"*20}\n')
        self.model = self._create_bot()
    
    def _get_personality(self):
        return f'{self.toughness} {self.intensity} {self.meanness} {self.seriousness} {self.critic_level} {self.user_belief}'
    
    def _get_toughness(self, q_level: int) -> str:
        """
        How tough or patient the assistant should be.

        :param q_level: int- scale of 0-100 from opposite to maximum. 
        """
        if q_level <= 50:
            quality = 'patient'
        if q_level >= 49:
            quality = 'tough'
        level = max([q_level, 50]) - min([q_level, 50])
        q_string = f'Personality-wise you are {self._get_quality_quantity(level)} {quality},'
        return q_string
    
    def _get_intensity(self, q_level: int) -> str:
        """
        How tough or patient the assistant should be.

        :param q_level: int- scale of 0-100 from opposite to maximum. 
        """
        if q_level >= 50:
            quality = 'intense and yell sometimes'
        if q_level <= 49:
            quality = 'calm'
        level = max([q_level, 50]) - min([q_level, 50])
        q_string = f'you are {self._get_quality_quantity(level)} {quality},'
        return q_string

    def _get_meanness(self, q_level: int) -> str:
        """
        How much the bot may include insults in their motivational speaches.

        :param q_level: int- scale of 0-99 from opposite to maximum. 
        """
        if q_level <= 50:
            quality = 'friendly'
        if q_level >= 49:
            quality = 'mean'
        level = max([q_level, 50]) - min([q_level, 50])
        q_string = f'and are also {self._get_quality_quantity(level)} {quality}.'
        return q_string
    
    def _get_seriousness(self, q_level: int) -> str:
        """
        How much the bot jokes.

        :param q_level: int- scale of 0-100 from opposite to maximum. 
        """
        if q_level <= 50:
            quality = 'playful'
        if q_level >= 49:
            quality = 'serious'
        level = max([q_level, 50]) - min([q_level, 50])
        q_string = f'Your attitude is mainly {self._get_quality_quantity(level)} {quality}.'
        return q_string

    def _get_critic_level(self, q_level: int) -> str:
        """
        How much criticism the bot should deliver.

        :param q_level: int- scale of 0-100 from opposite to maximum. 
        """
        if q_level <= 50:
            quality = 'positive'
        if q_level >= 49:
            quality = 'critical'
        level = max([q_level, 50]) - min([q_level, 50])
        q_string = f'Your attitude to the users achivements are primarily {self._get_quality_quantity(level)} {quality} and'
        return q_string
    
    def _get_user_beief(self, q_level: int) -> str:
        """
        How much the bot believes in the users abilities.

        :param q_level: int- scale of 0-100 from opposite to maximum. 
        """
        if q_level >= 50:
            quality = 'positive'
        if q_level <= 49:
            quality = 'negative'
        level = max([q_level, 50]) - min([q_level, 50])
        q_string = f'your attitude towards the users chanses of success are {self._get_quality_quantity(level)} {quality}.'
        return q_string
    
    def _get_quality_quantity(self, amount: int) -> str:
        """
        return sring how much (distance from 50) of the quality

        :param  amount: int(0-50) of how much of x
        :return: string (from a little to very much) describing the quatntity of the quality
        """
        if amount <= 10:
            return 'somewhat'
        if amount <= 20:
            return 'moderately'
        if amount <= 30:
            return 'quite'
        if amount <= 40:
            return 'very'
        return 'extremely'

    def _create_bot(self):
        """
        Create a llm with selected the qualities
        """
        create(model=self.bot_name, from_='llama3', system=self.system_prompt)
        
    
    def get_motivation(self, mot_theme: str) -> str:
        """
        problem in, motivational text out.
        """
        motivation = chat(model=self.bot_name, messages=[
            {
                'role': 'user',
                'content': f'give a motivational speach to the user who struggles with {mot_theme}.'
            }
        ])
        return motivation.message.content

    def get_audio_motivation(self, mot_theme):
        print(self.get_motivation(mot_theme))

print('.'*100)
problem = input('what do you need help with?\n')
print('.'*100)
print('')

b_name = 'jon'
toughness = 10
intensity = 10
meanness = 10
seriousness = 10
critic_level = 10
user_belief = 95

print('#'*100)
print('')
custom_bot = MotiBot(b_name, toughness, intensity, meanness, seriousness, critic_level, user_belief)
custom_bot.get_audio_motivation(problem)

b_name = 'noj'
toughness = 90
intensity = 95
meanness = 95
seriousness = 90
critic_level = 95
user_belief = 5

print('')
print('#'*100)
print('')
custom_bot = MotiBot(b_name, toughness, intensity, meanness, seriousness, critic_level, user_belief)
custom_bot.get_audio_motivation(problem)
print('')
print('#'*100)