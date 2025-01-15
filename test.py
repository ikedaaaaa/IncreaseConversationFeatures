# # import pandas as pd

# # # データの作成
# # data = [
# #     ["2023-12-04 15:29:24", "2023-12-04 15:29:26", 0],
# #     ["2023-12-04 15:29:26", "2023-12-04 15:29:26", -1],
# #     ["2023-12-04 15:29:26", "2023-12-04 15:29:27", 1],
# #     ["2023-12-04 15:29:27", "2023-12-04 15:29:28", -1],
# #     ["2023-12-04 15:29:28", "2023-12-04 15:29:29", 1],
# #     ["2023-12-04 15:29:29", "2023-12-04 15:29:30", -1],
# #     ["2023-12-04 15:29:30", "2023-12-04 15:29:34", 0],
# #     ["2023-12-04 15:29:34", "2023-12-04 15:29:33", -1],
# #     ["2023-12-04 15:29:33", "2023-12-04 15:29:35", 1],
# #     ["2023-12-04 15:29:35", "2023-12-04 15:29:36", -1],
# #     ["2023-12-04 15:29:36", "2023-12-04 15:29:38", 0],
# #     ["2023-12-04 15:29:38", "2023-12-04 15:29:39", -1],
# #     ["2023-12-04 15:29:39", "2023-12-04 15:29:40", 1],
# #     ["2023-12-04 15:29:40", "2023-12-04 15:29:42", -1],
# #     ["2023-12-04 15:29:42", "2023-12-04 15:29:43", 1],
# #     ["2023-12-04 15:29:43", "2023-12-04 15:29:43", -1],
# #     ["2023-12-04 15:29:43", "2023-12-04 15:29:48", 0],
# #     ["2023-12-04 15:30:33", "2023-12-04 15:30:40", 1],
# #     ["2023-12-04 15:30:34", "2023-12-04 15:30:37", 0],
# #     ["2023-12-04 15:30:38", "2023-12-04 15:30:39", 0],
# #     ["2023-12-04 15:30:41", "2023-12-04 15:30:43", 1],
# # ]

# # # DataFrameの作成
# # df = pd.DataFrame(data, columns=["start_time", "end_time", "speaker"])

# # # 時間をdatetime型に変換
# # df["start_time"] = pd.to_datetime(df["start_time"])
# # df["end_time"] = pd.to_datetime(df["end_time"])

# # # 無音時間（-1）を排除
# # df = df[df["speaker"] != -1].reset_index(drop=True)

# # # 発話開始時間順にソートし、同じ場合は終了時間順にソート
# # df = df.sort_values(by=["start_time", "end_time"]).reset_index(drop=True)

# # # 無音時間の挿入
# # new_rows = []
# # for i in range(len(df) - 1):
# #     current_row = df.iloc[i]
# #     next_row = df.iloc[i + 1]

# #     # 現在の行を追加
# #     new_rows.append(current_row)

# #     # 無音時間の条件を満たす場合、挿入
# #     if current_row["end_time"] < next_row["start_time"]:
# #         new_rows.append(pd.Series({
# #             "start_time": current_row["end_time"],
# #             "end_time": next_row["start_time"],
# #             "speaker": -1
# #         }))

# # # 最後の行を追加
# # new_rows.append(df.iloc[-1])

# # # 新しいDataFrameを作成
# # df_cleaned = pd.DataFrame(new_rows)

# # # 結果を表示
# # print(df_cleaned)


# import pandas as pd

# # データ
# data = [
#     ["2023-12-04 15:30:33", "2023-12-04 15:30:40", 1],
#     ["2023-12-04 15:30:34", "2023-12-04 15:30:37", 0],
#     ["2023-12-04 15:30:38", "2023-12-04 15:30:39", 0],
#     ["2023-12-04 15:30:41", "2023-12-04 15:30:43", 1],
# ]

# # DataFrameの作成
# df = pd.DataFrame(data, columns=["start_time", "end_time", "speaker"])

# # 時間をdatetime型に変換
# df["start_time"] = pd.to_datetime(df["start_time"])
# df["end_time"] = pd.to_datetime(df["end_time"])

# # 発話開始時間順にソートし、終了時間順にソート
# df = df.sort_values(by=["start_time", "end_time"]).reset_index(drop=True)

# # 無音時間の挿入
# new_rows = []
# for i in range(len(df) - 1):
#     current_row = df.iloc[i]
#     next_row = df.iloc[i + 1]

#     # 現在の行を追加
#     new_rows.append(current_row)

#     # 実際に無音時間が存在するかを確認
#     if (
#         current_row["end_time"] < next_row["start_time"]
#         and all(
#             current_row["end_time"] > row["start_time"]
#             or current_row["end_time"] <= row["end_time"]
#             for _, row in df.iloc[: i + 1].iterrows()
#         )
#     ):
#         # 無音時間を挿入
#         new_rows.append(pd.Series({
#             "start_time": current_row["end_time"],
#             "end_time": next_row["start_time"],
#             "speaker": -1
#         }))

# # 最後の行を追加
# new_rows.append(df.iloc[-1])

# # 新しいDataFrameを作成
# df_cleaned = pd.DataFrame(new_rows)

# # 結果を表示
# print(df_cleaned)

import pandas as pd

# データ
data = [
    ["2023-12-04 15:29:24", "2023-12-04 15:29:26", 0],
    ["2023-12-04 15:29:26", "2023-12-04 15:29:26", -1],
    ["2023-12-04 15:29:26", "2023-12-04 15:29:27", 1],
    ["2023-12-04 15:29:27", "2023-12-04 15:29:28", -1],
    ["2023-12-04 15:29:28", "2023-12-04 15:29:29", 1],
    ["2023-12-04 15:29:29", "2023-12-04 15:29:30", -1],
    ["2023-12-04 15:29:30", "2023-12-04 15:29:34", 0],
    ["2023-12-04 15:29:34", "2023-12-04 15:29:33", -1],
    ["2023-12-04 15:29:33", "2023-12-04 15:29:35", 1],
    ["2023-12-04 15:29:35", "2023-12-04 15:29:36", -1],
    ["2023-12-04 15:29:36", "2023-12-04 15:29:38", 0],
    ["2023-12-04 15:29:38", "2023-12-04 15:29:39", -1],
    ["2023-12-04 15:29:39", "2023-12-04 15:29:40", 1],
    ["2023-12-04 15:29:40", "2023-12-04 15:29:42", -1],
    ["2023-12-04 15:29:42", "2023-12-04 15:29:43", 1],
    ["2023-12-04 15:29:43", "2023-12-04 15:29:43", -1],
    ["2023-12-04 15:29:43", "2023-12-04 15:29:48", 0],
    ["2023-12-04 15:30:33", "2023-12-04 15:30:40", 1],
    ["2023-12-04 15:30:33", "2023-12-04 15:30:38", 1],
    ["2023-12-04 15:30:34", "2023-12-04 15:30:37", 0],
    ["2023-12-04 15:30:38", "2023-12-04 15:30:39", 0],
    ["2023-12-04 15:30:41", "2023-12-04 15:30:43", 1],
]

# DataFrameの作成
df = pd.DataFrame(data, columns=["start_time", "end_time", "speaker"])

# 時間をdatetime型に変換
df["start_time"] = pd.to_datetime(df["start_time"])
df["end_time"] = pd.to_datetime(df["end_time"])

# 無音時間（-1）を排除
df = df[df["speaker"] != -1].reset_index(drop=True)

# 発話開始時間順にソートし、終了時間順にソート
df = df.sort_values(by=["start_time", "end_time"]).reset_index(drop=True)

# 新しい行を格納するリスト
new_rows = []

# 無音時間の挿入処理
last_end_time = None  # 前回のend_timeを記憶する変数

for _, row in df.iterrows():
    if last_end_time is not None and row["start_time"] > last_end_time:
        # 無音時間を挿入
        new_rows.append(pd.Series({
            "start_time": last_end_time,
            "end_time": row["start_time"],
            "speaker": -1
        }))
    # 現在の行を追加
    new_rows.append(row.to_dict())
    # 現在のend_timeを記憶
    last_end_time = max(last_end_time, row["end_time"]) if last_end_time else row["end_time"]

# 新しいDataFrameを作成
df_cleaned = pd.DataFrame(new_rows)

# 結果を表示
print(df_cleaned)
