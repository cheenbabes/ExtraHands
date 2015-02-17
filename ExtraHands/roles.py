from rolepermissions.roles import AbstractUserRole

class Client(AbstractUserRole):
    available_permissions = {
        'create_event': True
    }

class Teacher(AbstractUserRole):
    available_permissions ={
        'create_available_time': True
    }
