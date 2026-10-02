---
title: Describe the shape you want
requires: [verify:data-returned]
---

# Describe the shape you want

The fix is to tell the agent what shape its answer must take. The
shape is described with a JSON Schema, a standard way of saying what
a piece of data must look like: which fields it has, what type each
is, and which are required. In Python a schema is written as a
dictionary.

The one in the cell asks for an object with one field, `days`, which
is a list. Each entry in the list has a `day`, an `opens` and a
`closes`. The `description` on a field is read by the model, so it is
the place to say what you mean: here, that times are in 24 hour form,
and that a day the shop is shut has no times at all.

The `output_format` option takes the schema. Nothing else about the
run changes: the same question, the same tool, the same file.

```{cell-insert}
:id: insert-structured
:path: {{ notebook }}
:tags: [structured]
:run: true
schema = {
    "type": "object",
    "properties": {
        "days": {
            "type": "array",
            "description": "One entry for each day of the week, Monday to Sunday",
            "items": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "enum": [
                            "Monday", "Tuesday", "Wednesday", "Thursday",
                            "Friday", "Saturday", "Sunday",
                        ],
                    },
                    "opens": {
                        "type": ["string", "null"],
                        "description": "Opening time, 24 hour HH:MM, or null when closed all day",
                    },
                    "closes": {
                        "type": ["string", "null"],
                        "description": "Closing time, 24 hour HH:MM, or null when closed all day",
                    },
                },
                "required": ["day", "opens", "closes"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["days"],
    "additionalProperties": False,
}

data_options = replace(options, output_format={"type": "json_schema", "schema": schema})

tool_calls = []

async for message in query(prompt=question, options=data_options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                tool_calls.append(block.name)
    elif isinstance(message, ResultMessage):
        structured = message

hours = structured.structured_output

print("type:", type(hours).__name__)

for entry in hours["days"]:
    print(entry)
```

`structured_output` is no longer empty. It is a Python dictionary, in
the shape the schema described: a list under `days`, and in it an
entry for every day, each with the three fields by the names you
chose. The times are in the form you asked for, and the day the shop
is shut has `None` for both.

Compare that with the file. The document gives Tuesday to Friday as
one row. The data has a separate entry for each of the four days,
because the schema asked for one entry a day. The agent did not copy
the file. It read it, understood it, and rewrote it to fit.

```{verify}
:id: data-returned
:label: The result carries data in the shape of the schema
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed structured
if not isinstance(hours, dict):
    print("structured_output is not a dictionary. The run ended with", structured.subtype, "- run the cell again.")
closing = {entry["day"]: entry["closes"] for entry in hours["days"]}
if closing.get("Saturday") != "16:40":
    print("Saturday's closing time is", closing.get("Saturday"), "and the file says 4:40pm. Run the cell again.")
isinstance(hours, dict) and len(closing) == 7 and closing.get("Saturday") == "16:40"
```
