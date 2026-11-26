import sys, json, sqlite3
sys.path.insert(0, sys.argv[1])
from catalog import Catalog
conn = sqlite3.connect(":memory:", isolation_level=None); conn.execute("PRAGMA foreign_keys=ON")
c = Catalog(conn)
# accidental stopword hit (Toyota-like)
t = c.add("https://global.toyota/en/company/vision-and-philosophy/production-system/")
b = c.add("https://bazel.build/remote/caching", title="Bazel remote cache")
print("query 'throttle writes to slow disk and refill buffer':")
for h in c.discover("throttle writes to slow disk and refill buffer", limit=5):
    print("  ", h["url"], "| why:", h["why"])
print("query ko '느린 저장 장치에 쓰기를 당겨서 보충':", c.discover("느린 저장 장치에 쓰기를 당겨서 보충", limit=5))
# identity
urls = ["https://github.com/paperless-ngx/paperless-ngx/blob/main/docs/usage.md",
        "https://github.com/paperless-ngx/paperless-ngx/blob/4973be8499bc61dc4f791a609d0d31e9ac9ccd41/docs/usage.md",
        "https://docs.paperless-ngx.com/usage/",
        "https://docs.paperless-ngx.com/usage",
        "HTTPS://Docs.Paperless-ngx.com:443/usage/",
        "https://docs.paperless-ngx.com/usage/#consumption",
        "https://docs.paperless-ngx.com/usage/?utm_source=x"]
ids = [c.add(u) for u in urls]
for u,i in zip(urls,ids): print(i, u)
print("distinct items:", len(set(ids)), "of", len(urls))
# title conflict
try:
    c.add("https://docs.paperless-ngx.com/usage/", title="Usage A"); c.add("https://docs.paperless-ngx.com/usage/", title="Usage B")
except Exception as e: print("retitle:", e)
