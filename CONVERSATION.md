# CONVERSATION.md: my exchanges with the AI (Claude)

## 1. Asking for help
I uploaded the exam PDF and my file campaigns_B.csv and asked Claude to help me with the program.

## 2. What the AI found in my data file (the traps)
- The separator is `;` and not `,`
- There is an invisible BOM at the start of the file, so I open it with `utf-8-sig`
- There is an empty extra column between Conversions and Revenue, so the columns are found by name, not by position
- Amounts use the decimal comma (3910,52), so I replace `,` by `.` before converting to a number
- Micro Influence has an empty Impressions cell, so it is excluded from every calculation
- B2B Webinar and App Install have 0 conversions, so they have no CPA (no division by zero) but they stay in the other calculations

## 3. The program
Claude gave me campaign_audit.py split into functions: to_number, read_campaigns, compute_kpis, build_questions, get_player_name, check_answer, play_quiz, save_result, show_table, main.

## 4. Problems I had and how I fixed them
- GitHub said "no repository found": my account had no repository yet. I created a new repository `campaign-audit` and opened a Codespace on it.
- The CSV was named campaigns_B__1_.csv: I renamed it to campaigns_B.csv, otherwise the program says "File not found".
- I did not know how to copy the code from the file card: Claude pasted the code in the chat and I copied it from there.
- I rewrote all the comments in my own words. In one comment I wrote "conversations" instead of "conversions" and corrected it.

## 5. Checking one value by hand
Highest CPA: Monthly Newsletter, cost 86715,34 / 875 conversions = 99.10 €. The program gives the same value.

## 6. Results
- Best CTR: Blog Traffic (4.44 %)
- Highest CPA: Monthly Newsletter (99.10 €)
- Campaigns with ROAS above 3: 5
- Channel with most conversions: Email (3478)
- Average CTR: 2.78 %

I ran the program and got 5/5. The result is saved in result.csv.