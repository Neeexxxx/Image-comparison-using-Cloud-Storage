import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def get_metadata():
    cred = credentials.Certificate('newAccessKey.json')
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    docs = db.collection(u'Training').stream()
    
    for doc in docs:
        # print(f'{doc.id} => {doc.to_dict()}')
        obj=doc.to_dict()
        print(obj['pHash'])
    
get_metadata()