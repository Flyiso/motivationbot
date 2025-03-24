from ollama import create, chat
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import numpy as np
import torch
from pydub import AudioSegment
from pydub.playback import play


class MotiBot:
    def __init__(self, 
                 bot_name: str = 'Rolf', voice_str = 'bm_george', 
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
        self.voice = voice_str
        self.s_len = 'The speach should take about 30 seconds to read loud'
        self.system_prompt = \
        f'Your task is to deliver motivational speaches through text (not in all caps). {self.s_len}. {self.personality}'
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
        motivation = self.get_motivation(mot_theme)
        print('#'*100)
        print('')
        print(motivation)
        print('')
        print('#'*100)
        pipeline = KPipeline(lang_code='a')
        generator = pipeline(motivation, voice=self.voice)
        audio_data = []
        for i, (gs, ps, audio) in enumerate(generator):
            audio_data.append(audio)
        full_speech = np.concatenate(audio_data)
        sf.write(f'audio_data/fullspeech{self.bot_name}.wav', full_speech, 24000)
        sound = AudioSegment.from_file(f'audio_data/fullspeech{self.bot_name}.wav')
        play(sound)
