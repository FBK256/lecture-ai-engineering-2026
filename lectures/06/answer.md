# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'search_phrase': 'Amazon S3 versioning', 'topics': ['general']})
- 気づき・疑問：ツールは内部でも外部でも使用できる.

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：実装
- やったこと：`app/mcp_server.py`で第3回の`make_quiz`をMCPツールとして公開した.範囲外の回を指定したときの返答を検証するテストを追加した.
- 結果：第99回を指定すると「第99回の確認問題はまだありません.用意されている回: ...」がツールの返答としてモデルに渡る.
- 気づき・疑問：`--trace`の`[tool return]`でツールの返答を確認できる.ツールの返答はエラーではなく通常の結果としてモデルに渡るため,モデルは用意されている回を案内できる.
