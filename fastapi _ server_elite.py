from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from council_integration import CouncilWithRepos
import asyncio

app = FastAPI()
council = CouncilWithRepos()

class QueryRequest(BaseModel):
    question: str

class SearchRequest(BaseModel):
    pattern: str

@app.post("/decide")
async def decide(request: QueryRequest):
    result = await council.decide_with_context(request.question)
    return {
        "decision": result.decision,
        "consensus": result.consensus_percentage,
        "repos_analyzed": council.repo_elite.total_repos,
        "files_analyzed": council.repo_elite.total_files,
        "synthesis": result.synthesis
    }

@app.post("/search")
async def search(request: SearchRequest):
    results = council.search_codebase(request.pattern)
    return {
        "pattern": request.pattern,
        "matches": len(results),
        "results": results[:50]  # Top 50
    }

@app.get("/summary")
async def summary():
    return council.repo_elite.get_repo_summary()

@app.get("/stats")
async def stats():
    return {
        "repositories": council.repo_elite.total_repos,
        "files": council.repo_elite.total_files,
        "functions": council.repo_elite.total_functions,
        "classes": council.repo_elite.total_classes
    }
