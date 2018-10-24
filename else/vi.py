from mymodule import Mypickle

path = '../query/'
seeds_score = Mypickle.load(path,"seeds_score_1")

score_list = {}
for seed_k, seed_v in seeds_score.items():
  for path_k, path_v in seed_v.items():
    if path_k not in score_list: score_list[path_k] = 0
    score_list[path_k] += path_v[0]/len(seeds_score) * 1.0

print(sorted(score_list.items(), key=lambda x: x[1]))
