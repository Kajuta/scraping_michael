import os
import firebase_admin
from firebase_admin import credentials , firestore
from google.cloud.firestore import Client

firebase_sdk_local_path = '/Users/pinkbpompom/Downloads/seikyo-scraping-line-firebase-adminsdk-5gfm4-1d7a705788.json'

# 本番
if os.getenv('GOOGLE_APPLICATION_CREDENTIALS') != None:
    fb_app = firebase_admin.initialize_app()
    is_cred = fb_app.credential

# ローカル時の設定
else:
    cred = credentials.Certificate(firebase_sdk_local_path)
    fb_app = firebase_admin.initialize_app(cred)


def get_firestore_client():
    db:Client = firestore.client(fb_app)
    return db

def get_db_doc(collection_name,document_id):
    db = get_firestore_client()
    return db.collection(collection_name).document(document_id).get()

def add_db_doc(collection_name, document_id,document_field):
    db = get_firestore_client()
    return db.collection(collection_name).add(document_field,document_id)

def update_db_doc(collection_name, document_id,document_field):
    db = get_firestore_client()
    return db.collection(collection_name).document(document_id).update(document_field)

def delete_db_doc(collection_name,document_id):
    db = get_firestore_client()
    return db.collection(collection_name).document(document_id).delete()

