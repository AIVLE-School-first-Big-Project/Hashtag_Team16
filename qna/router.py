class DBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'qna':
            return 'default'
        return None
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'qna':
            return 'default'
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'qna' or \
            obj2._meta.app_label == 'qna':
            return True
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'qna':
            return db == 'default'
        return None