from .tf import tf, VariableContainer
import numpy as np
import os.path

settings = {}

def flatten(var_list):
    return np.ravel([
        v.variables if isinstance(v, VariableContainer) else v
        for v in var_list
    ])


def run_session(var_list, cb):
    modelSaved = os.path.exists('./tmp/model.ckpt.meta')
    initializer = tf.variables_initializer(var_list)
    with tf.Session() as session:
        session.run(initializer)
        
        cb(session)



def modelExists(settings):
    filename = getFilename(settings)
    return os.path.exists('./models/'+filename+'.ckpt.meta')

def saveModel(session, settings):
    filename = getFilename(settings)
    saver = tf.train.Saver()
    save_path = saver.save(session, './models/'+filename+'.ckpt')
    print("Model saved in file: %s" % save_path)

def restoreModel(session, settings):
    filename = getFilename(settings)
    saver = tf.train.Saver()
    saver.restore(session, './models/'+filename+'.ckpt')

def getFilename(settings):
    return 'model-' + str(settings['country']) + '-' + str(settings['interval']) + '-' + str(settings['compressed']) + '-' + str(settings['lookback'])
