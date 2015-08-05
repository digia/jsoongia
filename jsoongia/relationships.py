

class SerializerRelationship(object):
    def __init__(self, reference):
        self.reference = reference

    def parse(self, reference_value, data):
       pass


class BelongsTo(SerializerRelationship):
    def __init__(self, reference=None):
        super().__init__(reference)

    def _build_reference(self, schema):
        return '_'.join([schema.type.replace('.', '_'), schema.ref])

    def parse(self, schema, data, included):
        if self.reference is None:
            self.reference = self._build_reference(schema)

        reference_value = data[self.reference]

        if not isinstance(included, list):
            included = [included]

        for potential_relationship in included:
            if reference_value == potential_relationship[schema.ref]:
                ref_label = schema.ref
                return {
                    'type': schema.type,
                    ref_label: potential_relationship[ref_label]
                }


class HasMany(SerializerRelationship):
    def parse(self, schema, data, included):
        parsed = []
        reference_value = data[schema.ref]

        if not isinstance(included, list):
            included = [included]

        for potential_relationship in included:
            if reference_value == potential_relationship[self.reference]:
                ref_label = schema.ref
                parsed.append({
                    'type': schema.type, 
                    ref_label: potential_relationship[ref_label]
                })

        if 1 == len(parsed):
            return {'data': parsed.pop()}

        return {'data': parsed}


