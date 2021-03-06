"""
Implements a family of rewards. Reward is a callable that:
- takes **session_record - see hnsw.EdgeHNSW.record_sessions or hnsw.ParallelHNSW.record_sessions
- a single number for each action -
"""


class MaxDCSReward:
    def __init__(self, max_dcs=1000, k=1, scale=False):
        self.max_dcs = max_dcs
        self.scale = scale
        self.k = k

    def __call__(self, best_vertex_ids, ground_truth_id,
                 total_distance_computations, actions, **etc):
        assert len(best_vertex_ids) >= self.k
        assert len(ground_truth_id) >= self.k

        answers = set(best_vertex_ids[:self.k])
        gts = set(ground_truth_id[:self.k].tolist())
        recall = float(len(answers & gts)) / self.k
        reward = recall * max(self.max_dcs - total_distance_computations, 1)
        if self.scale:
            reward /= self.max_dcs
        return [reward] * len(actions)


class RecallReward:
    def __call__(self, best_vertex_id, ground_truth_id, actions, **etc):
        recall = int(best_vertex_id == ground_truth_id[0])
        return [recall] * len(actions)


class WeightedRecallReward:
    def __init__(self, decay=0.5):
        self.decay = decay

    def __call__(self, best_vertex_id, ground_truth_id, actions, **etc):
        recall = 0.
        for i, gt in enumerate(ground_truth_id):
            if gt == best_vertex_id:
                recall = self.decay ** i
                break
        return [recall] * len(actions)
