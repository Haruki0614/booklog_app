# Booklog App - Render Deployment Guide

## 🚀 Renderでのデプロイ手順

### 1. Renderアカウントの準備
1. [Render.com](https://render.com)でアカウントを作成
2. GitHubリポジトリと連携

### 2. データベースの作成
1. Renderダッシュボードで「New PostgreSQL」を選択
2. 以下の設定で作成：
   - Name: `booklog-db`
   - Database Name: `booklog_db`
   - User: `booklog_user`

### 3. Webサービスの作成
1. Renderダッシュボードで「New Web Service」を選択
2. GitHubリポジトリを選択
3. 以下の設定：
   - Name: `booklog-app`
   - Environment: `Docker`
   - Build Command: (空欄)
   - Start Command: (空欄 - Dockerfileで指定)

### 4. 環境変数の設定
Renderのダッシュボードで以下の環境変数を設定：

```
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=booklog-app.onrender.com
DATABASE_URL=[PostgreSQLの接続文字列 - 自動設定]
```

### 5. 自動デプロイの設定
- Auto-Deploy: `Yes`
- Branch: `main`

### 6. デプロイの実行
1. 設定完了後、自動的にビルドが開始
2. ログを確認してエラーがないことを確認
3. デプロイ完了後、URLにアクセスして動作確認

## 📁 ファイル構造

```
booklog_app/
├── Dockerfile              # Render用Dockerファイル
├── render.yaml             # Render設定ファイル
├── .env.render             # 環境変数の例
├── backend/
│   ├── requirements.txt    # Python依存関係
│   ├── manage.py
│   └── config/
│       └── settings.py     # Django設定
└── README_RENDER.md        # このファイル
```

## 🔧 トラブルシューティング

### ビルドエラーの場合
1. Renderのログを確認
2. requirements.txtの依存関係を確認
3. Dockerfileの設定を確認

### 静的ファイルが表示されない場合
1. `STATICFILES_STORAGE`の設定を確認
2. `collectstatic`が正常に実行されているか確認

### データベース接続エラーの場合
1. `DATABASE_URL`が正しく設定されているか確認
2. PostgreSQLサービスが起動しているか確認

## 📝 注意事項

- 本番環境では必ず`DEBUG=False`に設定
- `SECRET_KEY`は安全な値を使用
- `ALLOWED_HOSTS`にRenderのドメインを追加
- データベースの移行は自動で実行されます

## 🔗 有用なリンク

- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
