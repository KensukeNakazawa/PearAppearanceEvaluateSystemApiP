from flask import Flask

from src.api.controllers import pear_evaluate_controller

api = Flask(__name__)


@api.route('/', methods=['GET'])
def health_check():
    return 'HEALTH CHECK'


@api.route('/pear/evaluates', methods=['POST'])
def pear_evaluate():
    # if request.method == 'POST':
    # return "OK"
    return pear_evaluate_controller.pear_evaluate()


@api.route('/pear/evaluates/<int:pear_id>', methods=['GET'])
def get_pear(pear_id: int):
    return pear_evaluate_controller.get_pear(pear_id=pear_id)


@api.route('/pear/evaluates', methods=['GET'])
def get_pear_evaluates():
    return pear_evaluate_controller.get_pear_evaluates()

