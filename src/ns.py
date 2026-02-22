import random
from instance import RCPSPInstance
from sgs import SGS

class NeighborhoodSearch:
    def __init__(self, instance, best_solution, best_makespan):
        self.instance = instance
        self.current_best = best_solution
        self.current_makespan = best_makespan
        self.sgs = SGS(instance)

    def improve(self, iterations=1000):
        """
        Local Search with Variable Neighborhood Descent (VND) principles.
        1. Adjacent Swap (Swap adjacent jobs)
        2. Arbitrary Swap (Swap any two jobs)
        3. Insert (Move job to new position)
        """
        n = len(self.current_best)
        improved = False
        
        # We iterate through different neighborhoods
        neighborhoods = ['swap_adjacent', 'swap_arbitrary', 'insert']
        
        no_improve_count = 0
        
        while no_improve_count < iterations:
            # Pick a neighborhood strategy
            # Start with small moves (adjacent), then larger ones
            strategy = random.choice(neighborhoods)
            
            new_list = list(self.current_best)
            
            if strategy == 'swap_adjacent':
                idx = random.randint(0, n - 2)
                # Swap
                new_list[idx], new_list[idx+1] = new_list[idx+1], new_list[idx]
                
            elif strategy == 'swap_arbitrary':
                # Swap two random indices
                i, j = random.sample(range(n), 2)
                new_list[i], new_list[j] = new_list[j], new_list[i]
                
            elif strategy == 'insert':
                # Pick a job and move it to a new position
                i = random.randint(0, n - 1)
                job = new_list.pop(i)
                j = random.randint(0, n - 1)
                new_list.insert(j, job)
            
            # Evaluate
            schedule, makespan = self.sgs.parallel_sgs(new_list)
            
            if makespan < self.current_makespan:
                self.current_best = new_list
                self.current_makespan = makespan
                improved = True
                no_improve_count = 0 # Reset counter
                print(f"  [NS] Improved Makespan to {self.current_makespan} ({strategy})")
                if self.current_makespan <= 65: # Optimization target
                    break
            else:
                no_improve_count += 1
                
        return self.current_best, self.current_makespan
