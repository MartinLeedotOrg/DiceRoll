from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import random

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config.update(JSONIFY_PRETTYPRINT_REGULAR = False)

parser = reqparse.RequestParser()
parser.add_argument('quantity', type=int, help='Number of dice you want to roll (defaults to 1)')
parser.add_argument('sides', type=int, help='Sides of the dice (defaults to 6)')


class Dice:
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)


class DiceTower:

    def __init__(self, sides, quantity):
        self.results = dict()
        self.sides = sides
        self.quantity = quantity
        self.die = Dice(sides=self.sides)

    def tumble(self):
        self.results['sum'] = int(0)
        self.results['dice'] = list()
        for dice in range(self.quantity):
            output = self.die.roll()
            self.results['sum'] += output
            self.results['dice'].append(output)
        return self.results


class Roll(Resource):
    @staticmethod
    def get():

        args = parser.parse_args()
        sides = args['sides'] or 6
        quantity = args['quantity'] or 1

        if sides <= 0:
            return {'error': 'Dice must have at least one side. At least two, really...'}, 500

        if quantity <= 0:
            return {'error': 'You must roll at least one die.'}, 500

        if quantity >= 1000000:
            return {'error': 'We\'re gonna need a bigger boat.'}, 403

        tower = DiceTower(sides=sides, quantity=quantity)

        return jsonify(tower.tumble())


api.add_resource(Roll, '/roll')

if __name__ == '__main__':
    app.run(debug=True)
