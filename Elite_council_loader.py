import os
import json
import ast
import subprocess
from pathlib import Path
from typing import Dict, List, Any
import hashlib

class EliteCouncilLoader:
    def __init__(self, repo_base: str = "./repos"):
        self.repo_base = Path(repo_base)
        self.repo_base.mkdir(exist_ok=True)
        self.repo_index = {}
        
    def load_all_repos(self):
        """Load ALL 62 repos into memory with full code analysis"""
        repos = self._get_all_repo_paths()
        
        for repo_path in repos:
            repo_name = repo_path.name
            print(f"Loading: {repo_name}")
            
            self.repo_index[repo_name] = {
                "path": str(repo_path),
                "files": self._extract_files(repo_path),
                "functions": self._extract_functions(repo_path),
                "classes": self._extract_classes(repo_path),
                "imports": self._extract_imports(repo_path),
                "dependencies": self._extract_dependencies(repo_path),
                "readme": self._get_readme(repo_path),
                "hash": self._hash_repo(repo_path)
            }
        
        return self.repo_index
    
    def _get_all_repo_paths(self):
        """Get all 62 repos"""
        # If repos not cloned, clone them
        if not any(self.repo_base.iterdir()):
            self._clone_all()
        return [p for p in self.repo_base.iterdir() if p.is_dir()]
    
    def _clone_all(self):
        """Clone all 62 repos from EAOUITTDOS"""
        result = subprocess.run(
            ["gh", "repo", "list", "EAOUITTDOS", "--limit", "100", "--json", "name", "-q", ".[].name"],
            capture_output=True,
            text=True
        )
        repos = [r for r in result.stdout.strip().split('\n') if r]
        
        for repo in repos:
            target = self.repo_base / repo
            if not target.exists():
                subprocess.run(
                    ["gh", "repo", "clone", f"EAOUITTDOS/{repo}", str(target)],
                    check=False
                )
    
    def _extract_files(self, repo_path: Path) -> Dict[str, str]:
        """Extract ALL code files content"""
        files = {}
        extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.c', '.cpp', '.h', '.hpp', '.java', '.rb', '.php', '.cs', '.swift', '.kt', '.scala', '.lua', '.r', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd', '.vbs', '.pl', '.pm', '.t', '.pod', '.sql', '.sqlite', '.db', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.xml', '.html', '.css', '.scss', '.sass', '.less', '.vue', '.svelte', '.elm', '.clj', '.cljs', '.cljc', '.edn', '.ex', '.exs', '.erl', '.hrl', '.lfe', '.fs', '.fsi', '.fsx', '.ml', '.mli', '.mly', '.mll', '.v', '.sv', '.svh', '.vhd', '.vhdl', '.verilog', '.systemverilog', '.purs', '.hs', '.lhs', '.idr', '.agda', '.coq', '.lean', '.isabelle', '.thy', '.smt2', '.smt', '.z3', '.dafny', '.boogie', '.why', '.tla', '.q', '.k', '.maude', '.cvc4', '.cvc5', '.opensmt', '.yices', '.z3str3', '.nq', '.nt', '.rq', '.sparql', '.ttl', '.owl', '.rdf', '.xmlns', '.xsd', '.wsdl', '.soap', '.wadl', '.raml', '.oas', '.openapi', '.swagger', '.proto', '.thrift', '.avro', '.capnp', '.flatbuffers', '.fbs', '.bond', '.messagepack', '.bson', '.cbor', '.jsonl', '.ndjson', '.geojson', '.topojson', '.kml', '.gpx', '.osm', '.pbf', '.mbtiles', '.gpkg', '.shp', '.shx', '.dbf', '.prj', '.cpg', '.qgs', '.qgz', '.qml', '.sld', '.style', '.mapcss', '.mss', '.mml', '.cartocss', '.less', '.stylus', '.pug', '.jade', '.haml', '.slim', '.ejs', '.njk', '.j2', '.jinja', '.twig', '.mustache', '.handlebars', '.hbs', '.dust', '.swig', '.eco', '.ect', '.jst', '.tmpl', '.tpl', '.liquid', '.erb', '.rhtml', '.rxml', '.builder', '.rake', '.thor', '.cap', '.ru', '.gemspec', '.podspec', '.pom', '.gradle', '.sbt', '.scala', '.build', '.bazel', '.bzl', '.nix', '.guix', '.manifest', '.spec', '.rpm', '.deb', '.ebuild', '.recipe', '.conanfile', '.cmake', '.makefile', '.mk', '.d', '.dd', '.rules', '.targets', '.props', '.vcxproj', '.sln', '.csproj', '.fsproj', '.vbproj', '.shproj', '.wixproj', '.nuspec', '.psd1', '.psm1', '.ps1xml', '.clixml', '.xaml', '.xul', '.xbl', '.xpt', '.idl', '.odl', '.tlb', '.rc', '.resx', '.resources', '.settings', '.config', '.dll.config', '.exe.config', '.application', '.manifest', '.deploy', '.vsto', '.dna', '.dna.config', '.template', '.tt', '.ttinclude', '.t4', '.edmx', '.edml', '.dbml', '.linq', '.disco', '.wsdl', '.vsdisco', '.svc', '.asmx', '.ashx', '.axd', '.rem', '.soap', '.aspx', '.ascx', '.master', '.skin', '.browser', '.webpart', '.dwp', '.wsp', '.stp', '.pnp', '.ps1', '.psm1', '.psd1', '.ps1xml', '.pssc', '.cdxml', '.mof', '.sdkman', '.tool-versions', '.asdf', '.env', '.envrc', '.nixpkgs', '.guix', '.spack', '.easybuild', '.module', '.load', '.pbs', '.slurm', '.condor', '.lsf', '.qsub', '.sbatch', '.job', '.sh', '.bash', '.zsh', '.fish', '.profile', '.bashrc', '.zshrc', '.fishrc', '.aliases', '.functions', '.env', '.venv', '.virtualenv', '.pyenv', '.rbenv', '.nvm', '.nodenv', '.goenv', '.plenv', '.phpenv', '.javaenv', '.luaenv', '.perlbrew', '.plenv', '.pyenv', '.virtualenv', '.rbenv', '.nvm', '.nodenv', '.goenv', '.plenv', '.phpenv', '.javaenv', '.luaenv', '.perlbrew'}
        
        for ext in extensions:
            for file_path in repo_path.rglob(f"*{ext}"):
                if file_path.is_file():
                    try:
                        relative_path = str(file_path.relative_to(repo_path))
                        # Skip binary files and large files
                        if file_path.stat().st_size < 1024 * 1024:  # < 1MB
                            content = file_path.read_text(encoding='utf-8', errors='ignore')
                            files[relative_path] = content
                    except:
                        pass
        return files
    
    def _extract_functions(self, repo_path: Path) -> Dict[str, List[str]]:
        """Extract all function definitions"""
        functions = {}
        for py_file in repo_path.rglob("*.py"):
            if py_file.is_file():
                try:
                    tree = ast.parse(py_file.read_text(encoding='utf-8', errors='ignore'))
                    funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                    if funcs:
                        functions[str(py_file.relative_to(repo_path))] = funcs
                except:
                    pass
        return functions
    
    def _extract_classes(self, repo_path: Path) -> Dict[str, List[str]]:
        """Extract all class definitions"""
        classes = {}
        for py_file in repo_path.rglob("*.py"):
            if py_file.is_file():
                try:
                    tree = ast.parse(py_file.read_text(encoding='utf-8', errors='ignore'))
                    cls = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                    if cls:
                        classes[str(py_file.relative_to(repo_path))] = cls
                except:
                    pass
        return classes
    
    def _extract_imports(self, repo_path: Path) -> Dict[str, List[str]]:
        """Extract all imports"""
        imports = {}
        for py_file in repo_path.rglob("*.py"):
            if py_file.is_file():
                try:
                    tree = ast.parse(py_file.read_text(encoding='utf-8', errors='ignore'))
                    imp = []
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            imp.extend([n.name for n in node.names])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                imp.append(node.module)
                    if imp:
                        imports[str(py_file.relative_to(repo_path))] = imp
                except:
                    pass
        return imports
    
    def _extract_dependencies(self, repo_path: Path) -> Dict[str, str]:
        """Extract dependencies from common files"""
        deps = {}
        # Check requirements.txt
        req_file = repo_path / "requirements.txt"
        if req_file.exists():
            deps["requirements.txt"] = req_file.read_text()
        
        # Check package.json
        pkg_file = repo_path / "package.json"
        if pkg_file.exists():
            try:
                deps["package.json"] = json.loads(pkg_file.read_text())
            except:
                pass
        
        # Check go.mod
        go_file = repo_path / "go.mod"
        if go_file.exists():
            deps["go.mod"] = go_file.read_text()
        
        # Check Cargo.toml
        cargo_file = repo_path / "Cargo.toml"
        if cargo_file.exists():
            deps["Cargo.toml"] = cargo_file.read_text()
        
        return deps
    
    def _get_readme(self, repo_path: Path) -> str:
        """Get README content"""
        for readme in repo_path.glob("README*"):
            if readme.is_file():
                try:
                    return readme.read_text(encoding='utf-8', errors='ignore')[:5000]
                except:
                    pass
        return ""
    
    def _hash_repo(self, repo_path: Path) -> str:
        """Generate hash of repo for change detection"""
        hasher = hashlib.sha256()
        for file_path in sorted(repo_path.rglob("*")):
            if file_path.is_file():
                try:
                    hasher.update(file_path.read_bytes()[:1024])  # Sample for speed
                except:
                    pass
        return hasher.hexdigest()[:16]

class EliteCouncil:
    def __init__(self):
        self.loader = EliteCouncilLoader()
        self.repo_index = self.loader.load_all_repos()
        self.total_repos = len(self.repo_index)
        self.total_files = sum(len(repo["files"]) for repo in self.repo_index.values())
        self.total_functions = sum(sum(len(funcs) for funcs in repo["functions"].values()) for repo in self.repo_index.values())
        self.total_classes = sum(sum(len(cls) for cls in repo["classes"].values()) for repo in self.repo_index.values())
        
        print(f"Loaded {self.total_repos} repositories")
        print(f"Total files: {self.total_files}")
        print(f"Total functions: {self.total_functions}")
        print(f"Total classes: {self.total_classes}")
    
    def get_code_context(self, query: str) -> str:
        """Build context from relevant repos based on query"""
        context = []
        for repo_name, repo_data in self.repo_index.items():
            # Check if repo matches query
            if any(word.lower() in repo_name.lower() or word.lower() in repo_data["readme"].lower() for word in query.split()):
                context.append(f"\n=== REPOSITORY: {repo_name} ===\n")
                context.append(f"README: {repo_data['readme'][:1000]}\n")
                
                # Add top files
                files = list(repo_data["files"].keys())[:20]
                for file in files:
                    context.append(f"File: {file}")
                    content = repo_data["files"][file][:500]  # Truncate for token limit
                    context.append(content[:200] + "...\n")
                
                # Add functions
                for file, funcs in list(repo_data["functions"].items())[:5]:
                    context.append(f"Functions in {file}: {', '.join(funcs[:10])}")
                
                # Add classes
                for file, cls in list(repo_data["classes"].items())[:5]:
                    context.append(f"Classes in {file}: {', '.join(cls[:10])}")
        
        return "\n".join(context) if context else "No matching repos found."
    
    def search_all_code(self, pattern: str) -> List[Dict[str, Any]]:
        """Search for pattern across all 62 repos"""
        results = []
        for repo_name, repo_data in self.repo_index.items():
            for file_path, content in repo_data["files"].items():
                if pattern.lower() in content.lower():
                    results.append({
                        "repo": repo_name,
                        "file": file_path,
                        "snippet": content[:200]
                    })
        return results
    
    def get_repo_summary(self) -> Dict[str, Any]:
        """Get full summary of all repos"""
        return {
            "total_repos": self.total_repos,
            "total_files": self.total_files,
            "total_functions": self.total_functions,
            "total_classes": self.total_classes,
            "repos": [
                {
                    "name": name,
                    "files": len(data["files"]),
                    "functions": sum(len(f) for f in data["functions"].values()),
                    "classes": sum(len(c) for c in data["classes"].values()),
                    "has_readme": bool(data["readme"]),
                    "dependencies": list(data["dependencies"].keys())
                }
                for name, data in self.repo_index.items()
            ]
        }
