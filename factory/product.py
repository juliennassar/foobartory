import uuid


class Foo:
    """
    Foo object with unique ID
    """

    def __init__(self):
        self.uuid = uuid.uuid4()


class Bar:
    """
    Bar object with unique ID
    """

    def __init__(self):
        self.uuid = uuid.uuid4()


class FooBar:
    """
    FooBar object with IDs from composing Foo and Bar
    """

    def __init__(self, foo: Foo, bar: Bar):
        self.foo_uuid = foo.uuid
        self.bar = bar.uuid
