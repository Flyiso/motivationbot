from kivy.app import App
from kivy.uix.widget import Widget
from bots import MotiBot
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from pathlib import Path
import threading
import pickle
import os


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
        self.font_size = min([self.width * 0.1, self.height*0.5])
    
    def disable_button(self):
        self.disabled = True
        self.canvas.before.clear() 
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1) 
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(size=self.adjust_font_size) 
    
    def enable_button(self):
        self.disabled = False
        self.canvas.before.clear() 
        with self.canvas.before:
            Color(0.1, 0.9, 0.1, 1) 
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(size=self.adjust_font_size) 


class MyBotWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical',
                         padding=[30, 20, 30, 20],
                         spacing=50)

        self.spinner = Spinner(
            text="Select coach:",
            values=self.get_bots(),
            size_hint_y = None,
            font_size = 40
        )

        self.llm_speach = Label(
            text="Enter bot, problem and press the button to get motivation.",
            size_hint=(1, None),
            text_size=(400, None),
            valign="top",
            halign="center",
            font_size=30
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
        self.llm_speach.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.llm_speach)
        self.add_widget(self.scroll_view)

    def send_data(self, instance):
        """Handles UI updates and starts processing in a separate thread."""
        selected_bot = self.spinner.text
        input_text = self.text_input.text

        if selected_bot == "Select coach":
            print("Please select a coach!")
            return

        if not input_text.strip():
            print("Please tell what you need help with!")
            return

        self.llm_speach.text = "Generating speech..."

        
        instance.disabled = True
        self.button.Color=(0.5, 0.5, 0.1, 0)
        instance.Color = (0.5, 0.5, 0.5, 1)
        instance.disable_button()

        
        #Clock.schedule_once(lambda dt: self.do_layout(), 0)

        threading.Thread(target=self.process_motivation, args=(instance,), daemon=True).start()

    def process_motivation(self, instance):
        """Runs the audio processing & motivation generation in a background thread."""
        selected_bot = self.spinner.text
        input_text = self.text_input.text
        with open(f"custom_models/{selected_bot}.pkl", "rb") as f:
            loaded_bot = pickle.load(f)
        loaded_bot.get_motivation(input_text)
        Clock.schedule_once(lambda dt: self.update_motivation_text(loaded_bot), 0)
        loaded_bot.get_audio_motivation()
        Clock.schedule_once(lambda dt: instance.enable_button(), 0)

    def update_motivation_text(self, loaded_bot):
        """Ensures UI updates with motivation text."""
        self.llm_speach.halign = 'left'
        self.llm_speach.text = loaded_bot.motivation
        
    def get_bots(self):
        bots = [bot.stem for bot in Path('custom_models').iterdir() if bot.is_file()]
        return bots


class NewBotWidget(BoxLayout):
    def __init__(self, box, carousel, **kwargs):
        super().__init__(orientation='vertical',
                         padding=[30, 10, 30, 10],
                         spacing=25)

        self.dependent_box = box
        self.carousel = carousel
        self.text_input = TextInput(
            hint_text="Name the new Coach",
            font_size = 30,
        )

        self.spinner = Spinner(
            text="Select voice:",
            values=self.get_voices(),
            font_size = 30
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
            size_hint_y = 1,
            background_color = (0, 0, 0, 0)
        )
        self.button.bind(on_press=self.send_data)
    
        self.add_widget(self.text_input)
        self.add_widget(self.spinner)
        self.add_widget(self.get_labeled_slider('Soft', 'Though', self.slider_toughness))
        self.add_widget(self.get_labeled_slider('Calm', 'Intense', self.slider_intensity))
        self.add_widget(self.get_labeled_slider('Nice', 'Mean', self.slider_meanness))
        self.add_widget(self.get_labeled_slider('Not serious', 'Serious', self.slider_seriousness))
        self.add_widget(self.get_labeled_slider('Forgiving', 'Critical', self.slider_criticlevel))
        self.add_widget(self.get_labeled_slider('Trusting', 'Sceptical', self.slider_userbelief))
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
        self.dependent_box.spinner.values.append(bot_name)
        self.dependent_box.spinner.text = bot_name
        self.carousel.index = 0
    
    def clean_text(self, to_clean: str):
        return to_clean.strip().replace(" ", "-")
        
    def get_voices(self):
        return ['bf_emma', 'bf_isabella', 'bm_george', 'bm_fable', 'am_puck', 'am_michael', 'af_bella', 'af_heart']
    
    def get_label_box(self, w_1, w_2):
        label_box = BoxLayout(orientation='horizontal', padding=(0, 0))
        left_label = Label(text=w_1, halign="left", size_hint_x=None, width=150, font_size=30)
        right_label = Label(text=w_2, halign="right", size_hint_x=None, width=150, font_size=30)
        label_box.add_widget(left_label)
        label_box.add_widget(Label(size_hint_x=1))
        label_box.add_widget(right_label)
        return label_box
    
    def get_labeled_slider(self, w_1, w_2, slider):
        box = BoxLayout(orientation="vertical", spacing=0, padding=(10, 10))
        box.add_widget(self.get_label_box(w_1, w_2))
        box.add_widget(slider)
        return box

        

class MotivationBotApp(App):
    def build(self):
        confirm_dirs('audio_data')
        confirm_dirs('custom_models')

        main_box = BoxLayout(orientation='vertical')
        carousel = Carousel(direction="right")
        box_1 = MyBotWidget()
        box_2 = NewBotWidget(box_1, carousel)
        carousel.add_widget(box_1)
        carousel.add_widget(box_2)
        main_box.add_widget(carousel)
        return main_box

if __name__ == '__main__':
    MotivationBotApp().run()
