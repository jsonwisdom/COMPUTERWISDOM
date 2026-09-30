# ARCHIVESSNAKE JSONMODEL / JM BOUNDARY V0.1

**Status:** HOLD  
**Authority created:** false  
**TAD session obtained:** false  
**TAD identifiers bound to ArchivesSpace URIs:** false  
**Write permission inferred:** false  
**Date recorded:** 2026-09-22

## 1. Core distinction

JSONModel is ArchivesSpace's record language. ArchivesSnake does not invent new record schemas; it wraps JSON returned by ArchivesSpace and offers a lightweight `JM` payload factory.

```text
JSONMODEL_TYPE = ARCHIVESSPACE SCHEMA NAME
ASNAKE_CLASS   = PYTHON WRAPPER
WRAPPER        != NEW SCHEMA
FACTORY_STAMP  != SERVER ACCEPTANCE
```

Persisted records commonly carry:

```json
{"jsonmodel_type": "resource"}
```

Ruby selects schemas with `JSONModel(:resource)`. Python sees the same discriminator in a dictionary and may wrap that dictionary in an ArchivesSnake class.

## 2. ArchivesSnake wrapper surface

| Class | Role |
|---|---|
| `JSONModelObject` | Wraps one record; JSON keys become attributes and unknown attributes may resolve child routes. |
| `JSONModelRelation` | Wraps list/index routes; iterable; calling with an ID fetches one object. |
| `ComponentObject` | Specialized archival-object wrapper with `.tree`. |
| `TreeNode` / `TreeNodeData` | Resource and archival-object tree waypoints/data. |
| `AgentRelation` | Splits `/agents` into people, families, corporate entities, and software. |
| `ResourceRelation` | Resolves resources across repositories. |
| `JM` | Dynamic factory returning a plain dictionary with `jsonmodel_type` stamped. |

Observed dispatch signifiers:

```python
component_signifiers = {"archival_object", "archival_objects"}
jmtype_signifiers = {"ref", "jsonmodel_type"}
searchdoc_signifiers = {"primary_type", "types", "id", "json"}
```

A Solr search document is not itself a JSONModel record. ArchivesSnake parses `doc["json"]` before wrapping.

## 3. `JM` is one metaclass hook

```python
class _JMeta(type):
    def __getattr__(self, key):
        def jsonmodel_wrapper(**kwargs):
            out = {"jsonmodel_type": key}
            out.update(**kwargs)
            return out

        if key.startswith('_'):
            return super().__getattr__(self, key)
        return jsonmodel_wrapper

class JM(metaclass=_JMeta):
    pass
```

Call chain:

```text
JM.resource(title="x")
  -> _JMeta.__getattr__(JM, "resource")
  -> jsonmodel_wrapper(title="x")
  -> {"jsonmodel_type": "resource", "title": "x"}
```

The return value is a plain `dict`, not `JSONModelObject`. `JM` loads no schema, performs no required-field validation, assigns no URI, and creates no fixed catalogue of methods. Underscore-prefixed names are not factories.

```python
JM.banana(peel=True)
# {"jsonmodel_type": "banana", "peel": True}

JM.archival_object()
# type stamp only; required fields absent

JM.Resource(title="x")
# wrong case; ArchivesSpace should reject this unknown type
```

The legal type set is determined by `common/schemas` on the ArchivesSpace server receiving the POST.

## 4. Common top-level record types

Repository-scoped examples:

- `repository`
- `resource`
- `archival_object`
- `accession`
- `digital_object`
- `digital_object_component`
- `event`
- `assessment`
- `classification` / `classification_term`
- `top_container`
- `container_profile`
- `location` / `location_profile`
- administrative records such as groups, users, and required fields

Global examples:

- `agent_person` at `/agents/people/:id`
- `agent_family` at `/agents/families/:id`
- `agent_corporate_entity` at `/agents/corporate_entities/:id`
- `agent_software` at `/agents/software/:id`
- `subject`
- `vocabulary` / `term`
- `user`

Agent kind and name subtype must agree: person/name_person, family/name_family, corporate entity/name_corporate_entity, software/name_software.

## 5. Nested/subrecord examples

Nested records still carry their own `jsonmodel_type` when the server schema calls for it:

- `date`, `extent`
- note families such as `note_text`, `note_multipart`, `note_bioghist`, `note_scopecontent`, `note_odd`, `note_index`, `note_chronology`, `note_definedlist`, and `note_orderedlist`
- `instance`, `sub_container`, `file_version`
- `external_id`, `external_document`, `revision_statement`, `deaccession`
- `rights_statement`, `agent_contact`
- `name_person`, `name_family`, `name_corporate_entity`, `name_software`

Not every nested object is independently type-stamped. Relationship stubs such as linked agents may instead be schema-shaped objects containing role and ref.

Ref pattern:

```json
{"ref": "/repositories/2/resources/102"}
```

When requested through `resolve[]`, ArchivesSpace may attach the expanded object under `_resolved`.

## 6. TAD-shaped candidate mapping

If TAD tracks exist in ArchivesSpace as advertised, a catalogue row would ordinarily be an `archival_object`. Playable media would ordinarily be represented by a `digital_object` (and possibly a `digital_object_component`) whose file bytes live elsewhere, such as DSpace. The link is commonly an `instance`.

```json
{
  "jsonmodel_type": "archival_object",
  "uri": "/repositories/2/archival_objects/117780",
  "title": "...",
  "level": "item",
  "ref_id": "...",
  "publish": true,
  "resource": {"ref": "/repositories/2/resources/..."},
  "parent": {"ref": "/repositories/2/archival_objects/..."},
  "linked_agents": [
    {"role": "creator", "ref": "/agents/people/273"}
  ],
  "instances": [
    {
      "jsonmodel_type": "instance",
      "instance_type": "digital_object",
      "digital_object": {"ref": "/repositories/2/digital_objects/..."}
    }
  ]
}
```

Illustrative agent only:

```json
{
  "jsonmodel_type": "agent_person",
  "uri": "/agents/people/273",
  "names": [
    {
      "jsonmodel_type": "name_person",
      "primary_name": "Maclean",
      "rest_of_name": "Calum Iain"
    }
  ]
}
```

These URIs are not evidence. TAD public identifiers such as track `58474` or person `273` remain front-end keys until a backend response or dump binds them to ArchivesSpace URIs.

## 7. Payload construction examples

```python
from asnake.jsonmodel import JM

resource = JM.resource(
    title="Michelle Crone Papers",
    id_0="apap101",
    level="collection",
    publish=True,
)

ao = JM.archival_object(
    title="The Boddamers hinged the monkey",
    level="item",
    publish=True,
    resource={"ref": "/repositories/2/resources/1"},
    dates=[JM.date(begin="1772", date_type="single", label="creation")],
    linked_agents=[{"role": "creator", "ref": "/agents/people/273"}],
    instances=[
        JM.instance(
            instance_type="digital_object",
            digital_object={"ref": "/repositories/2/digital_objects/9"},
        )
    ],
)

digital_object = JM.digital_object(
    title="Tape extract",
    digital_object_id="TAD-58474",
)
```

These are candidate payloads only. ArchivesSpace validates them when POSTed.

## 8. Read and write boundary

Read raw JSON:

```python
obj = aspace.client.get(
    "/repositories/2/archival_objects/117780"
).json()
assert obj["jsonmodel_type"] == "archival_object"
```

Safely mutate an existing wrapped record:

```python
body = ao.json()  # reified deep copy
body["title"] = body["title"] + "!"
aspace.client.post(body["uri"], json=body)
```

Create a new candidate record:

```python
payload = JM.archival_object(
    title="...",
    level="item",
    resource={"ref": "/repositories/2/resources/1"},
)
client.post("/repositories/2/archival_objects", json=payload)
```

Never POST a Solr document. Parse its embedded JSON record first. Never POST a ref-only stub as though it were a complete record.

## 9. Frozen boundaries

```text
JM.resource()          != VALIDATED_RECORD
jsonmodel_type         != TAD_TRACK_ID
archival_object        != digital_object
digital_object         != DSPACE_BYTES
agent_person           != TAD /person/273 UNTIL BOUND
Solr primary_type      != jsonmodel_type
FACTORY_STAMP          != SERVER_ACCEPT
POST                   != PERMISSION_TO WRITE TAD
```

Using ArchivesSnake against Edinburgh requires the institution's API endpoint, repository identifier, authentication/session, and permission. None is created or inferred here.

## 10. Source pins

- ArchivesSnake repository: `archivesspace-labs/ArchivesSnake`
- Observed default-branch tree: `1df4bb6a2499c894c7f1a3b07746e6805b05c8e5`
- Observed `asnake/jsonmodel/__init__.py` blob: `fe89e6fb5d755c58031f414edd588f7eb5939259`
- ArchivesSpace API reference: <https://archivesspace.github.io/archivesspace/api/>
- ArchivesSpace schema/database architecture: <https://archivesspace.github.io/tech-docs/architecture/backend/database.html>

Source pins establish what was inspected; they do not establish a TAD backend mapping.

```text
STATE     = HOLD
AUTHORITY = FALSE
```
