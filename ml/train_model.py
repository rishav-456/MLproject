import cv2
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore
from tensorflow.keras.applications import ResNet50 # type: ignore
from tensorflow.keras.models import Model # type: ignore
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint # type: ignore
import tensorflow as tf
from sklearn.utils.class_weight import compute_class_weight
from constants import MODEL, BEST_MODEL

# preprocessing function
def preprocessing(image):
    """
    The function `preprocessing` converts an input image to grayscale, applies Gaussian blur, and
    creates a 3-channel image with blurred edges.
    
    :param image: The `preprocessing` function takes an input image as a parameter and performs the
    following preprocessing steps on it:
    :return: a 3-channel image where each channel contains the blurred grayscale image.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 1.4)
    edges_3_channel = cv2.merge([blurred_image, blurred_image, blurred_image])
    return edges_3_channel


# Define body shapes
shapes = ["apple", "pear", "rectangle", "inverted triangle", "hourglass"]

# Dictionary to map shapes to numerical labels
labels_annot = {shapes[i]: i for i in range(len(shapes))}


images = []
labels = []

# *--------------------------Do only one process--------------------------------------*

# Sample and process images for each shape
# Do these steps only when data folder is exist in the location utils\data
# Otherwise, use training_data folder without doing any preprocessing

# Process 1:- Using data folder

# Sample data to be use in training
myData = [] # [h,weight,c,w,hi,shape.lower(),path])

# Load data from CSV
df = pd.read_csv("utils\data\data.csv")
for shape in shapes:
    sample = df.loc[df["shape"] == shape].sample(982)  # Sample 982 images per shape
    sample.reset_index(inplace=True)
    for i in sample.index:
        img = cv2.imread(sample.loc[i, 'img'])
        img = cv2.resize(img,(224,224))
        img = preprocessing(img)  # Apply preprocessing
        cv2.imwrite(f"ml\\training_data\\{shape}\\{i+1}.png",img)
        images.append(img)
        labels.append(labels_annot[shape])
        sample.loc[i, 'img'] = f"ml\\training_data\\{shape}\\{i+1}.png"
        myData.append(list(sample.loc[i,:][1:]))

# Saving the training data information into a csv
df = pd.DataFrame(myData, columns="height weight bust waist hip shape img".split())
df.to_csv(r"ml\training_dataset.csv",index=False)

# *---------------------------------------------------------------------------------------*

# # Process 2:- Using training_data folder

# df = pd.read_csv(r"ml\training_dataset.csv")
# for shape in shapes:
#     sample = df.loc[df["shape"] == shape]
#     sample.reset_index(inplace=True)
#     for i in sample.index:
#         img = cv2.imread(sample.loc[i, 'img'])
#         img = cv2.resize(img,(224,224))
#         images.append(img)
#         labels.append(labels_annot[shape])

# *---------------------------------------------------------------------------------------*

# Convert lists to NumPy arrays
images = np.array(images)
labels = np.array(labels)

# Shuffle images and labels together
images, labels = shuffle(images, labels, random_state=42)

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

# Data augmentation
train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator()

train_generator = train_datagen.flow(X_train, y_train, batch_size=32, shuffle=True)
val_generator = val_datagen.flow(X_val, y_val, batch_size=32, shuffle=True)

# Compute class weights
class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(y_train), y=y_train)
class_weights = dict(enumerate(class_weights))

# Load the ResNet50 model, excluding the top layers
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Add custom layers on top of the base model
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)
x = Dropout(0.5)(x)
x = Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)
x = Dropout(0.5)(x)
predictions = Dense(5, activation='softmax')(x)  # 5 classes for body shapes

# Create the full model
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the layers of the base model
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Callbacks
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.00001)
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
model_checkpoint = ModelCheckpoint(BEST_MODEL, monitor='val_accuracy', save_best_only=True, mode='max')

# Train the model with callbacks
history = model.fit(train_generator,
                    epochs=50,
                    validation_data=val_generator,
                    callbacks=[reduce_lr, early_stopping, model_checkpoint],
                    class_weight=class_weights)

# Unfreeze some layers of the base model and fine-tune the model
for layer in base_model.layers[-10:]:
    layer.trainable = True

model.compile(optimizer=Adam(learning_rate=0.00001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history_fine = model.fit(train_generator,
                         epochs=20,
                         validation_data=val_generator,
                         callbacks=[reduce_lr, early_stopping, model_checkpoint],
                         class_weight=class_weights)

# Evaluate the model
val_loss, val_accuracy = model.evaluate(val_generator)
print(f'Validation Loss: {val_loss}')
print(f'Validation Accuracy: {val_accuracy}')

# Save the trained model
model.save(MODEL)