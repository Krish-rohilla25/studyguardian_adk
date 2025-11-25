import logging
from datetime import datetime
from termcolor import colored

class AgentLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentLogger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.logger = logging.getLogger("StudyGuardian")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler("study_guardian.log")
        fh.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        self.logger.addHandler(fh)

    def log(self, agent_name: str, message: str):
        """
        Log an event from an agent.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{agent_name}] {message}"
        self.logger.info(log_msg)
        # Optional: Print to console for debug (can be toggled)
        # print(colored(f"[{timestamp}] {log_msg}", "grey"))

    def error(self, agent_name: str, message: str):
        """
        Log an error.
        """
        self.logger.error(f"[{agent_name}] ERROR: {message}")
