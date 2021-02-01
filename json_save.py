import json

j_strc = {
    "synonyms": {
        "abs": "3",
        "press": "3",
        "pull-up": "2",
        "pull-ups": "2",
        "pullup": "2",
        "pullups": "2",
        "pushup": "0",
        "pushups": "0",
        "squat": "1",
        "squats": "1",
        "отж": "0",
        "отжим": "0",
        "отжимание": "0",
        "отжиманий": "0",
        "отжимания": "0",
        "портной": "0",
        "подт": "2",
        "подтяг": "2",
        "подтягивание": "2",
        "подтягиваний": "2",
        "подтягивания": "2",
        "прес": "3",
        "пресс": "3",
        "присед": "1",
        "приседание": "1",
        "приседаний": "1",
        "приседания": "1",
        "трицепс": "4",
        "triceps": "4"
    },
    "workouts": {
        "0": "pushups",
        "1": "squats",
        "2": "pull-ups",
        "3": "abs",
        "4": "triceps"
    }
}

with open('workout_test.json', 'w', encoding="utf-8") as f:
    json.dump(j_strc, f, sort_keys=True, indent=4, ensure_ascii=False)

#
# with open('workout.json', 'r', encoding="utf-8") as f:
#     data = json.load(f)
#     print(data)
