from elite_council_loader import EliteCouncil
from council_orchestrator import CouncilOrchestrator
import asyncio

class CouncilWithRepos:
    def __init__(self):
        self.council = CouncilOrchestrator("config.yaml")
        self.repo_elite = EliteCouncil()
    
    async def decide_with_context(self, question: str):
        # Get relevant code context from all 62 repos
        context = self.repo_elite.get_code_context(question)
        
        # Inject context into council prompt
        prompt = f"""
CODEBASE CONTEXT (from ALL {self.repo_elite.total_repos} repositories):
{context}

QUESTION: {question}

Provide decision based on analysis of this entire codebase."""
        
        # Run council with enhanced prompt
        # Modify orchestrator to accept custom prompt
        return await self.council.process_with_prompt(prompt)
    
    def search_codebase(self, query: str):
        """Search all 62 repos instantly"""
        return self.repo_elite.search_all_code(query)
    
    def get_full_index(self):
        """Get complete index of all code"""
        return self.repo_elite.repo_index
