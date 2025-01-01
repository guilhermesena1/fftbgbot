import tensorflow as tf
def get_fftbg_model():
    return tf.keras.Sequential([
      tf.keras.layers.Input(shape=(3624, 2)),
      tf.keras.layers.Conv1D(8, 4, activation='relu'),
      tf.keras.layers.Conv1D(16, 8, activation='relu'),
      #tf.keras.layers.MaxPooling1D(),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(8, activation='relu'),
      tf.keras.layers.Dense(1, activation='sigmoid')
    ])