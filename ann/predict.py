from ann.trainer import GradientDescentTrainer
from ann.model import SimpleModel
from ann.session import run_session


def predict(lookback, inputs, outputs, predictions):
    model = SimpleModel(lookback, 1)
    trainer = GradientDescentTrainer(model)
    results = None

    def predict_session(session):
        nonlocal results
        for _ in range(30000):
            trainer.train(session, inputs, outputs)
        results = model.predict(session, predictions)
    run_session([model.biases, model.weights], predict_session)
    return results.tolist()

