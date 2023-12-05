import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from keras.callbacks import Callback
from carbon_track import CarbonTrack

ct = CarbonTrack('firebase-token.json path', 'firebase-database-url', 'carbon-api-key')

class CustomCallback(Callback):
    def on_epoch_begin(self, epoch, logs=None):
        print(f"Start of epoch {epoch + 1}")
        ct.collect()


# Data loading and preprocessing
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# Model configuration
model = models.Sequential()
model.add(layers.Conv2D(256, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(512, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

# Compiling the Model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Output Model Summary
model.summary()

# Train the model
custom_callback_instance = CustomCallback()
model.fit(train_images, train_labels, epochs=5, batch_size=64, validation_split=0.2, callbacks=[custom_callback_instance])

# Evaluate models
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f'Test accuracy: {test_acc}')

print("get firebase data")
log = ct.getdata(local=True)
print(log)