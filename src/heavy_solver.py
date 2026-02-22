import random
import heapq
from sgs import SGS
from instance import RCPSPInstance
from ns import NeighborhoodSearch

def solve_heavy(instance_path):
    inst = RCPSPInstance(instance_path)
    sgs = SGS(inst)
    
    # Genetic Algorithm Parameters
    POP_SIZE = 1000
    GENERATIONS = 5000
    
    # Initialize Population
    population = []
    best_makespan = float('inf')
    best_list = None
    
    print("Generating Population...")
    for _ in range(POP_SIZE):
        chrom = list(range(1, inst.num_jobs + 1))
        random.shuffle(chrom)
        sched, ms = sgs.parallel_sgs(chrom)
        population.append((ms, chrom))
        if ms < best_makespan:
            best_makespan = ms
            best_list = chrom
            print(f"Init Best: {best_makespan}")

    print("Evolving...")
    for gen in range(GENERATIONS):
        # Elitism
        population.sort(key=lambda x: x[0])
        
        if population[0][0] < best_makespan:
            best_makespan = population[0][0]
            best_list = population[0][1]
            print(f"Gen {gen}: New Best: {best_makespan}")
            if best_makespan <= 65:
                # Try local search aggressively when close
                ns = NeighborhoodSearch(inst, best_list, best_makespan)
                _, improved_ms = ns.improve(iterations=10000)
                if improved_ms < best_makespan:
                    best_makespan = improved_ms
                    print(f"  [NS] Improved to {best_makespan}!")
        
        # Stop if 65 reached (BKS)
        if best_makespan <= 65:
            print("Reached BKS 65!")
            break
            
        # Selection and Crossover
        new_pop = population[:50] # Elites
        
        while len(new_pop) < POP_SIZE:
            # Tournament
            p1 = population[random.randint(0, 200)][1] # Bias to top 20%
            p2 = population[random.randint(0, 200)][1]
            
            # Crossover
            cut = random.randint(1, len(p1)-1)
            child = p1[:cut] + [j for j in p2 if j not in p1[:cut]]
            
            # Mutation (Swap)
            if random.random() < 0.3:
                i, j = random.sample(range(len(child)), 2)
                child[i], child[j] = child[j], child[i]
                
            # Evaluate
            _, ms = sgs.parallel_sgs(child)
            new_pop.append((ms, child))
            
        population = new_pop
        
        # Periodic Local Search on Best
        if gen % 50 == 0:
            ns = NeighborhoodSearch(inst, population[0][1], population[0][0])
            improved_list, improved_ms = ns.improve(iterations=1000)
            if improved_ms < population[0][0]:
                population[0] = (improved_ms, improved_list)
                if improved_ms < best_makespan:
                    best_makespan = improved_ms
                    best_list = improved_list
                    print(f"Gen {gen} [NS]: Improved Best to {best_makespan}")

    print(f"Final Best: {best_makespan}")
    
    # Save
    sched, _ = sgs.parallel_sgs(best_list)
    with open("solution_j6010_8_heavy.txt", "w") as f:
        f.write(f"Instance: {instance_path}\n")
        f.write(f"Makespan: {best_makespan}\n")
        f.write("Schedule:\n")
        for j, s in sorted(sched.items()):
            if j!=0 and j!=inst.num_jobs+1:
                f.write(f"{j}: {s}\n")

if __name__ == "__main__":
    solve_heavy("/home/cheikhmelainine/SupNum_Challenge_S3C_1447/data/j6010_8.sm")
