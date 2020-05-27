#####   INTERNAL DB

# from backend.dbutils import check_password, check_admin, user_exists, show_users, add_user, del_user, change_password
# from backend.dbsetup import recreate_database, recreate_initial_users

#add_user('testuser', 'secretsuperpass', 'N')
#print(del_user('testuser3'))
#print(change_password('testuser', 'newtestpasss'))


# recreate_database()
# recreate_initial_users()
# print(show_users())

#####   QUIZ DB

# from backend.quizsetup import recreate_database, recreate_initial_quiz
from backend.quizutils import get_questions, get_next_question, get_questions_count, get_answers, get_all_users_answered

# recreate_database()
# recreate_initial_quiz()

# print(get_questions('GEO'))

# print(get_next_question('GEO', 1))

#
print(get_answers('GEO', 'gc'))

# print(get_all_users_answered('GEO'))
