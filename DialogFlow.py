from flask import Flask, make_response, request, jsonify

app = Flask(__name__)


# initialize the flask appapp = Flask(__name__)

# create a route for webhook
@app.route('/webhook')
def hello():
    return 'Hello World!'


# run the app
if __name__ == '__main__':
    app.run()
    hello()
# # function for responses
# def results():
#     # build a request object
#     req = request.get_json(force=True)
# # fetch action from json
#     action = req.get('queryResult').get('action')
# # return a fulfillment response
#     return {'fulfillmentText': 'This is a response from webhook.'}
# # create a route for webhook
# @app.route('/webhook', methods=['GET', 'POST'])
# def webhook():
#     # return response
#     return make_response(jsonify(results()))