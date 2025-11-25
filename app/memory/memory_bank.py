import json
import os
from typing import Dict, Any

class MemoryBank:
    def __init__(self, db_path: str = "memory_bank.json"):
        self.db_path = db_path
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                self.memory = json.load(f)
            # Ensure conversation_history exists (migration)
            if "conversation_history" not in self.memory:
                self.memory["conversation_history"] = []
        else:
            self.memory = {
                "user_profile": {},
                "study_sessions": [],
                "weak_areas": [],
                "conversation_history": []
            }

    def _save_memory(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def get_context(self) -> str:
        """
        Retrieve relevant context for the current session.
        """
        # 1. Recent Topics
        recent_sessions = self.memory["study_sessions"][-3:]
        topics = [s.get("topic", "Unknown") for s in recent_sessions]
        topic_context = f"User recently studied: {', '.join(topics)}." if topics else "No previous study history."
        
        # 2. Recent Conversation History (Last 3 turns)
        history = self.memory.get("conversation_history", [])[-3:]
        history_str = ""
        if history:
            history_str = "\nRecent Conversation:\n"
            for turn in history:
                history_str += f"User: {turn['user']}\nAgent: {turn['agent']}\n"
        
        return f"{topic_context}\n{history_str}"

    def add_session(self, topic: str, notes: str):
        self.memory["study_sessions"].append({
            "topic": topic,
            "notes": notes,
            "timestamp": "TODO: Add timestamp"
        })
        self._save_memory()

    def add_turn(self, user_input: str, agent_output: str):
        self.memory["conversation_history"].append({
            "user": user_input,
            "agent": agent_output
        })
        # Keep only last 10 turns to prevent bloat
        if len(self.memory["conversation_history"]) > 10:
            self.memory["conversation_history"] = self.memory["conversation_history"][-10:]
        self._save_memory()
