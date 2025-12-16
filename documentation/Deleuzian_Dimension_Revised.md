# Deleuzian Dimension - Revised Schema

Based on Deleuze & Guattari's "What is Philosophy?" (1991) - their actual theory of concepts.

## Key Insight

Philosophy is "the art of forming, inventing, and fabricating concepts." Concepts are not representations but CREATIONS. They:
- Have no identity, only becoming
- Are self-referential (posit themselves and their objects simultaneously)
- Are "real without being actual, ideal without being abstract"

## Core Elements of a Concept

### 1. COMPONENTS
Every concept is a multiplicity of inseparable components.
- Example: Descartes' cogito = {doubting, thinking, being}
- Components are heterogeneous but held together
- The concept is "fragmentary" yet "whole"

### 2. ZONES OF INDISCERNIBILITY
Where components overlap, something passes between them.
- Example: In cogito, doubting-thinking zone: "the doubter cannot doubt their own thought"
- These are loci of becoming within the concept
- Enable internal dynamism

### 3. ENDOCONSISTENCY
Internal coherence - how components hold together.
- What makes the concept unified despite being fragmentary
- The "point of absolute survey" that traverses all components

### 4. EXOCONSISTENCY (Neighborhood)
External relations - how concept relates to other concepts.
- Concepts form "neighborhoods" with other concepts
- "Bridges" connect concepts across planes
- Order of neighborhood determines concept's position in philosophical space

### 5. PLANE OF IMMANENCE
The pre-philosophical "ground" on which concepts are created.
- Determines what counts as a legitimate problem
- Different philosophies have different planes
- "The absolute ground of philosophy, its earth"
- Contains unthought/unquestioned assumptions

### 6. CONCEPTUAL PERSONA
The "subject" that activates thinking with this concept.
- Not the philosopher as person but a philosophical character
- Example: Socrates (for Plato), the Idiot (for Descartes), Dionysus (for Nietzsche)
- "Powers of concepts" that operate on the plane

### 7. PROBLEM ADDRESSED
Concepts are created to address problems.
- Every event is a critical point in a problem
- The problem is transformed by events it engenders
- Concepts are "the contour, configuration, constellation of an event to come"

---

## Revised Database Schema

### Table: concept_components
Individual components that make up the concept.

| Field | Type | Description |
|-------|------|-------------|
| id | SERIAL | Primary key |
| concept_id | INTEGER FK | Parent concept |
| component_name | VARCHAR(100) | Name of component (e.g., "doubting") |
| component_description | TEXT | What this component contributes |
| is_intensive | BOOLEAN | Is this an intensive variation? |
| order_index | INTEGER | Position in concept's structure |
| confidence | FLOAT | Confidence this is a true component |
| created_at | TIMESTAMPTZ | |

### Table: concept_zones_of_indiscernibility
Where components overlap - zones of becoming.

| Field | Type | Description |
|-------|------|-------------|
| id | SERIAL | Primary key |
| concept_id | INTEGER FK | Parent concept |
| component_a_id | INTEGER FK | First component |
| component_b_id | INTEGER FK | Second component |
| zone_description | TEXT | What passes between them in this zone |
| what_becomes_possible | TEXT | What this zone enables |
| confidence | FLOAT | |
| created_at | TIMESTAMPTZ | |

### Table: concept_consistency
Endoconsistency and exoconsistency analysis.

| Field | Type | Description |
|-------|------|-------------|
| id | SERIAL | Primary key |
| concept_id | INTEGER FK | Parent concept (1:1) |
| endoconsistency_description | TEXT | How components hold together internally |
| survey_point | TEXT | The "point of absolute survey" that unifies |
| consistency_strength | VARCHAR(20) | strong/moderate/weak/unstable |
| created_at | TIMESTAMPTZ | |

### Table: concept_neighborhood (exoconsistency)
Relations to other concepts - the concept's neighborhood.

| Field | Type | Description |
|-------|------|-------------|
| id | SERIAL | Primary key |
| concept_id | INTEGER FK | Parent concept |
| neighbor_concept_id | INTEGER FK | Related concept |
| relation_type | VARCHAR(30) | bridge/resonance/interference/repulsion |
| relation_description | TEXT | Nature of the connection |
| neighborhood_order | INTEGER | How close in neighborhood (1=closest) |
| bridges_across_plane | BOOLEAN | Does this bridge different planes? |
| confidence | FLOAT | |
| created_at | TIMESTAMPTZ | |

### Table: concept_plane_of_immanence
The plane on which concept operates.

| Field | Type | Description |
|-------|------|-------------|
| id | SERIAL | Primary key |
| concept_id | INTEGER FK | Parent concept |
| plane_name | VARCHAR(100) | Name/description of the plane |
| what_plane_presupposes | TEXT | Unthought assumptions of this plane |
| legitimate_problems | TEXT | What counts as a problem on this plane |
| excluded_problems | TEXT | What can't be asked on this plane |
| historical_emergence | VARCHAR(100) | When this plane emerged |
| confidence | FLOAT | |
| created_at | TIMESTAMPTZ | |

### Table: concept_personae
Conceptual personae that activate this concept.

| Field | Type | Description |
|-------|------|-------------|
| id | SERIAL | Primary key |
| concept_id | INTEGER FK | Parent concept |
| persona_name | VARCHAR(100) | Name of persona (e.g., "the sovereign", "the entrepreneur") |
| persona_description | TEXT | What this persona does/thinks |
| what_persona_enables | TEXT | What thinking it enables |
| historical_origin | TEXT | Where this persona comes from |
| confidence | FLOAT | |
| created_at | TIMESTAMPTZ | |

### Table: concept_problems (revised)
Problems the concept was created to address.

| Field | Type | Description |
|-------|------|-------------|
| id | SERIAL | Primary key |
| concept_id | INTEGER FK | Parent concept |
| problem_statement | TEXT | The problem/tension being addressed |
| problem_type | VARCHAR(30) | political/epistemological/ontological/practical |
| what_event_triggered | TEXT | What event made this problem pressing |
| how_concept_responds | TEXT | How the concept addresses this problem |
| problem_transformed_to | TEXT | How problem changes through concept's use |
| confidence | FLOAT | |
| created_at | TIMESTAMPTZ | |

---

## Example: "Technological Sovereignty"

### Components
1. **Sovereignty** - supreme authority, non-interference
2. **Technology** - productive capacity, innovation systems
3. **State** - political entity exercising control
4. **Territory** - bounded space of jurisdiction

### Zones of Indiscernibility
- **Sovereignty-Technology zone**: "Can control be exercised over networked systems the way it is over territory?"
- **State-Technology zone**: "Is the state the appropriate actor for technology governance?"

### Consistency
- **Endoconsistency**: Weak - components don't cohere well (territory logic ≠ network logic)
- **Survey point**: The "national interest" supposedly unifies, but this is strained

### Neighborhood
- **Bridges to**: Economic sovereignty, data sovereignty, digital sovereignty
- **Interference with**: Globalization, interdependence, network theory
- **Neighborhood order**: Close to "sovereignty" (1), distant from "network" (3)

### Plane of Immanence
- **Plane**: Westphalian state system / geopolitical realism
- **Presupposes**: States are primary actors, territory is controllable, autonomy is possible
- **Legitimate problems**: "How to defend national interests"
- **Excluded problems**: "Is state sovereignty coherent in a networked world?"

### Conceptual Persona
- **The Sovereign**: Decision-maker who can declare exception, defend national interest
- **The Strategic Planner**: Rational actor calculating national advantage

### Problem Addressed
- **Problem**: How to mobilize resources for tech independence while remaining embedded in global systems
- **Event that triggered**: US-China tech tensions (2018-), Snowden (2013)
- **How concept responds**: By extending familiar sovereignty logic to new domain
- **Problem transformed**: From "how to achieve autonomy" to "how to claim autonomy while managing dependency"

---

## What We Removed (from A Thousand Plateaus, not concept theory)

The following were from Deleuze's OTHER work on desire/social machines, not his theory of concepts:
- ~~Lines of flight~~ (rhizomatics)
- ~~Deterritorialization/reterritorialization~~ (territorial analysis)
- ~~Becomings~~ (desire theory) - though "zones of indiscernibility" ARE loci of becoming within concepts
- ~~Body without organs~~ (desiring-machines)

These could be applied to analyze concepts, but they're not Deleuze's theory OF concepts.
