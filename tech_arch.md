# Technical Architecture for Pyzelda RPG Expansion

## Data Structures
- **Quests**: Stored as JSON in `data/quests/quests.json`. Each quest: dict with id, title, objectives (list of dicts), rewards (dict), prerequisites (list).
- **Story Flags**: Dict in `StoryManager` class, saved in `save_manager.py` as part of save_data.
- **Dialogue Data**: Dict in `dialogues.py`, with NPC ids as keys, containing greeting, choices (list of dicts with text, response, flag).

## New Classes
- **QuestManager** (`quests.py`): Manages quest loading, starting, updating progress.
- **StoryManager** (`story.py`): Handles flags, updates on actions.
- **DialogueSystem** (`dialogues.py`): Manages dialogue flow, UI integration.
- **CutsceneEngine** (`cutscenes.py`): Handles cutscene playback.
- **QuestJournal** (`ui.py`): UI for viewing quests.
- **Boss** (`bosses.py`): Base class for boss encounters with phases.

## Integration Points
- `main.py`: Initialize managers in Game.__init__, update in run loop.
- `level.py`: Load new maps, check flags for unlocks.
- `enemy.py`: Extend for new types, hook deaths to quest updates.
- `save_manager.py`: Add quest and story data to save/load.

## File Structure Additions
- `code/quests.py`
- `code/story.py`
- `code/dialogues.py`
- `code/cutscenes.py`
- `code/bosses.py`
- `code/items.py`
- `data/quests/quests.json`
- `data/dialogues/dialogues.json`