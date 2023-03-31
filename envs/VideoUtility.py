import os
import pygame
import moviepy.video.io.ImageSequenceClip
import shutil


class VideoUtility:
    def __init__(self):
        if 'output' not in os.listdir():
            os.mkdir('output')
        self.output_dir = os.path.abspath('output')
        self.current_sequence_dir = None
        self.current_filename = None
        self.image_files = []

    def initialize(self, filename):
        self.current_filename = filename
        self.current_sequence_dir = os.path.join(self.output_dir, filename + '_im_seq')
        if os.path.basename(self.current_sequence_dir) in os.listdir(self.output_dir):
            shutil.rmtree(self.current_sequence_dir)
        os.mkdir(self.current_sequence_dir)

    def save_image(self, image_name, surf):
        image_filename = os.path.join(self.current_sequence_dir, image_name)
        pygame.image.save(surf, image_filename)
        self.image_files.append(image_filename)

    def compile_images(self):
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(self.image_files, fps=15)
        clip.write_videofile(os.path.join(self.output_dir, self.current_filename + '.mp4'))
        shutil.rmtree(self.current_sequence_dir)
        self.current_sequence_dir = None
        self.current_filename = None
        self.image_files = []