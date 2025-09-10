def process_scores(scores):
    print("Average:", sum(scores)/len(scores))
    print("Highest:", max(scores))
    print("Lowest:", min(scores))

process_scores([88, 92, 79, 93, 85])