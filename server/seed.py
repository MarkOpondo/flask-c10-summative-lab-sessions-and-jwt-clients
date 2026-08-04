import random
from faker import Faker
from app import create_app, db
from app.models import User, Note

fake = Faker()

app = create_app("development")

with app.app_context():
    print("Clearing existing database tables")

    db.session.query(User).delete()
    db.session.query(Note).delete()
    db.session.commit()

    print("Populating users database")
    user_list = []

    test_user = User(username = "Mark")
    test_user.password_hash = "mark12345"

    user_list.append(test_user)

    for _ in range(10):
        username = fake.unique.user_name()
        user = User(username=username)
        user.password_hash = "opondo54321"
        user_list.append(user)

    db.session.add_all(user_list)

    db.session.flush()

    print("Populating notes database")
    note_list = []

    for user in user_list:
        num_of_notes = random.randint(1,5)

        for _ in range(num_of_notes):
            note = Note(
                title = fake.sentence(nb_words=3).rstrip('.'),
                body = fake.text(max_nb_chars=200),
                user_id = user.id
            )

            note_list.append(note)

    
    db.session.add_all(note_list)
    db.session.commit()

    print(f"{len(user_list), len(note_list)}")