import random
import copy
from sgs import SGS

class GeneticAlgorithm:
    def __init__(self, instance, pop_size=100, max_generations=200):
        self.instance = instance
        self.pop_size = pop_size
        self.max_generations = max_generations
        self.sgs = SGS(instance)
        
        self.population = [] # List of (chromosome, makespan)
        self.best_makespan = float('inf')
        self.best_solution = None
        
        # Precompute valid priorities range (1..N)
        self.jobs = list(range(1, instance.num_jobs + 1))
        
        # Topological Sort base for validation
        self.topo_order = self.topological_sort()

    def topological_sort(self):
        # Kahn's algorithm or DFS
        # We need A valid topological sort
        # But for GA, chromosomes are priority lists (permutation).
        # Any permutation is technically valid input for Serial SGS if we skip ineligible.
        # However, for Parallel SGS and crossovers, we prefer topological valid permutations.
        
        in_degree = {j: len(self.instance.predecessors[j]) for j in self.jobs}
        queue = [j for j in self.jobs if in_degree[j] == 0]
        topo = []
        
        while queue:
            u = queue.pop(0)
            topo.append(u)
            for v in self.instance.successors[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
        return topo

    def generate_initial_population(self):
        # Generate random topological permutations
        # Or just random priority lists if SGS handles precedence.
        # Parallel SGS handles precedence dynamically using eligible set.
        # Serial SGS handles precedence dynamically too.
        # So permutation is just a priority guide.
        
        for _ in range(self.pop_size):
            # Start with base topo order and perturb slightly?
            # Or just random shuffle of jobs?
            # Standard GA RCPSP uses random keys or topological sort variants.
            # Let's use random topological sorts (random tie breaking in Kahn's algo)
            
            chrom = self.random_topological_sort()
            makespan = self.evaluate(chrom)
            self.population.append({'chrom': chrom, 'makespan': makespan})
            
            if makespan < self.best_makespan:
                self.best_makespan = makespan
                self.best_solution = chrom

    def random_topological_sort(self):
        in_degree = {j: len(self.instance.predecessors[j]) for j in self.jobs}
        # Use a list for eligible set to pick randomly
        eligible = [j for j in self.jobs if in_degree[j] == 0]
        topo = []
        
        while eligible:
            # Pick random eligible job
            idx = random.randint(0, len(eligible) - 1)
            u = eligible.pop(idx)
            topo.append(u)
            
            for v in self.instance.successors[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    eligible.append(v)
        return topo

    def evaluate(self, chromosome):
        # Use Parallel SGS for evaluation (usually better for makespan)
        # Serial SGS is better for robust scheduling but Parallel often gives tighter schedules
        # The paper uses both? Or P-SGS primarily.
        schedule, makespan = self.sgs.parallel_sgs(chromosome)
        return makespan

    def crossover(self, p1, p2):
        # Simple One-Point Crossover for Permutations (maintaining relative order)
        # Or better: Precedence Preservative Crossover (PPX) or similar.
        # Here implementing a simple ordered crossover
        
        n = len(p1)
        point = random.randint(1, n - 1)
        
        # Offspring 1: Left part from P1, Right part from P2 (relative order)
        child1 = p1[:point]
        set1 = set(child1)
        child1 += [gene for gene in p2 if gene not in set1]
        
        # Offspring 2
        child2 = p2[:point]
        set2 = set(child2)
        child2 += [gene for gene in p1 if gene not in set2]
        
        return child1, child2

    def mutation(self, chrom):
        # Swap mutation (adjacent swap is safer for precedence, or arbitrary swap)
        # Check precedence feasibility if swapping arbitrary.
        # Or just swap and let SGS handle it (priority changes).
        # We swap two random elements.
        
        new_chrom = chrom[:]
        idx1, idx2 = random.sample(range(len(chrom)), 2)
        new_chrom[idx1], new_chrom[idx2] = new_chrom[idx2], new_chrom[idx1]
        return new_chrom

    def run(self):
        self.generate_initial_population()
        
        for generation in range(self.max_generations):
            # Sort population
            self.population.sort(key=lambda x: x['makespan'])
            
            # Elitism
            new_pop = self.population[:int(self.pop_size * 0.1)]
            
            # Generate offspring
            while len(new_pop) < self.pop_size:
                # Tournament Selection
                p1 = self.tournament_select()
                p2 = self.tournament_select()
                
                c1_chrom, c2_chrom = self.crossover(p1['chrom'], p2['chrom'])
                
                # Mutation
                if random.random() < 0.1:
                    c1_chrom = self.mutation(c1_chrom)
                if random.random() < 0.1:
                    c2_chrom = self.mutation(c2_chrom)
                
                new_pop.append({'chrom': c1_chrom, 'makespan': self.evaluate(c1_chrom)})
                new_pop.append({'chrom': c2_chrom, 'makespan': self.evaluate(c2_chrom)})
            
            self.population = new_pop[:self.pop_size]
            current_best = self.population[0]
            
            if current_best['makespan'] < self.best_makespan:
                self.best_makespan = current_best['makespan']
                self.best_solution = current_best['chrom']
                print(f"Gen {generation}: New Best Makespan = {self.best_makespan}")
            
        return self.best_solution, self.best_makespan

    def tournament_select(self, k=3):
        candidates = random.sample(self.population, k)
        return min(candidates, key=lambda x: x['makespan'])
