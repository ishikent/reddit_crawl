`reddit-thread-dumper` は、RedditのスレッドをMarkdown形式に変換するコマンドラインツールです。
指定したRedditスレッドのURLから、投稿内容、コメント、およびそれらのメタデータ(投稿者、日時、スコアなど)を取得し、整形されたMarkdownファ
イルとして出力します。

## 特徴

*   RedditスレッドのURLを1つ指定するだけで、簡単にMarkdown形式に変換
*   投稿のタイトル、本文、投稿者、日時、スコア、URLを出力
*   コメントは階層構造を保持し、各コメントの投稿者、日時、スコア、本文を出力
*   [deleted]コメントにも対応
*   MoreComments(読み込まれていないコメント)は"More comments... (not loaded)"として出力
*   PRAW (Python Reddit API Wrapper) を使用してReddit APIにアクセス
*   読み取り専用モードで動作するため、Redditアカウントは不要 (ただし、API制限に注意)
*   uvを使用してビルド、インストール

## 動作要件

*   Python 3.8 以上
*   praw

## インストール

1.  **uvのインストール (まだの場合):**
    ```bash
    pip install uv
    ```
    または
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **reddit-thread-dumperのインストール:**
    ```bash
    git clone https://github.com/<your_username>/reddit_crawl.git # リポジトリをクローン
    cd reddit_crawl
    uv build  # wheelファイルを生成
    uv pip install dist/reddit_thread_dumper-*.whl  # 生成されたwheelファイルをインストール
    ```

## 使い方

```bash
rtd <RedditスレッドのURL>

