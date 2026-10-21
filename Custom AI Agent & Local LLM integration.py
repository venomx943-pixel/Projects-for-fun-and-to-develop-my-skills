import json
import time
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class AgentStatus(Enum):
    INITIALIZED = "INITIALIZED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ModelRole(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "ASSISTANT"

@dataclass
class MessageContext:
    role: ModelRole
    content: str
    timestamp: float

@dataclass
class AgentTaskResult:
    task_id: str
    status: AgentStatus
    execution_time: float
    output_tokens: int
    response_content: str
    metadata: Dict[str, Any]

class LocalModelEngineInterface:
    def __init__(self, model_name: str = "Llama-3-Local"):
        self._model_name = model_name
        self._is_loaded = True

    def generate_inference(self, system_prompt: str, user_query: str) -> str:
        if not self._is_loaded:
            raise RuntimeError("Model engine not loaded.")
        
        simulated_response = f"Processed inference securely using [{self._model_name}]. Context evaluated for query: '{user_query[:30]}...' Execution successful."
        return simulated_response

class ConversationMemoryManager:
    def __init__(self, max_history_length: int = 10):
        self._max_history = max_history_length
        self._history: List[MessageContext] = []

    def add_message(self, role: ModelRole, content: str):
        if len(self._history) >= self._max_history:
            self._history.pop(0)
        self._history.append(MessageContext(role=role, content=content, timestamp=time.time()))

    def get_formatted_context(self) -> List[Dict[str, str]]:
        return [{"role": msg.role.value.lower(), "content": msg.content} for msg in self._history]

class CustomAIAgentSystem:
    def __init__(self, agent_name: str, system_instructions: str):
        self._agent_id = str(uuid.uuid4())
        self._agent_name = agent_name
        self._system_instructions = system_instructions
        self._engine = LocalModelEngineInterface()
        self._memory = ConversationMemoryManager()
        self._memory.add_message(ModelRole.SYSTEM, system_instructions)

    def execute_task(self, user_input: str) -> AgentTaskResult:
        start_time = time.time()
        try:
            self._memory.add_message(ModelRole.USER, user_input)
            
            raw_response = self._engine.generate_inference(self._system_instructions, user_input)
            
            self._memory.add_message(ModelRole.ASSISTANT, raw_response)
            
            execution_time = round(time.time() - start_time, 4)
            token_count = len(raw_response.split()) * 2

            return AgentTaskResult(
                task_id=str(uuid.uuid4()),
                status=AgentStatus.COMPLETED,
                execution_time=execution_time,
                output_tokens=token_count,
                response_content=raw_response,
                metadata={"agent_id": self._agent_id, "agent_name": self._agent_name}
            )
        except Exception as e:
            execution_time = round(time.time() - start_time, 4)
            return AgentTaskResult(
                task_id=str(uuid.uuid4()),
                status=AgentStatus.FAILED,
                execution_time=execution_time,
                output_tokens=0,
                response_content=str(e),
                metadata={"agent_id": self._agent_id, "error": True}
            )

class AgentExecutionOrchestrator:
    @staticmethod
    def run_demonstration():
        print("=" * 70)
        print("          CUSTOM AI AGENT & LOCAL LLM INTEGRATION ENGINE         ")
        print("=" * 70)
        
        system_prompt = "You are an autonomous engineering assistant built for secure backend data analysis."
        agent = CustomAIAgentSystem(agent_name="Nexus-Core-Agent", system_instructions=system_prompt)
        
        print(f"[+] Initialized Agent ID : {agent._agent_id}")
        print(f"[+] Agent Name           : {agent._agent_name}")
        print("-" * 70)

        sample_queries = [
            "Analyze system resource allocation parameters.",
            "Generate secure JSON output structure for database ingestion.",
            "Verify local environment integrity and token constraints."
        ]

        for idx, query in enumerate(sample_queries, 1):
            print(f"[{idx}] Executing Query: {query}")
            result = agent.execute_task(query)
            print(f"    Status     : {result.status.value}")
            print(f"    Time Taken : {result.execution_time}s | Tokens: {result.output_tokens}")
            print(f"    Response   : {result.response_content}")
            print("-" * 70)

        print("[+] Agent Orchestration Execution Completed Successfully.")

if __name__ == "__main__":
    AgentExecutionOrchestrator.run_demonstration()