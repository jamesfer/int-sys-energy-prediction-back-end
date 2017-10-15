from ann.trainer import GradientDescentTrainer
from ann.model import SimpleModel
from ann.session import run_session
# from training import build_training_set
# from data import get_data_row
# from data import data_only

# row = get_data_row('hourly', 'DE')
# data = data_only(row)
# inputs, outputs, low, high = build_training_set(data, "2014", "2015", 3)
#
# model = SimpleModel(3, 1)
# trainer = GradientDescentTrainer(model)
#
#
# def run(session):
#     for _ in range(1000):
#         trainer.train(session, inputs, outputs)
#
#     for i in range(10):
#         print(model.predict(session, [inputs[i * 10]]))
#
#
# run_session([model.biases, model.weights], run)


def predict(lookback, inputs, outputs, predictions):
    # print(inputs)
    model = SimpleModel(lookback, 1)
    trainer = GradientDescentTrainer(model)
    results = None

    def predict_session(session):
        nonlocal results
        for _ in range(1000):
            trainer.train(session, inputs, outputs)
        results = model.predict(session, predictions)
    run_session([model.biases, model.weights], predict_session)
    return results.tolist()

