# Import necessary libraries
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
import cv2

class InteractiveVideoApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Camera widget
        self.camera = Camera(resolution=(640, 480))
        self.layout.add_widget(self.camera)

        # Image widget to display video effects
        self.image = Image()
        self.layout.add_widget(self.image)

        # Start/Stop button
        self.start_stop_button = Button(text="Start")
        self.start_stop_button.bind(on_press=self.toggle_camera)
        self.layout.add_widget(self.start_stop_button)

        # Label for instructions
        self.instruction_label = Label(text="Press 'Start' to begin recording")
        self.layout.add_widget(self.instruction_label)

        # Capture frames from the camera
        self.capture = cv2.VideoCapture(0)

        # Flag to control camera state
        self.is_camera_active = False

        # Schedule the update function
        Clock.schedule_interval(self.update, 1.0 / 30)  # 30 FPS

        return self.layout

    def toggle_camera(self, instance):
        if self.is_camera_active:
            self.capture.release()
            self.is_camera_active = False
            self.start_stop_button.text = "Start"
            self.instruction_label.text = "Press 'Start' to begin recording"
        else:
            self.capture.open(0)
            self.is_camera_active = True
            self.start_stop_button.text = "Stop"
            self.instruction_label.text = "Recording..."

    def update(self, dt):
        if self.is_camera_active:
            ret, frame = self.capture.read()
            if ret:
                # Process the frame here (e.g., apply video effects)
                # For simplicity, we just display the raw frame
                self.image.texture = self.texture_from_frame(frame)

    def texture_from_frame(self, frame):
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        return texture

if __name__ == '__main__':
    InteractiveVideoApp().run()