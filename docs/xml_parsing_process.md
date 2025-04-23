# Tacview XML Parsing Process

This document explains how Tacview XML files are parsed and stored in the database in the tacview2db project.

## Overall Process

The XML parsing process follows these steps:

1. A Tacview file is loaded and parsed using the `Tacview` class
2. Mission data is extracted and stored in the database
3. Each event in the file is processed sequentially
4. For each event:
   - Event data is extracted and stored
   - Primary object data is extracted and linked to the event
   - Secondary object data (if present) is extracted and linked
   - Parent object data (if present) is extracted and linked

## Component Breakdown

### Tacview Class

The `Tacview` class is responsible for initial parsing of the XML file. It:
- Opens and parses the Tacview XML file
- Extracts mission-level metadata
- Extracts all event data
- Makes this data available to other components

### Mission Object

The `Mission` object:
- Receives mission data from the Tacview parser
- Checks if this mission already exists in the database
- Creates a new mission record if needed
- Returns a mission ID for linking to events

### Event Processing

For each event in the XML:

1. **Event Object**:
   - Extracts event details (timestamp, type, etc.)
   - Writes event to database with link to mission ID
   - Returns event ID for linking to objects

2. **Primary Object**:
   - Every event must have a primary object
   - Extracts details about the primary actor/object
   - Links to the event via foreign key
   - Example: aircraft, ground unit, or player that initiated the event

3. **Secondary Object** (if present):
   - Represents what the action was performed on
   - Only exists for certain event types
   - Links to the event via foreign key
   - Example: target of an attack, object being damaged

4. **Parent Object** (if present):
   - Only exists when a secondary object is present
   - Represents who performed the action
   - Links to both the event and secondary object
   - Example: the player or AI that caused damage to the secondary object

## Data Flow Diagram

```
XML File → Tacview Parser
    ↓
Mission → Database (missions table)
    ↓
Events → Database (events table)
    ↓
    ├→ Primary Object → Database (primary_objects table)
    ↓
    ├→ Secondary Object → Database (secondary_objects table)
    ↓
    └→ Parent Object → Database (parent_objects table)
```

## Code Example

The core processing logic for events looks like this:

```python
# Process all events in the parsed XML data
for event in event_data:
    # Create and store event
    event_obj = Event(event)
    event_obj.write_to_db(db, mission_obj.id)
    
    # Every event has a primary object
    primary_obj = Primary(event)
    primary_obj.write_to_db(db, event_obj.id)
    
    # Secondary objects may exist
    if Secondary.xml_object_exists(event):
        secondary_obj = Secondary(event)
        secondary_obj.write_to_db(db, event_obj.id)
        
        # Parent objects can only exist if secondary object exists
        if Parent.xml_object_exists(event):
            parent_obj = Parent(event)
            parent_obj.write_to_db(db, event_obj.id, secondary_obj.id)
```

## Database Relationships

- **Mission** - Top level entity containing mission metadata
- **Event** - Linked to mission via mission_id
- **Primary** - Linked to event via event_id
- **Secondary** - Linked to event via event_id
- **Parent** - Linked to event via event_id and secondary via secondary_id

This structure allows for complex querying of events, their actors, and targets across multiple missions while maintaining relational integrity.

## Object Hierarchy Example

For a "damage" event, the hierarchy might look like:

- **Mission**: Operation Overlord
- **Event**: Damage event at timestamp 3600
- **Primary**: F-16C aircraft (what was damaged)
- **Secondary**: SAM site (what caused the damage)
- **Parent**: Enemy AI (who operated the SAM)

This structure allows complete tracking of who did what to whom throughout a mission.
