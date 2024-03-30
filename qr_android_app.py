from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
import qrcode, qr_code_generator, os
from kivy.clock import Clock

Window.size = 360, 640  #Window size
Window.clearcolor = (1, 1, 1, 1)    #White background

qr = qrcode.QRCode(version = 1,     #qrcode object
                    error_correction = qrcode.constants.ERROR_CORRECT_L,
                    box_size = 50,
                    border = 10)

class Function(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 6    #initial counter
        self.code = str()   #data of qrcode
        self.folder = "qr_code_image/"
    def generate(self, root):   #Function that will be called when clicked 'Generate' button
        self.count = self.counter   #counter that will display on screen(5-4-3-2-1-0)
        self.image_generate(root)
        self.update(root)
        Clock.schedule_interval(self.update, 1) #update function will be called in a second intervals.
    def update(self, *kwargs):  #counter update
        if self.count == 0:
            self.image_generate(*kwargs)    #QR image will be generated if count is 0
            self.count = 6
        self.count -= 1
        self.ids.timing.text = str(self.count)  #display the counter
        
    def image_generate(self, root):
        for filename in os.listdir(self.folder):
            file_path = os.path.join(self.folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except :
                pass
        code = qr_code_generator.randomize() #randomized code
        self.code = code
        qr.clear() #clear qr data
        qr.add_data(code)   #add data to qr
        qr.make(fit = True)
        qrimg = qr.make_image(fill_color = "black", back_color = "white") #create image with colors
        qrimg.save(f"{self.folder}{code}", format = 'PNG')    #save qrcode as file
        self.ids.qr_image.source = f"{self.folder}{code}"    #display the image
        self.ids.qr_code.text = code[qr_code_generator.initial_code_length:]    #display random part of the code
    def stop(self, root):
        Clock.unschedule(self.update)   #timer will stop when clicked 'Stop' button
class MyApp(MDApp):
    Builder.load_file('layout.kv')  #load the layout file
    def build(self):
        return Function()
    
if __name__ == "__main__":
    MyApp().run()
