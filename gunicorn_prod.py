# ワーカー数
workers = 4

# ワーカーのクラス、*2 にあるようにUvicornWorkerを指定 (Uvicornがインストールされている必要がある)
worker_class = 'uvicorn.workers.UvicornWorker'

# IPアドレスとポート
bind = '0.0.0.0:443'

# プロセスIDを保存するファイル名
pidfile = 'prod.pid'

# デーモン化する場合はTrue
daemon = True

# エラーログ
errorlog = './logs/error_log.txt'

# プロセスの名前
proc_name = 'esm'

# アクセスログ
accesslog = './logs/access_log.txt'

# SSL証明書とキーの場所 (HTTPS用)
certfile = "/etc/letsencrypt/live/inui.jn.sfc.keio.ac.jp/fullchain.pem"
keyfile = "/etc/letsencrypt/live/inui.jn.sfc.keio.ac.jp/privkey.pem"
