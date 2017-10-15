from .tf import tf, VariableContainer
import numpy as np


def flatten(var_list):
    return np.ravel([
        v.variables if isinstance(v, VariableContainer) else v
        for v in var_list
    ])


def run_session(var_list, cb):
    initializer = tf.variables_initializer(var_list)
    with tf.Session() as session:
        session.run(initializer)
        cb(session)
