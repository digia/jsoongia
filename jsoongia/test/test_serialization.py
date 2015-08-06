from unittest import TestCase
from .. import Serializer, relationships
from .serialization import PollSerializer, AnswerSerializer, UuidRefSerializer
from .generators import poll, answer


class BelongsToRelationshipTestCase(TestCase):
    def it_should_build_reference(self):
        belongs_to = relationships.BelongsTo()

        included = [poll(1), poll(2)]
        data = answer(20, 1)

        parsed = belongs_to.parse(PollSerializer, data, included)

        self.assertTrue(parsed['type'])
        self.assertTrue(parsed['id'])
        self.assertEquals(1, parsed['id'])
        self.assertEquals(PollSerializer.type, parsed['type'])

    def it_should_build_reference_with_only_one_include(self):
        belongs_to = relationships.BelongsTo()

        included = poll(1)
        data = answer(20, 1)

        parsed = belongs_to.parse(PollSerializer, data, included)

        self.assertTrue(parsed['type'])
        self.assertTrue(parsed['id'])
        self.assertEquals(1, parsed['id'])
        self.assertEquals(PollSerializer.type, parsed['type'])


class HasManyRelationshipTestCase(TestCase):
    def it_should_handle_a_has_many_relationship(self):
        has_many = relationships.HasMany('poll_id')

        # anser(id, poll_id)
        included = [answer(1, 1), answer(2, 1), answer(3, 2)]
        data = poll(1)

        parsed = has_many.parse(AnswerSerializer, data, included)

        self.assertEquals(2, len(parsed['data']))

    def it_should_handle_a_has_many_with_only_one_include(self):
        has_many = relationships.HasMany('poll_id')

        # anser(id, poll_id)
        included = answer(1, 1)
        data = poll(1)

        parsed = has_many.parse(AnswerSerializer, data, included)

        self.assertTrue(parsed['data']['id'])
        self.assertTrue(parsed['data']['type'])
        

class SerializerTestCase(TestCase):
    def it_should_init(self):
        self.assertIsInstance(Serializer(), Serializer)

    def it_only_serializes_attributes(self):
        s = PollSerializer()
        data = poll(1)

        data['not_a_attribute'] = 'hello'

        serialized = s.serialize(data)

        self.assertTrue(serialized['data'])
        self.assertEquals(data['id'], serialized['data']['id'])
        self.assertEquals(s.type, serialized['data']['type'])
        self.assertTrue(serialized['data']['attributes'])
        self.assertEquals(data['question'], serialized['data']['attributes']['question'])

        def get_bad_attr(data):
            return data['data']['attributes']['not_a_attribute']

        self.assertRaises(KeyError, get_bad_attr, serialized)

    def it_should_serialize_lists_of_data(self):
        s = PollSerializer()
        data = [poll(n+1) for n in range(10)]

        serialized = s.serialize(data)

        self.assertEquals(10, len(serialized['data']))

    def it_should_include_meta_at_root(self):
        s = PollSerializer()
            
        meta = {'total': 100}
        serialized = s.serialize({'id': 1}, meta=meta)

        self.assertEquals(meta, serialized['meta'])

        meta = [] # Meta must be a dict
        serialized = s.serialize({'id': 1}, meta=meta)

        self.assertEquals(None, serialized.get('meta', None))

    def it_should_handle_relationships(self):
        s = AnswerSerializer() # BelongsToRelationship

        data = answer(1, 22)
        included = {'poll': poll(22)}

        serialized = s.serialize(data, included)

        self.assertTrue(serialized['data'])
        self.assertEquals(AnswerSerializer.type, serialized['data']['type'])
        self.assertEquals(data[AnswerSerializer.ref], serialized['data'][AnswerSerializer.ref])
        self.assertEquals(data['text'], serialized['data']['attributes']['text'])
        self.assertTrue(serialized['data']['relationships'])

        self.assertTrue(serialized['data']['relationships']['poll'])
        self.assertEquals(2, len(serialized['data']['relationships']['poll']))

        self.assertTrue(serialized['included'])
        self.assertEquals(1, len(serialized['included']))

    def it_should_handle_relationships_as_a_string(self):
        s = PollSerializer() # BelongsToRelationship

        data = poll(1)
        included = {'answer': answer(22, 1)}

        serialized = s.serialize(data, included)

        print(serialized)
        self.assertEquals(PollSerializer.type, serialized['data']['type'])
        self.assertEquals(data['question'], serialized['data']['attributes']['question'])
        self.assertEquals(data['multiple_choice'], serialized['data']['attributes']['multiple_choice'])
        self.assertEquals(data['multiple_votes'], serialized['data']['attributes']['multiple_votes'])

        self.assertTrue(serialized['data']['relationships']['answer'])
        self.assertTrue(serialized['included'])
        self.assertEquals(1, len(serialized['included']))

    def it_should_allow_different_refs(self):
        s = UuidRefSerializer() 

        data = {'uuid': 'aZeA'}

        parsed = s.serialize(data)

        self.assertTrue(parsed['data']['uuid'])
        self.assertEquals(data['uuid'], parsed['data']['uuid'])


