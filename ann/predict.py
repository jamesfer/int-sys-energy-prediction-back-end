from ann.trainer import GradientDescentTrainer
from ann.model import SimpleModel
from ann.session import run_session

import os.path

import tensorflow as tf

def predict(train, lookback, inputs, outputs, predictions):
    model = SimpleModel(lookback, 1)
    trainer = GradientDescentTrainer(model)
    results = None

    def predict_session(session):
        nonlocal results
        # train the data if client asked for it
        if train:
            for _ in range(30000):
                trainer.train(session, inputs, outputs)
        
        # save model to file
        modelSaved = os.path.exists('./tmp/model.ckpt.meta')

        if train:
            saver = tf.train.Saver()
            save_path = saver.save(session, './tmp/model.ckpt')
            print("Model saved in file: %s" % save_path)
        
        results = model.predict(session, predictions)
        
    run_session([model.biases, model.weights], predict_session)
    return results.tolist()

