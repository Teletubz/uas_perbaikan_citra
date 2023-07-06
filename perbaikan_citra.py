import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#gilang pranatha
#312210371

class ImageEnhancementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Enhancement Application")
        self.root.configure(background='teal')
        self.image = None
        self.original_image = None

        self.create_widgets()

    def create_widgets(self):
        upload_button = ttk.Button(self.root, text="Upload Image for Enhancement", command=self.load_image)
        upload_button.pack(pady=10)

        self.filtering_combobox = ttk.Combobox(self.root, values=['Histogram Equalization', 'Median Filter'], state='disabled')
        self.filtering_combobox.pack()
        self.filtering_combobox.bind('<<ComboboxSelected>>', self.apply_filter)

        self.mse_label = ttk.Label(self.root, text="MSE: ", background='teal', foreground='white')
        self.mse_label.pack(pady=5)

        self.psnr_label = ttk.Label(self.root, text="PSNR: ", background='teal', foreground='white')
        self.psnr_label.pack(pady=5)

        self.original_image_label = ttk.Label(self.root)
        self.original_image_label.pack(pady=10)

        self.filtered_image_label = ttk.Label(self.root)
        self.filtered_image_label.pack(pady=10)

        self.frame_top = ttk.Frame(self.root)
        self.frame_top.pack()

        self.image_axes = plt.figure(figsize=(3, 3)).add_subplot(111)
        self.image_axes.axis("off")
        self.canvas_gambar_asli = FigureCanvasTkAgg(self.image_axes.figure, master=self.frame_top)
        self.canvas_gambar_asli.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)
        self.label_gambar_asli = ttk.Label(self.frame_top, text="Original Image", background='teal', foreground='white')
        self.label_gambar_asli.pack(side=tk.LEFT, padx=(0, 10))

        self.image_axes_filter = plt.figure(figsize=(3, 3)).add_subplot(111)
        self.image_axes_filter.axis("off")
        self.canvas_gambar_filter = FigureCanvasTkAgg(self.image_axes_filter.figure, master=self.frame_top)
        self.canvas_gambar_filter.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)
        self.label_filter = ttk.Label(self.frame_top, text="Enhanced Image", background='teal', foreground='white')
        self.label_filter.pack(side=tk.LEFT, padx=(0, 10))

    def load_image(self):
        file_path = filedialog.askopenfilename()
        self.image = cv2.imread(file_path)
        self.original_image = self.image.copy()

        # Convert image to PIL format for display in Tkinter
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        self.original_image = Image.fromarray(self.original_image)

        # Resize image for display
        self.original_image = self.original_image.resize((300, 300))

        # Update image label
        self.original_image_label.configure(image=ImageTk.PhotoImage(self.original_image))

        # Update image in the Matplotlib canvas
        self.image_axes.imshow(self.original_image)
        self.canvas_gambar_asli.draw()

        # Enable filtering combo box
        self.filtering_combobox.config(state='enabled')

    def apply_histogram_equalization(self):
        img_yuv = cv2.cvtColor(self.image, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        result = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        return result

    def apply_median_filter(self):
        result = cv2.medianBlur(self.image, 3)
        return result

    def calculate_mse(self, original, filtered):
        resized_original = cv2.resize(original, (filtered.shape[1], filtered.shape[0]))
        mse = np.mean((resized_original - filtered) ** 2)
        return mse

    def calculate_psnr(self, mse):
        max_pixel_value = 255.0
        psnr = 10 * np.log10((max_pixel_value ** 2) / mse)
        return psnr

    def apply_filter(self, event=None):
        if self.image is None:
            return

        selected_filter = self.filtering_combobox.get()
        if selected_filter == 'Histogram Equalization':
            filtered_image = self.apply_histogram_equalization()
        elif selected_filter == 'Median Filter':
            filtered_image = self.apply_median_filter()
        else:
            return

        mse = self.calculate_mse(np.array(self.original_image), filtered_image)
        psnr = self.calculate_psnr(mse)
        self.mse_label.config(text="MSE: {:.2f}".format(mse))
        self.psnr_label.config(text="PSNR: {:.2f}".format(psnr))

        # Convert filtered image to PIL format for display in Tkinter
        filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)
        filtered_image = Image.fromarray(filtered_image)

        # Resize image for display
        filtered_image = filtered_image.resize((300, 300))

        # Update image label
        self.filtered_image_label.configure(image=ImageTk.PhotoImage(filtered_image))

        # Update image in the Matplotlib canvas
        self.image_axes_filter.imshow(filtered_image)
        self.canvas_gambar_filter.draw()

# Run the application
root = tk.Tk()
app = ImageEnhancementApp(root)
root.mainloop()
