import heapq

class SGS:
    def __init__(self, instance):
        self.instance = instance

    def serial_sgs(self, priority_list):
        """
        Serial Schedule Generation Scheme.
        Jobs are selected one by one from priority list and scheduled at earliest feasible time.
        """
        num_jobs = self.instance.num_jobs
        schedule = {}
        scheduled = set()
        
        # Predecessor count tracking
        unscheduled_preds = {j: len(self.instance.predecessors[j]) for j in range(1, num_jobs + 1)}
        
        resource_usage = {} 
        
        def get_usage(t):
            if t not in resource_usage:
                resource_usage[t] = [0] * self.instance.num_resources
            return resource_usage[t]

        def check_feasibility(start, duration, reqs):
            for t in range(start, start + duration):
                usage = get_usage(t)
                for r in range(self.instance.num_resources):
                    if usage[r] + reqs[r] > self.instance.capacities[r]:
                        return False
            return True

        def book_resources(start, duration, reqs):
            for t in range(start, start + duration):
                usage = get_usage(t)
                for r in range(self.instance.num_resources):
                    usage[r] += reqs[r]

        schedule[0] = 0
        scheduled.add(0)
        
        for job in priority_list:
            if job == 0 or job == num_jobs + 1: continue 
            
            est = 0
            for pred in self.instance.predecessors[job]:
                if pred in schedule:
                    finish = schedule[pred] + self.instance.durations[pred]
                    if finish > est: est = finish
            
            duration = self.instance.durations[job]
            reqs = self.instance.requests[job]
            
            start_time = est
            while True:
                if check_feasibility(start_time, duration, reqs):
                    break
                start_time += 1
            
            schedule[job] = start_time
            book_resources(start_time, duration, reqs)
            scheduled.add(job)
            
        sink = num_jobs + 1
        makespan = 0
        for j in range(1, num_jobs + 1):
            finish = schedule[j] + self.instance.durations[j]
            if finish > makespan: makespan = finish
        schedule[sink] = makespan
            
        return schedule, makespan

    def parallel_sgs(self, priority_list, direction='forward'):
        """
        Parallel Schedule Generation Scheme.
        If direction='backward', we schedule on the REVERSED graph logic.
        """
        num_jobs = self.instance.num_jobs
        schedule = {}
        scheduled = set()
        active_jobs = [] 
        
        if direction == 'forward':
            preds_dict = self.instance.predecessors
            succs_dict = self.instance.successors
            jobs_to_schedule = list(range(1, num_jobs + 1))
        else:
            # Backward: Swap Predecessors and Successors
            preds_dict = self.instance.successors
            succs_dict = self.instance.predecessors
            jobs_to_schedule = list(range(1, num_jobs + 1))

        priority_map = {job: i for i, job in enumerate(priority_list)}
        unscheduled_preds = {j: len(preds_dict[j]) for j in jobs_to_schedule}
        
        eligible = []
        for j in jobs_to_schedule:
            if unscheduled_preds[j] == 0:
                heapq.heappush(eligible, (priority_map.get(j, float('inf')), j))
                
        time = 0
        completed_count = 0
        
        while completed_count < len(jobs_to_schedule):
            active_jobs.sort(key=lambda x: x[0])
            while active_jobs and active_jobs[0][0] <= time:
                fin, j = active_jobs.pop(0)
                for succ in succs_dict[j]:
                    unscheduled_preds[succ] -= 1
                    if unscheduled_preds[succ] == 0:
                        heapq.heappush(eligible, (priority_map.get(succ, float('inf')), succ))
                completed_count += 1
            
            current_usage = [0] * self.instance.num_resources
            for fin, j in active_jobs:
                reqs = self.instance.requests[j]
                for r in range(self.instance.num_resources):
                    current_usage[r] += reqs[r]
            
            available = [self.instance.capacities[r] - current_usage[r] for r in range(self.instance.num_resources)]
            
            temp_skipped = []
            while eligible:
                prio, job = heapq.heappop(eligible)
                reqs = self.instance.requests[job]
                
                can_start = True
                for r in range(self.instance.num_resources):
                    if reqs[r] > available[r]:
                        can_start = False
                        break
                
                if can_start:
                    schedule[job] = time
                    scheduled.add(job)
                    duration = self.instance.durations[job]
                    active_jobs.append((time + duration, job))
                    
                    for r in range(self.instance.num_resources):
                        available[r] -= reqs[r]
                else:
                    temp_skipped.append((prio, job))
            
            for item in temp_skipped:
                heapq.heappush(eligible, item)
                
            if completed_count < len(jobs_to_schedule):
                if active_jobs:
                    time = active_jobs[0][0]
                elif eligible:
                     break
                else:
                    break 

        makespan = 0
        for j in schedule:
            fin = schedule[j] + self.instance.durations[j]
            if fin > makespan: makespan = fin
            
        return schedule, makespan

    def fbi(self, schedule, makespan):
        """
        Forward-Backward Improvement.
        1. Forward Schedule (Input)
        2. Backward Schedule: Priorities = decreasing completion times of Forward.
        3. Forward Schedule: Priorities = increasing start times of Backward.
        """
        completions = []
        for j, start in schedule.items():
            if j == 0 or j == self.instance.num_jobs + 1: continue
            finish = start + self.instance.durations[j]
            completions.append((finish, j))
        
        completions.sort(key=lambda x: x[0], reverse=True)
        backward_prio_list = [j for f, j in completions]
        
        back_schedule, back_makespan = self.parallel_sgs(backward_prio_list, direction='backward')
        
        back_starts = []
        for j, start in back_schedule.items():
            if j == 0 or j == self.instance.num_jobs + 1: continue
            back_starts.append((start, j))
            
        back_starts.sort(key=lambda x: x[0], reverse=True)
        forward_prio_list = [j for s, j in back_starts]
        
        new_schedule, new_makespan = self.parallel_sgs(forward_prio_list, direction='forward')
        
        return new_schedule, new_makespan, forward_prio_list
