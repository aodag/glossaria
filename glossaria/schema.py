import colander as c


class GlossaryNewSchema(c.Schema):
    name = c.SchemaNode(c.String())
    description = c.SchemaNode(c.String())


class GlossaryEditSchema(c.Schema):
    description = c.SchemaNode(c.String())
