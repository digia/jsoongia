from unittest import TestCase
from .. import Serializer, relationships


class PollSerializer(Serializer):
    type = 'poll'
    attributes = [
        'question', 'multiple_choice', 'multiple_votes', 'created_at', 'updated_at', 
    ]
    relationships = {
        'answer': {
            'serializer': 'jsoongia.test.serialization.AnswerSerializer',
            'relationship': relationships.HasMany('poll_id')
        }
    }


class AnswerSerializer(Serializer):
    type = 'poll.answer'
    attributes = ['text']
    relationships = {
        'poll': {
            'serializer': PollSerializer,
            'relationship': relationships.BelongsTo()
        }
    }


class UuidRefSerializer(Serializer):
    ref = 'uuid'
    type = 'uuid.ref'
    

