from ollama import create, chat

class MotiBot:
    def __init__(self):
        self.toughness = self._get_toughness()
        self.meanness = self._get_meanness()
        self.seriousness = self._get_seriousness()
        self.critic_level = self._get_critic_level()
        self.user_belief = self._get_user_beief()
        self.personality = self._get_personality()
        self.system_prompt = /
        f'You are a coach who deliver motivational speaches.{self.personality}'
    
    def _get_personality(self):
        return f'{self.toughness} {self.meanness} {self.seriousness} {self.critic_level} {self.user_belief}'
    
    def _get_toughness(self, q_level: int) -> str:
        """
        How tough or patient the assistant should be.

        :param q_level: int- scale of 0-100 from opposite to maximum. 
        """
        if q_level >= 50:
            quality = 'patient'
        if q_level <= 49:
            quality = 'tough'
        level = max([q_level, 50]) - min([q_level, 50])
        q_string = f'your personality are {self._get_quality_quantity(level)} {quality}.'
        return q_string

    def _get_meanness(self, q_level: int) -> str:
        """
        How much the bot may include insults in their motivational speaches.

        :param q_level: int- scale of 0-99 from opposite to maximum. 
        """
        if q_level >= 50:
            quality = 'friendly'
        if q_level <= 49:
            quality = 'mean'
        level = max([q_level, 50]) - min([q_level, 50])
        q_string = f'You are also {self._get_quality_quantity(level)} {quality}.'
        return q_string
    
    def _get_seriousness(self, q_level: int) -> str:
        """
        How much the bot jokes.

        :param q_level: int- scale of 0-100 from opposite to maximum. 
        """
        if q_level >= 50:
            quality = 'playful'
        if q_level <= 49:
            quality = 'serious'
        level = max([q_level, 50]) - min([q_level, 50])
        q_string = f'Your attitude is mainly {self._get_quality_quantity(level)} {quality}.'
        return q_string

    def _get_critic_level(self, q_level: int) -> str:
        """
        How much criticism the bot should deliver.

        :param q_level: int- scale of 0-100 from opposite to maximum. 
        """
        if q_level >= 50:
            quality = 'positive'
        if q_level <= 49:
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
        pass
    
    def get_motivation(self, mot_theme: str) -> str:
        """
        problem in, motivational text out.
        """
        pass