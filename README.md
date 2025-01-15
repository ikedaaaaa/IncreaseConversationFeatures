# IncreaseConversationFeatures
既存の会話特徴量ファイルからさらに会話特徴量を増やす処理

基本的にはAnalyzeConversationと同じ．すでにある会話特徴量ファイル

## 1. コンテナを作成する．
``` bash
# yml,dockerfile,requirements.txtを編集した場合はbuildをする必要がある
docker compose -f compose.yml up --build -d

# buildをしなくてもいい場合
docker compose -f compose.yml up  -d
```

## 2. コンテナ内に入る．
``` bash
docker exec -it IncreaseConversationFeatures bash   
```

## 3. コンテナ内でpythonファイルを実行する
``` bash
# python main.py {音声ファイルのパス} {会話情報のcsvのパス}
例：python main.py ./data/test_file.wav ./data/test_file_info.csv
```

## 4. コンテナを壊す
``` bash
docker compose -f compose.yml down  
```

# 手順
特徴量csvを入力したら，追加で特徴量を分析し，cidに対応した形で会話特徴量を出力する．細かい考え方はwikに．それを元に細かい手順を考える．
