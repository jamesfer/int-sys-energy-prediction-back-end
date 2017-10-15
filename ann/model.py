from ann.tf import tf, VariableContainer


class Model(VariableContainer):
    def __init__(self, inputs, weights, biases, outputs):
        self.inputs = inputs
        self.weights = weights
        self.biases = biases
        self.outputs = outputs
        super(Model, self).__init__([inputs, weights, biases, outputs])


class SimpleModel(Model):
    def __init__(self, input_number, output_number):
        inputs = tf.placeholder(tf.float32, [None, input_number], name='inputs')
        weights = tf.Variable(tf.zeros([input_number, 1]), name='weights')
        biases = tf.Variable(tf.zeros([output_number]), name='biases')
        nn_formula = tf.matmul(inputs, weights) + biases

        outputs = tf.nn.sigmoid(nn_formula)
        super(SimpleModel, self).__init__(inputs, weights, biases, outputs)

    def predict(self, session, inputs):
        return session.run(self.outputs, feed_dict={self.inputs: inputs})
