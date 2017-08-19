from flask import Flask
from flask_restful import Resource, Api, reqparse
import random

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('quantity', type=int, help='Number of dice you want to roll (defaults to 1)')
parser.add_argument('sides', type=int, help='Sides of the dice (defaults to 6)')

class Dice:
    def __init__(self, sides):
        self.sides = sides

    def roll(self) -> object:
        return random.randint(1,self.sides)

class Roll(Resource):

    def get(self):
        results = dict()
        results['sum'] = int(0)
        results['dice'] = list()

        args = parser.parse_args()
        sides = args['sides'] or 6
        quantity = args['quantity'] or 1

        if sides <= 0:
            return {'error': 'Dice must have at least one side. At least two, really...'}, 500

        if quantity <= 0:
            return {'error': 'You must roll at least one die'}, 500

        for dice in range(quantity):
            output = Dice(sides=sides).roll()
            results['sum'] += output
            results['dice'].append(output)

        return results

api.add_resource(Roll, '/roll')

if __name__ == '__main__':
    app.run(debug=True)
