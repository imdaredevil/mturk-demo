NUM_IMAGES = 10
NUM_ROWS = 5
QUESTIONS = [
    "Describe in detail the item or alteration that is being used to hide the identity of the person",
    "Describe why the item or alteration being used to hide the identity looks unnatural"
]

CLEAN_FIELDNAMES = ["transaction_id", "trial_id", "trial_name", "ground_truth"]

for i in range(NUM_ROWS):
    CLEAN_FIELDNAMES.append(f"des{i}")
    CLEAN_FIELDNAMES.append(f"status des{i}")
    