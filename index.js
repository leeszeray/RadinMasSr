// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Suggestion} = require('dialogflow-fulfillment');
const {dialogflow, BasicCard, BrowseCarousel, BrowseCarouselItem, Button, Carousel, Image, LinkOutSuggestion, List, MediaObject, Suggestions, SimpleResponse, Table} = require('actions-on-google');
const {actionssdk} = require('actions-on-google');

var config = {
    credential: admin.credential.applicationDefault(),
    databaseURL: 'https://radinmas-info-app.firebaseio.com/'
};
admin.initializeApp(config);
process.env.DEBUG = 'dialogflow:debug';
const app = dialogflow({debug: true});
const db = admin.database();

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });

  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));

  function welcome(agent) {
    agent.add(`Welcome to Radin Mas Info App! I could help with queries related to Class, Interest and Event details. How would you like to proceed?`);
    agent.add(new Card({
      	title: `Hello!💁`,
      	text: `Welcome to Radin Mas Info App! I could help with queries related to Class, Interest and Event details. How would you like to proceed? State one of the information types you would like to hear about.`
    }));
    agent.add(new Suggestion(`Classes.`));
    agent.add(new Suggestion(`Interest Groups.`));
    agent.add(new Suggestion(`Events.`));
  }

  function fallback(agent) {
    agent.add(`I didn't understand`);
    agent.add(`I'm sorry, can you try again?`);
  }

  function introClass(agent) {
    agent.add(`You have entered Class conversation flow. Please state how you would like to query for your class details. Refer to the suggestions for sameple queries.`);
    var ref = db.ref("radin_mas/classes/product_name");
    ref.on("value", function(snapshot) {
      var s = snapshot.val().toString();
      var arr = s.split(",", 3);
      agent.add(new Card({
        	title: `You have entered Class conversation flow.`,
        	text: `Please state how you would like to query for your class details. Refer to the suggestions for sample queries.`
      }));

      agent.add(new Suggestion(arr[0].toString() + ` classes`));
      agent.add(new Suggestion(arr[1].toString() + ` classes`));
      agent.add(new Suggestion(arr[2].toString() + ` classes`));

    }, function (errorObject) {
      console.log("The read failed: " + errorObject.code);
    });
  }

   function checkAppointment (agent) {
     const product_name = agent.parameters.product_name;
     

     // This variable needs to hold an instance of Date object that specifies the start time of the appointment.
     const dateTimeStart = convertTimestampToDate(agent.parameters.product_name);
     // This variable holds the end time of the appointment, which is calculated by adding an hour to the start time.
     const dateTimeEnd = addHours(dateTimeStart, 1);
     // Convert the Date object into human-readable strings.
     const appointmentTimeString = getLocaleTimeString(dateTimeStart);
     const appointmentDateString = getLocaleDateString(dateTimeStart);
     // The checkCalendarAvailablity() function checks the availability of the time slot.
     return checkCalendarAvailablity(dateTimeStart, dateTimeEnd).then(() => {
       // The time slot is available.
       // The function returns a response that asks for the confirmation of the date and time.
       agent.add(`Okay, ${appointmentDateString} at ${appointmentTimeString}. Did I get that right?`);
     }).catch(() => {
       // The time slot is not available.
       agent.add(`Sorry, we're booked on ${appointmentDateString} at ${appointmentTimeString}. Is there anything else I can do for you?`);
       // Delete the context 'MakeAppointment-followup' to return the flow of conversation to the beginning.
       agent.context.delete('makeappointment-followup');
     });
   }

  function specificClass(agent){
	  var className = agent.parameters.class_name;

	  return db.collection('classes').doc(className).get()
	    .then( doc => {
	      var value = doc.data();
	      agent.add(`Date Time for ${className} is ${value.date_time}.`);
	    });
	  }

  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('Specific Class Intent', specificClass);
  intentMap.set('Intro Class intent', introClass);

  // intentMap.set('Event intent', introEvent);
  // intentMap.set('Interest intent', introInterest);
  // intentMap.set('your intent name here', yourFunctionHandler);

  exports.webhook = functions.https.onRequest(app);

  agent.handleRequest(intentMap);
});
