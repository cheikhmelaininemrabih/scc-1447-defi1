import os

class RCPSPInstance:
    def __init__(self, filepath):
        self.filepath = filepath
        self.num_jobs = 0
        self.num_resources = 0
        self.durations = {}  # 1-based index (0 is dummy start)
        self.requests = {}   # 1-based index
        self.successors = {} # 1-based index to list
        self.predecessors = {} # 1-based index to list
        self.capacities = []
        
        if filepath:
            self.parse()
        else:
            # Default empty for testing
            pass

    def parse(self):
        try:
            with open(self.filepath, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: File {self.filepath} not found.")
            return

        mode = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 1. Parse number of jobs
            if line.startswith('jobs (incl. supersource/sink ):'):
                parts = line.split(':')
                if len(parts) > 1:
                    self.num_jobs = int(parts[1].strip())
                    # Initialize structures
                    self.durations = {i: 0 for i in range(1, self.num_jobs + 1)}
                    self.requests = {i: [] for i in range(1, self.num_jobs + 1)}
                    self.successors = {i: [] for i in range(1, self.num_jobs + 1)}
                    self.predecessors = {i: [] for i in range(1, self.num_jobs + 1)}
                continue
            
            # 2. Parse number of resources
            # Format usually: "  - renewable                 :  4   R"
            if 'renewable' in line and ':' in line:
                try:
                    parts = line.split(':')
                    val_str = parts[1].strip().split()[0]
                    self.num_resources = int(val_str)
                except:
                    pass
                continue

            # 3. Detect Sections
            if line.startswith('PRECEDENCE RELATIONS:'):
                mode = 'PRECEDENCE'
                continue
            
            if line.startswith('REQUESTS/DURATIONS:'):
                mode = 'REQUESTS'
                continue
            
            if line.startswith('RESOURCEAVAILABILITIES:'):
                mode = 'RESOURCES'
                continue
            
            if line.startswith('*'): # End of section marker sometimes
                if mode == 'RESOURCES' and self.capacities:
                    mode = None
                continue

            # 4. Parse Content based on mode
            if mode == 'PRECEDENCE':
                if line.startswith('jobnr.'): continue
                try:
                    parts = list(map(int, line.split()))
                    if not parts: continue
                    # Format: jobnr. #modes #successors succ1 succ2 ...
                    job_id = parts[0]
                    succs = parts[3:]
                    self.successors[job_id] = succs
                    for s in succs:
                        if s not in self.predecessors: self.predecessors[s] = []
                        self.predecessors[s].append(job_id)
                except ValueError:
                    continue
            
            elif mode == 'REQUESTS':
                if line.startswith('jobnr.') or line.startswith('-----'): continue
                try:
                    parts = list(map(int, line.split()))
                    if not parts: continue
                    # Format: jobnr. mode duration R1 R2 ...
                    job_id = parts[0]
                    duration = parts[2]
                    reqs = parts[3:]
                    self.durations[job_id] = duration
                    self.requests[job_id] = reqs
                except ValueError:
                    continue
            
            elif mode == 'RESOURCES':
                if line.startswith('R'): continue
                if line.startswith('Resource'): continue # Some files might have headers
                if line.startswith('*'):
                    mode = None
                    continue
                try:
                    parts = list(map(int, line.split()))
                    # We accept if we find at least one capacity, even if it doesn't match num_resources exactly initially
                    # but typically it should.
                    if len(parts) > 0:
                        self.capacities = parts
                        if self.num_resources == 0:
                             self.num_resources = len(parts)
                        mode = None # Done
                except ValueError:
                    continue

    def check_validity(self):
        """Simple check to ensure instance is loaded correctly."""
        valid = True
        if self.num_jobs == 0:
            print("Error: No jobs loaded.")
            valid = False
        if self.num_resources == 0:
            print("Error: No resources loaded.")
            # Try to infer from capacities if parsing failed
            if self.capacities:
                self.num_resources = len(self.capacities)
                print(f"Inferred num_resources = {self.num_resources}")
            else:
                valid = False
        if not self.capacities:
            print("Error: No capacities loaded.")
            valid = False
        return valid

    def __repr__(self):
        return f"RCPSPInstance(jobs={self.num_jobs}, res={self.num_resources}, caps={self.capacities})"
