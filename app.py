from flask import Flask
from flask_restful import Resource, Api
import random

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Dice:
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        return random.randint(1,self.sides)


class Roll(Resource):
    def get(self):
        d6 = Dice(sides=6)
        return d6.roll()


api.add_resource(HelloWorld, '/')
api.add_resource(Roll, '/roll')

if __name__ == '__main__':
    app.run(debug=True)