import inspect
import importlib


class Serializer(object):
    """Serialize data into JSON API serialization
    
    Schema example:
        'type': 'user',
        'ref': 'id',
        'attributes': []
        'relationships': {}

    """
    type = ''
    ref = 'id'
    attributes = []
    relationships = {}

    def serialize(self, data, included={}, meta={}):
        root = {}

        if included: 
            root['included'] = self._serialize_included(self.relationships, included)

        if meta and isinstance(meta, dict): root['meta'] = meta

        if isinstance(data, list):
            root['data'] = [self._serialize_data(self, d, included) for d in data]
        else:
            root['data'] = self._serialize_data(self, data, included)

        return root

    def _serialize_data(self, schema, data, included):
        ref = schema.ref
        serialized = {}
        attributes = {}

        serialized['type'] = schema.type
        serialized[ref] = data[ref]

        for attr in schema.attributes:
            try:
                attributes[attr] = data[attr]
            except KeyError:
                continue 

        serialized['attributes'] = attributes

        relationships = self._serialize_data_relationships(
            schema,
            data,
            included
        )

        if relationships: serialized['relationships'] = relationships

        return serialized

    def _serialize_data_relationships(self, schema, data, included):
        relationships = {}

        for relation, attributes in schema.relationships.items():
            if relation not in included: continue

            relation_data = included[relation]
            parser = attributes['relationship']
            serializer = self._get_serializer(attributes['serializer'])
            relationships[relation] = parser.parse(serializer, data, relation_data)

        return relationships

    def _serialize_included(self, relationships, included):
        data = []

        for include, attributes in included.items():
            if include in relationships:
                serializer = self._get_serializer(relationships[include]['serializer'])()
                serialized = serializer.serialize(attributes)['data']

                if isinstance(serialized, list):
                    data = data + serialized
                if isinstance(serialized, dict):
                    data.append(serialized)

        return self._remove_included_duplicates(data)

    def _get_serializer(self, serializer):
        if isinstance(serializer, str):
            segments = serializer.split('.')
            cls = segments.pop()
            module = importlib.import_module('.'.join(segments))
            serializer = getattr(module, cls)
        
        return serializer

    def _remove_included_duplicates(self, included):
        unique = []
        seen = []
        for include in included:
            compare = {'type': include['type'], 'id': include['id']}
            if not compare in seen:
                unique.append(include)
                seen.append(compare)

        return unique


