from faker import Faker


def poll(id):
    f = Faker()

    return {
        'id': id,
        'question': f.sentence(nb_words=5),
        'multiple_choice': f.pybool(),
        'multiple_votes': f.pybool(),
    }

def answer(id, poll_id):
    f = Faker()

    return {
        'id': id,
        'text': f.sentence(nb_words=3),
        'poll_id': poll_id,
    }
