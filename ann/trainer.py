from ann.tf import tf, VariableContainer


class GradientDescentTrainer(VariableContainer):
    def __init__(self, model):
        self.inputs = model.inputs
        dims = [None, model.outputs.shape.dims[1]]
        self.goals = tf.placeholder(tf.float32, dims, name='goals')

        cost_eq = mean_squared_error(model.outputs, self.goals)
        self.cost = tf.reduce_mean(cost_eq)

        optimizer = tf.train.GradientDescentOptimizer(0.5)
        self.train_step = optimizer.minimize(self.cost)
        super(GradientDescentTrainer, self).__init__([self.goals])

    def train(self, session, inputs, outputs):
        session.run(self.train_step, feed_dict={
            self.inputs: inputs,
            self.goals: outputs,
        })


def mean_squared_error(outputs, goals):
    return tf.reduce_mean(tf.squared_difference(goals, outputs), 1)
