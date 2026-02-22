from ns import NeighborhoodSearch

# ... inside solve function in main.py ...

# After generating initial population and finding best initial
# Add this inside the evolution loop when improvement slows down or periodically

# Inside the main loop:
if gen % 10 == 0:
    ns = NeighborhoodSearch(inst, best_list, best_makespan)
    new_chrom, new_makespan = ns.improve(iterations=2000)
    if new_makespan < best_makespan:
        best_makespan = new_makespan
        best_list = new_chrom
        # Update schedule
        best_schedule, _ = sgs.parallel_sgs(best_list)
        # Add to population
        population.append((best_makespan, best_list))
        print(f"  [NS] Improvement at Gen {gen}: {best_makespan}")
