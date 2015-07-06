# JSOONGIA - JSON API
===================
A framework agnostic JSON API serializer.

**Currently a work in progress**
TODO:
[X] Meta
[X] Include/Relationships
[ ] Links
[ ] Refactor tests/Add tests
[ ] Setup for PIP
[ ] Create a 'real' README

### Quick Example
```python

# serializers.py
from jsoongia import Serializer, relationships

class UserSerializer(Serializer):
    ref = 'id'
    type = 'user'
    attributes = ['email', 'fname', 'lname']
    relationships = {
        'comment': {
            'serializer': CommentSerializer,
            'relationship': relationships.BelongsTo('user_id')
        }
    }


# views.py
from .serializers import UserSerializer

def get_something():
    serializer = UserSerializer
    data = {...}
    included = {'comment': ...}

    serialized = serializer.serialize(data, included)

```
