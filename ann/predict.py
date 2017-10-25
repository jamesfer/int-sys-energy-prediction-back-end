from ann.trainer import GradientDescentTrainer
from ann.model import SimpleModel
from ann.session import run_session, restoreModel, modelExists, saveModel

import os.path

import tensorflow as tf

def predict(train, lookback, inputs, outputs, predictions, settings):
    model = SimpleModel(lookback, 1)
    trainer = GradientDescentTrainer(model)
    results = None

    def predict_session(session):
        nonlocal results

        modelSaved = modelExists(settings)

        if modelSaved:
            print("model is saved, restoring model!")
            restoreModel(session, settings)
        else:
            print("model is not saved, not restored!")

        # train the data if client asked for it
        if train:
            for _ in range(30000):
                trainer.train(session, inputs, outputs)
        
        print(session.run(model.biases)) # prints biases
        print(session.run(model.weights)) # prints weights

        # save model to file
        if train:
            saveModel(session,settings)
        
        results = model.predict(session, predictions)
        
    run_session([model.biases, model.weights], predict_session)
    return results.tolist()

