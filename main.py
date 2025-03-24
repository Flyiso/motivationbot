from kivy.app import App
from kivy.uix.widget import Widget
from bots import MotiBot
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from pathlib import Path
import pickle
import os

# to remember/have easy access to model creation:
#b_name = 'jon'
#voice = 'bm_george'
#toughness = 10
#intensity = 10
#meanness = 8
#seriousness = 10
#critic_level = 9
#user_belief = 99

#custom_bot = MotiBot(b_name, voice, toughness, intensity, meanness, seriousness, critic_level, user_belief)
#with open(f"custom_models/{b_name}.pkl", "wb") as f:
#    pickle.dump(custom_bot, f)


def confirm_dirs(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.1, 0.9, 0.1, 1) 
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(size=self.adjust_font_size) 

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def adjust_font_size(self, *args):
        self.font_size = self.width * 0.1

class MyBotWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical',
                         padding=[30, 20, 30, 20],
                         spacing=35)

        self.spinner = Spinner(
            text="Select coach:",
            values=self.get_bots(),
            size_hint_y = 0.15,
            font_size = 40
        )

        self.text_input = TextInput(
            hint_text="What do you struggle with?",
            size_hint_y = 0.30,
            font_size = 50,
        )

        self.button = RoundedButton(
            text="MOTIVATE ME!",
            size_hint_y = 0.40,
            background_color = (0, 0, 0, 0)
        )
        self.button.bind(on_press=self.send_data)

        self.add_widget(self.spinner)
        self.add_widget(self.text_input)
        self.add_widget(self.button)

    def send_data(self, instance):
        selected_bot = self.spinner.text
        input_text = self.text_input.text

        if selected_bot == "Select coach":
            print("Please select a coach!")
            return

        if not input_text.strip():
            print("Please tell what you need help with!")
            return

        user_problem = input_text
        with open(f"custom_models/{selected_bot}.pkl", "rb") as f:
            loaded_bot = pickle.load(f)
        loaded_bot.get_audio_motivation(input_text)
    
    def get_bots(self):
        bots = [bot.stem for bot in Path('custom_models').iterdir() if bot.is_file()]
        return bots


class NewBotWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical',
                         padding=[10, 20, 10, 20],
                         spacing=5)

        self.text_input = TextInput(
            hint_text="Name the new Coach",
            font_size = 50,
        )

        self.spinner = Spinner(
            text="Select voice:",
            values=self.get_voices(),
            font_size = 40
            )
        
        self.slider_toughness = Slider(
            min = 0,
            max = 100,
            value = 50
        )

        self.slider_intensity = Slider(
            min = 0,
            max = 100,
            value = 50
        )

        self.slider_meanness = Slider(
            min = 0,
            max = 100,
            value = 50
        )

        self.slider_seriousness = Slider(
            min = 0,
            max = 100,
            value = 50
        )

        self.slider_criticlevel = Slider(
            min = 0,
            max = 100,
            value = 50
        )
        
        self.slider_userbelief = Slider(
            min = 0,
            max = 100,
            value = 50
        )

        self.button = RoundedButton(
            text="Create Coach!",
            size_hint_y = 0.30,
            background_color = (0, 0, 0, 0)
        )
        self.button.bind(on_press=self.send_data)
    
        self.add_widget(self.text_input)
        self.add_widget(self.spinner)
        self.add_widget(self.slider_toughness)
        self.add_widget(self.slider_intensity)
        self.add_widget(self.slider_meanness)
        self.add_widget(self.slider_seriousness)
        self.add_widget(self.slider_criticlevel)
        self.add_widget(self.slider_userbelief)
        self.add_widget(self.button)

    def send_data(self, instance):
        bot_name = self.text_input.text
        selected_voice = self.spinner.text

        if selected_voice == "Select voice":
            print("Please select a voice")
            return

        if not bot_name.strip():
            print("Please Name the coach!")
            return
        bot_name = self.clean_text(bot_name)

        bot = MotiBot(bot_name, selected_voice,
                      self.slider_toughness.value, self.slider_intensity.value,
                      self.slider_meanness.value, self.slider_seriousness.value,
                      self.slider_criticlevel.value, self.slider_userbelief.value)
        with open(f"custom_models/{bot_name}.pkl", "wb") as f:
            pickle.dump(bot, f)
    
    def clean_text(self, to_clean: str):
        return to_clean.strip().replace(" ", "-")
        
    def get_voices(self):
        return ['bf_emma', 'bf_isabella', 'bm_george', 'bm_fable', 'am_puck', 'am_michael', 'af_bella', 'af_heart']


class MotivationBotApp(App):
    def build(self):
        confirm_dirs('audio_data')
        confirm_dirs('custom_models')

        carousel = Carousel(direction="right")
        box_1 = MyBotWidget()
        box_2 = NewBotWidget()
        carousel.add_widget(box_1)
        carousel.add_widget(box_2)

        return carousel

if __name__ == '__main__':
    MotivationBotApp().run()
