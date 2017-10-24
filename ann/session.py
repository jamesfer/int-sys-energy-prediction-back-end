from .tf import tf, VariableContainer
import numpy as np
import os.path


def flatten(var_list):
    return np.ravel([
        v.variables if isinstance(v, VariableContainer) else v
        for v in var_list
    ])


def run_session(var_list, cb):
    modelSaved = os.path.exists('./tmp/model.ckpt.meta')
    initializer = tf.variables_initializer(var_list)
    print(var_list)
    saver = tf.train.Saver()
    print("model saved: %s" % modelSaved)
    with tf.Session() as session:
        # restore saved model
        if modelSaved:
            result = saver.restore(session, './tmp/model.ckpt')
        else:
            session.run(initializer)
        
        print(session.run(var_list[0])) # prints biases
        print(session.run(var_list[1])) # prints weights
        

        cb(session)
