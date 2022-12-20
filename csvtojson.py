# csvをjsonファイルに直す
import pandas as pd

df = pd.read_csv("newly_confirmed_cases_daily.csv")
df.to_json("new_confirm.json",orient='records',lines=True)