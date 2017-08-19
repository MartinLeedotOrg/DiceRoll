from flask import Flask
from flask_restful import Resource, Api, reqparse
from collections import OrderedDict
import random

app = Flask(__name__)
api = Api(app)

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
        self.results = OrderedDict()
        self.sides = sides
        self.quantity = quantity

    def tumble(self):
        self.results['sum'] = int(0)
        self.results['dice'] = list()
        for dice in range(self.quantity):
            output = Dice(sides=self.sides).roll()
            self.results['sum'] += output
            self.results['dice'].append(output)
        return self.results


class Roll(Resource):
    def get(self):

        args = parser.parse_args()
        sides = args['sides'] or 6
        quantity = args['quantity'] or 1

        if sides <= 0:
            return {'error': 'Dice must have at least one side. At least two, really...'}, 500

        if quantity <= 0:
            return {'error': 'You must roll at least one die'}, 500

        tower = DiceTower(sides=sides, quantity=quantity)

        return tower.tumble()


api.add_resource(Roll, '/roll')

if __name__ == '__main__':
    app.run(debug=True)
