import firebase_admin
from firebase_admin import credentials, db
import json


def upload_data(json_name):
    cred = credentials.Certificate('./radinmas-info-app-firebase-adminsdk-ntv76-cbef984d38.json')
    try:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://radinmas-info-app.firebaseio.com/'
        })

    except ValueError as e:
        firebase_admin.get_app()

    ref = db.reference('radin_mas/' + str(json_name) + '/')

    class_file = open(str(json_name) + ".json", "r")

    for line in class_file.readlines():
        data = json.loads(line)
        ref.set(data)



# # functional: updates retrieved data in json file to fire base
# # for course data only
#
# import firebase_admin
# from firebase_admin import credentials, db
# import json
# from pandas import DataFrame
#
# # The values of a Python dictionary can be of any data type.
# # So you don’t have to confine yourself to using constants (integers, strings),
# # you can also use function names and lambdas as values.
# # For example, you can also implement the above switch statement by
# # creating a dictionary of function names as values.
# # In this case, switcher is a dictionary of function names, and not strings.
#
#
# def upload_class_detail(db, row, index):
#     # doc_ref = db.collection(u'courses').document(u'' + row['product'] + '')
#     doc_ref = db.collection(u'classes').document(u'' + str(index) + '')
#     doc_ref.set({
#         u'product_name': row['product_name'],
#         u'product_link': row['product_link'],
#         u'price': row['price'],
#         u'date_time': row['date_time'],
#         u'session_no': row['session_no'],
#         u'class_schedule': row['class_schedule'],
#         u'location': row['location'],
#         u'venue': row['venue'],
#         u'closing_date': row['closing_date'],
#         u'vacancy_left': row['vacancy_left'],
#         u'max_participant': row['max_participant']
#     })
#
#
# def upload_interest_detail(db, row, index):
#     # doc_ref = db.collection(u'courses').document(u'' + row['product'] + '')
#     doc_ref = db.collection(u'interests').document(u'' + str(index) + '')
#     doc_ref.set({
#         u'product_name': row['product_name'],
#         u'product_link': row['product_link'],
#         u'location': row['location'],
#         u'membership_period': row['membership_period'],
#         u'vacancy': row['vacancy']
#     })
#
#
# def upload_event_detail(db, row, index):
#     # doc_ref = db.collection(u'courses').document(u'' + row['product'] + '')
#     doc_ref = db.collection(u'events').document(u'' + str(index) + '')
#     doc_ref.set({
#         u'product_name': row['product_name'],
#         u'product_link': row['product_link'],
#         u'date_time': row['date_time'],
#         u'location': row['location'],
#         u'event_schedule': row['event_schedule'],
#         u'venue': row['venue'],
#         u'closing_date': row['closing_date'],
#         u'vacancy_left': row['vacancy_left'],
#         u'max_participant': row['max_participant']
#     })
#
#
# def upload_data():
#
#     cred = credentials.Certificate('./radinmas-info-app-firebase-adminsdk-ntv76-cbef984d38.json')
#     firebase_admin.initialize_app(cred, {
#         'databaseURL': 'https://radinmas-info-app.firebaseio.com/'
#     })
#     # app = firebase_admin.get_app()
#     #
#     # cred = credentials.Certificate('./radinmas-info-app-firebase-adminsdk-ntv76-cbef984d38.json')
#     # firebase_admin.initialize_app(cred)
#
#     #db = firestore.client()
#
#     ref = db.reference('restricted_access/secret_document')
#     print(ref.get())
#
#     class_data = json.load(open('./Class.json'))
#     interest_data = json.load(open('./Interest.json'))
#     event_data = json.load(open('./Event.json'))
#
#     class_df = DataFrame(class_data)
#     interest_df = DataFrame(interest_data)
#     event_df = DataFrame(event_data)
#
#     for index, row in class_df.iterrows():
#         upload_class_detail(db, row, index)
#
#     for index, row in interest_df.iterrows():
#         upload_interest_detail(db, row, index)
#
#     for index, row in event_df.iterrows():
#         upload_event_detail(db, row, index)
#
#     #
#     # batch = db.batch()
#     # classes_ref = db.collection(u'classes')
#     # interests_ref = db.collection(u'interests')
#     # events_ref = db.collection(u'events')
#     #
#     # batch.set(classes_ref)
#     # batch.set(interests_ref)
#     # batch.set(events_ref)
#     #
#     # batch.commit()
#     #
#     # print("Done")
#
#     # for index, row in df.iterrows():
#     #     get_class_details(db, row, index)
#
#     # switcher = {
#     #     "Class": [upload_class_detail(db, row, df) for index, row in df.iterrows()],
#     #     "Interest": [upload_interest_detail(db, row, df) for index, row in df.iterrows()],
#     #     "Event": [upload_event_detail(db, row, df) for index, row in df.iterrows()],
#     # }
#     # # Get the function from switcher dictionary
#     # func = switcher.get(argument, lambda: "Invalid month")
#     # # Execute the function
#     # func()
#
#
#     # courses_ref = db.collection(u'courses')
#     # docs = courses_ref.get()
#     #
#     # for doc in docs:
#     #     print(u'{} => {}'.format(doc.id, doc.to_dict()))
#
#
#
