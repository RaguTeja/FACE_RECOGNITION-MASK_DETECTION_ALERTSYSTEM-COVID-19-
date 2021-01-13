from tensorflow.keras.layers import Dense,Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16
from glob import glob
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img

IMAGE_SIZE=[224,224]

train_path='./Images/train'
test_path='./Images/test'

model=VGG16(input_shape=IMAGE_SIZE+[3],weights='imagenet',include_top=False)

model.summary()


for layer in model.layers:
    layer.trainable=False
    
model.summary()

folders=glob(r"/Datasets/train/*")
print(folders)


x=Flatten()(model.output)
predict=Dense(len(folders),activation='softmax')(x)

model=Model(inputs=model.input,outputs=predict)

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

model.summary()

train_datagen=ImageDataGenerator(rescale=1./255,
                                 shear_range=0.2,zoom_range=0.2,horizonal_flip=True)
test_datagen=ImageDataGenerator(rescale=1./255)

train_data=train_datagen.flow_from_directory(train_path,target_size=(224,224),
                                             batch_size=90,class_mode='categorical')

test_data=test_datagen.flow_from_directory(test_path,target_size=(224,224),
                                             batch_size=90,class_mode='categorical')



history=model.fit(train_data,validation_data=test_data,epochs=10,steps_per_epoch=len(train_data),
                  validation_steps=len(test_data)))
