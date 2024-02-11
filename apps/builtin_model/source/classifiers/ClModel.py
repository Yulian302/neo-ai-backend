from keras import Model
from keras.applications import VGG16
from keras.layers import Flatten, Dense, Dropout, Input
from keras.optimizers.legacy import Adam
from keras.saving import register_keras_serializable


def init_model():
    input_layer = Input(shape=(512, 512, 3))
    x = ClModel(
        (512, 512, 3),
        n_units_fc1=128,
        n_units_fc2=128,
        d_rate1=0.3,
        d_rate2=0.2,
        n_classes=4,
    )(input_layer)
    model = Model(inputs=input_layer, outputs=x)
    # print(model.summary(expand_nested=True))
    compile_model(model)


def compile_model(model):
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss="sparse_categorical_crossentropy",
        metrics=["sparse_categorical_accuracy", "accuracy"],
    )


@register_keras_serializable()
class ClModel(Model):
    predictions = {0: "glioma", 1: "meningioma", 2: "no tumors", 3: "petituary"}

    def __init__(
        self, input_shape, n_units_fc1, n_units_fc2, d_rate1, d_rate2, n_classes
    ):
        super(ClModel, self).__init__()

        self.vgg_16 = VGG16(
            input_shape=input_shape, include_top=False, weights="imagenet"
        )

        for layer in self.vgg_16.layers:
            layer.trainable = False

        self.vgg_16.layers[-2].trainable = True
        self.vgg_16.layers[-3].trainable = True
        self.vgg_16.layers[-4].trainable = True

        self.flatten = Flatten()
        self.dropout1 = Dropout(d_rate1)
        self.dense1 = Dense(n_units_fc1)
        self.dropout2 = Dropout(d_rate2)
        self.out = Dense(n_classes, activation="softmax")

    def call(self, inputs, training=False, add_title=None):
        x_ = self.vgg_16(inputs)
        x_ = self.flatten(x_)
        if training:
            x_ = self.dropout1(x_)
        x_ = self.dense1(x_)
        if training:
            x_ = self.dropout2(x_)
        x_ = self.out(x_)
        return x_
