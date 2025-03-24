from kivy.app import App
from kivy.uix.widget import Widget
from bots import MotiBot
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
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
        self.font_size = self.height * 0.45

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
        

class MotivationBotApp(App):
    def build(self):
        confirm_dirs('audio_data')
        confirm_dirs('custom_models')
        return MyBotWidget()

if __name__ == '__main__':
    MyBotApp().run()
