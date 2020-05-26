from backend.dbutils import check_password, check_admin, user_exists, show_users, add_user, del_user, change_password
from backend.dbsetup import recreate_database, recreate_initial_users

#add_user('testuser', 'secretsuperpass', 'N')
#print(del_user('testuser3'))
#print(change_password('testuser', 'newtestpasss'))


recreate_database()
recreate_initial_users()
print(show_users())

