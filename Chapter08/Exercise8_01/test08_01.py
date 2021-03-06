import unittest
import import_ipynb
import pandas as pd
import numpy as np
import pandas.testing as pd_testing
import numpy.testing as np_testing
import pathlib
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.applications import NASNetMobile


class Test(unittest.TestCase):
	def setUp(self):
		import Exercise08_01
		self.exercises = Exercise08_01

		self.file_url = 'https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip'
		self.zip_dir = tf.keras.utils.get_file('cats_and_dogs.zip', origin=self.file_url, extract=True)
		self.path = pathlib.Path(self.zip_dir).parent / 'cats_and_dogs_filtered'
		self.train_dir = self.path / 'train'
		self.validation_dir = self.path / 'validation'
		self.total_train = 2000
		self.total_val = 1000

		self.train_image_generator = ImageDataGenerator(rescale=1. / 255)
		self.validation_image_generator = ImageDataGenerator(rescale=1. / 255)
		self.batch_size = 32
		self.img_height = 224
		self.img_width = 224
		self.channel = 3
		self.train_data_gen = self.train_image_generator.flow_from_directory(batch_size=self.batch_size,
																			 directory=self.train_dir, shuffle=True,
																			 target_size=(
																			 self.img_height, self.img_width),
																			 class_mode='binary')
		self.val_data_gen = self.validation_image_generator.flow_from_directory(batch_size=self.batch_size,
																				directory=self.validation_dir,
																				target_size=(
																				self.img_height, self.img_width),
																				class_mode='binary')

		np.random.seed(8)
		tf.random.set_seed(8)

		self.base_model = NASNetMobile(include_top=False, input_shape=(self.img_height, self.img_width, self.channel), weights='imagenet')
		self.base_model.trainable = False

		self.model = tf.keras.Sequential([
			self.base_model,
			layers.Flatten(),
			layers.Dense(500, activation='relu'),
			layers.Dense(1, activation='sigmoid')
		])
		self.model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(0.001), metrics=['accuracy'])

	def test_file_url(self):
		self.assertEqual(self.exercises.file_url, self.file_url)

	def test_total_train(self):
		self.assertEqual(self.exercises.total_train, self.total_train)

	def test_total_val(self):
		self.assertEqual(self.exercises.total_val, self.total_val)

	def test_base_model_summary(self):
		self.assertEqual(self.exercises.base_model.summary(), self.base_model.summary())

	def test_model_summary(self):
		self.assertEqual(self.exercises.model.summary(), self.model.summary())


if __name__ == '__main__':
	unittest.main()
