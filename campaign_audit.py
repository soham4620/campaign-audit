# campaign_audit.py - Campaign Audit Quiz (Session 8)

import csv
import os
from datetime import date

DATA_FILE = "campaigns_B.csv"
RESULT_FILE = "result.csv"


def to_number(text):
    # it turns 3910,52 into 3910.52 and also a empty cell into nothing 
    text = text.strip().replace(" ", "").replace(",", ".")
    if text == "":
        return None
    return float(text)


def read_campaigns(filename):
    # it will open the csv files and the columns are seperated by;
    # it finds each column by the name because there is a empty columnn
    campaigns = []
    with open(filename, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter=";")
        header = [h.strip() for h in next(reader)]

        def col(start):
            for i, h in enumerate(header):
                if h.lower().startswith(start):
                    return i
            raise ValueError("Column not found: " + start)

        i_name, i_chan = col("campaign"), col("channel")
        i_imp, i_clk = col("impressions"), col("clicks")
        i_cost, i_conv, i_rev = col("cost"), col("conversions"), col("revenue")

        for row in reader:
            if not row or all(c.strip() == "" for c in row):
                continue  # ignore the empty lines
            impressions = to_number(row[i_imp])
            if impressions is None or impressions == 0:
                print("Excluded (no impressions):", row[i_name])
                continue
            campaigns.append({
                "name": row[i_name].strip(),
                "channel": row[i_chan].strip(),
                "impressions": impressions,
                "clicks": to_number(row[i_clk]) or 0,
                "cost": to_number(row[i_cost]) or 0,
                "conversions": to_number(row[i_conv]) or 0,
                "revenue": to_number(row[i_rev]) or 0,
            })
    return campaigns


def compute_kpis(campaigns):
    # calculates the CTR,CPA and ROAS for every campaign 
    # if there are zero conversions then there is no CPA,so no division by zero
    for c in campaigns:
        c["ctr"] = c["clicks"] / c["impressions"]
        c["cpa"] = c["cost"] / c["conversions"] if c["conversions"] > 0 else None
        c["roas"] = c["revenue"] / c["cost"] if c["cost"] > 0 else None
    return campaigns


def build_questions(campaigns):
    # the program calculates the right answers by itself,they are not written by hand 
    best_ctr = max(campaigns, key=lambda c: c["ctr"])
    with_cpa = [c for c in campaigns if c["cpa"] is not None]
    worst_cpa = max(with_cpa, key=lambda c: c["cpa"])
    roas_above_3 = sum(1 for c in campaigns if c["roas"] is not None and c["roas"] > 3)

    conv_by_channel = {}
    for c in campaigns:
        conv_by_channel[c["channel"]] = conv_by_channel.get(c["channel"], 0) + c["conversions"]
    top_channel = max(conv_by_channel, key=conv_by_channel.get)

    # average CTR of all the campaigns,in percent,with 2 decimals
    avg_ctr = round(sum(c["ctr"] for c in campaigns) / len(campaigns) * 100, 2)

    return [
        ("Which campaign has the best CTR?", best_ctr["name"], "text"),
        ("Which campaign has the highest CPA?", worst_cpa["name"], "text"),
        ("How many campaigns have a ROAS above 3?", roas_above_3, "int"),
        ("Which channel generated the most conversions in total?", top_channel, "text"),
        ("What is the average CTR across all campaigns, in %, rounded to two decimals?", avg_ctr, "float"),
    ]


def get_player_name():
    # asks the player name and asks again if he types nothing 
    while True:
        name = input("Your name: ").strip()
        if name:
            return name
        print("Please type a name.")


def check_answer(answer, correct, kind):
    # checks the answer, capital letters don’t matter and 2,78 or 2.78 both work
    answer = answer.strip()
    try:
        if kind == "int":
            return int(answer) == correct
        if kind == "float":
            return round(float(answer.replace(",", ".").replace("%", "")), 2) == correct
    except ValueError:
        return False
    return answer.lower() == str(correct).lower()


def play_quiz(questions):
    score = 0
    for number, (question, correct, kind) in enumerate(questions, start=1):
        print(f"\nQuestion {number}: {question}")
        answer = input("> ")
        if check_answer(answer, correct, kind):
            print("Correct!")
            score += 1
        else:
            print("Wrong. The answer was:", correct)
    return score


def save_result(name, score, total):
    # saves the name, score and date in result.csv, the title row only the first time
    new_file = not os.path.exists(RESULT_FILE)
    with open(RESULT_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["name", "score", "date"])
        writer.writerow([name, f"{score}/{total}", date.today().isoformat()])


def show_table(campaigns):
    # shows a table with CTR, CPA and ROAS so I can check one number by hand
    print(f"{'Campaign':<20}{'Channel':<14}{'CTR %':>8}{'CPA €':>10}{'ROAS':>8}")
    for c in campaigns:
        cpa = f"{c['cpa']:.2f}" if c["cpa"] is not None else "n/a"
        print(f"{c['name']:<20}{c['channel']:<14}{c['ctr']*100:>8.2f}{cpa:>10}{c['roas']:>8.2f}")


def main():
    step = "start"
    try:
        step = "read_campaigns"
        campaigns = read_campaigns(DATA_FILE)
        step = "compute_kpis"
        campaigns = compute_kpis(campaigns)
        show_table(campaigns)
        step = "build_questions"
        questions = build_questions(campaigns)
        step = "get_player_name"
        name = get_player_name()
        step = "play_quiz"
        score = play_quiz(questions)
        print(f"\nFinal score: {score}/{len(questions)}")
        step = "save_result"
        save_result(name, score, len(questions))
        print("Saved in", RESULT_FILE)
    except FileNotFoundError:
        print("File not found:", DATA_FILE)
    except Exception as e:
        print(f"Error in {step}: {e}")


if __name__ == "__main__":
    main()