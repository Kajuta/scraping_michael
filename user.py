from firebase import add_db_doc,get_db_doc,update_db_doc,delete_db_doc

COLLECTIOM_NAME = ''

class Profile():
    def __init__(self,name=None,sex=None,birthday=None,address=None,metadata=None,param_dict:dict=None) -> None:
        if param_dict is not None:
            self.name = param_dict.get('name')
            self.sex = param_dict.get('sex')
            self.birthday = param_dict.get('birthday')
            self.address = param_dict.get('address')
            self.metadata = param_dict.get('metadata')
        else:
            self.name = name
            self.sex = sex
            self.birthday = birthday
            self.address = address
            self.metadata = {} if metadata is None else metadata

class OpenaiData():
    def __init__(self,thread_id:str,metadata=None,param_dict:dict=None) -> None:
        if param_dict is not None:
            self.thread_id = param_dict.get('thread_id')
            self.metadata = param_dict.get('metadata')
        else:
            self.thread_id = thread_id
            self.metadata = {} if metadata is None else metadata 

class User():
    '''
        教えて!マイケルのLINE登録ユーザーを管理するクラス
    '''
    def __init__(self,user_id:str) -> None:
        '''
        LINEのuser_idをKeyとして、Firestoreのコレクション「Users」にアクセスしてデータを呼び出しインスタンスを生成
        存在しない場合は新たにインスタンスを生成し、Firestoreへ情報登録される
        '''
        # 情報の存在確認
        doc = get_db_doc(
            collection_name=COLLECTIOM_NAME,
            document_id=user_id
        )
        if doc.exists:
            # 存在する
            if user_id == doc.get('id'):
                self.id = user_id
                self.openai_data = OpenaiData(param_dict=doc.get('openai_data'))
                self.profile = Profile(param_dict=doc.get('profile'))
        else:
            # 存在しない
            self.id = user_id
            self.openai_data = OpenaiData()
            self.profile = Profile()

    def update_firestore_doc(self):
        '''
        現在のインスタンスの値をもとに、FirestoreのDocmentを更新する
        '''
        docment_field = self.__dict__
        docment_field.__setattr__('openai_data',docment_field.get('openai_data').__dict__)
        docment_field.__setattr__('profile',docment_field.get('profile').__dict__)

        update_result = update_db_doc(
            collection_name=COLLECTIOM_NAME,
            document_id=self.id,
            document_field=docment_field
        )
        return update_result
