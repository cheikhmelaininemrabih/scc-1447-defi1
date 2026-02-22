import random
import heapq
import time
import os
import sys

# Ensure instance.py, sgs.py, genetic.py, ns.py are in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from instance import RCPSPInstance
from sgs import SGS
from ns import NeighborhoodSearch

def solve(instance_path):
    print(f"Solving {instance_path}...")
    inst = RCPSPInstance(instance_path)
    print(f"Loaded: Jobs={inst.num_jobs}, Resources={inst.num_resources}, Capacities={inst.capacities}")
    
    if inst.num_resources == 0:
        print("CRITICAL: No resources loaded. Exiting.")
        return

    # Increase parameters for serious run
    POP_SIZE = 1000
    GENERATIONS = 2000
    # Add restart mechanism if stuck?
    
    # Create initial population (Random Priority Lists)
    # The priority list should be a permutation of 1..num_jobs
    population = []
    sgs = SGS(inst)
    
    jobs = list(range(1, inst.num_jobs + 1))
    
    start_time = time.time()
    
    best_makespan = float('inf')
    best_schedule = None
    best_list = None
    
    print("Initializing Population...")
    for _ in range(POP_SIZE):
        prio_list = jobs[:]
        random.shuffle(prio_list)
        sched, makespan = sgs.parallel_sgs(prio_list)
        population.append((makespan, prio_list))
        
        if makespan < best_makespan:
            best_makespan = makespan
            best_schedule = sched
            best_list = prio_list
            print(f"  Initial Best: {best_makespan}")

    print(f"Starting Evolution (Target < 65)...")
    
    for gen in range(GENERATIONS):
        # Sort by makespan (minimize)
        population.sort(key=lambda x: x[0])
        
        # Check current best
        if population[0][0] < best_makespan:
            best_makespan = population[0][0]
            best_list = population[0][1]
            # Re-generate schedule to store
            best_schedule, _ = sgs.parallel_sgs(best_list)
            print(f"Gen {gen}: New Best Makespan = {best_makespan}")
        
        if best_makespan <= 64:
            print("Target reached! Stopping.")
            break
            
        # Run Neighborhood Search periodically
        if gen % 20 == 0:
            ns = NeighborhoodSearch(inst, best_list, best_makespan)
            new_chrom, new_makespan = ns.improve(iterations=2000)
            if new_makespan < best_makespan:
                best_makespan = new_makespan
                best_list = new_chrom
                best_schedule, _ = sgs.parallel_sgs(best_list)
                print(f"Gen {gen}: [NS] New Best Makespan = {best_makespan}")
                # Add to population
                population.append((best_makespan, best_list))
                
        # Forward-Backward Improvement (FBI) on Best
        if gen % 10 == 0:
            fbi_sched, fbi_ms, fbi_list = sgs.fbi(best_schedule, best_makespan)
            if fbi_ms < best_makespan:
                best_makespan = fbi_ms
                best_schedule = fbi_sched
                best_list = fbi_list
                print(f"Gen {gen}: [FBI] New Best Makespan = {best_makespan}")
                population.append((best_makespan, best_list))
            
        # Elitism
        new_pop = population[:10]
        
        # Crossover & Mutation
        while len(new_pop) < POP_SIZE:
            # Tournament Selection
            p1 = min(random.sample(population, 3), key=lambda x: x[0])[1]
            p2 = min(random.sample(population, 3), key=lambda x: x[0])[1]
            
            # Simple Crossover (Order 1)
            cut = random.randint(1, len(jobs) - 1)
            child1 = p1[:cut] + [j for j in p2 if j not in p1[:cut]]
            
            # Mutation
            if random.random() < 0.2:
                idx1, idx2 = random.sample(range(len(child1)), 2)
                child1[idx1], child1[idx2] = child1[idx2], child1[idx1]
            
            # Evaluate
            sched, ms = sgs.parallel_sgs(child1)
            new_pop.append((ms, child1))
            
        population = new_pop

    print(f"Final Best Makespan: {best_makespan}")
    
    # Save Solution
    output_path = "solution_j6010_8.txt"
    with open(output_path, "w") as f:
        f.write(f"Instance: {os.path.basename(instance_path)}\n")
        f.write(f"Makespan: {best_makespan}\n")
        f.write("Schedule (Job ID: Start Time):\n")
        sorted_jobs = sorted(best_schedule.items())
        for j, start in sorted_jobs:
            if j == 0 or j == inst.num_jobs + 1: continue
            f.write(f"{j}: {start}\n")
            
    print(f"Solution saved to {output_path}")

    # Verify
    verify_solution(inst, best_schedule, best_makespan)

def verify_solution(inst, schedule, reported_makespan):
    print("\n--- Verifying Solution ---")
    
    # Check Precedence
    for j in range(1, inst.num_jobs + 1):
        start_j = schedule.get(j, 0)
        for pred in inst.predecessors[j]:
            finish_pred = schedule.get(pred, 0) + inst.durations[pred]
            if start_j < finish_pred:
                print(f"❌ Precedence FAIL: Job {j} starts at {start_j} before pred {pred} finishes at {finish_pred}")
                return False
                
    print("✅ Precedence Constraints: OK")
    
    # Check Resources
    horizon = reported_makespan + 1
    usage = {r: [0] * horizon for r in range(inst.num_resources)}
    
    for j in range(1, inst.num_jobs + 1):
        start = schedule.get(j, 0)
        dur = inst.durations[j]
        reqs = inst.requests[j]
        
        for t in range(start, start + dur):
            for r in range(inst.num_resources):
                usage[r][t] += reqs[r]
                
    # Check against capacities
    violation = False
    for r in range(inst.num_resources):
        cap = inst.capacities[r]
        for t in range(horizon):
            if usage[r][t] > cap:
                print(f"❌ Resource FAIL: Res {r+1} at time {t}, used {usage[r][t]} > {cap}")
                violation = True
                
    if not violation:
        print("✅ Resource Constraints: OK")
        print(f"🎉 VALID SOLUTION FOUND: Makespan {reported_makespan}")
        return True
    else:
        print("❌ Solution INVALID due to resource overload.")
        return False

if __name__ == "__main__":
    instance_file = "/home/cheikhmelainine/SupNum_Challenge_S3C_1447/data/j6010_8.sm"
    solve(instance_file)
