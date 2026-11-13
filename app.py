# ============================================================
# 🎬 منصة السينما والوثائقيات الحرة (نسخة بدون API)
# التشغيل: pip install flask
#           python app.py
# ============================================================

from flask import Flask, render_template_string, request

app = Flask(__name__)

# قائمة الأفلام والوثائقيات الخاصة بك (تضيف وتعدل عليها بحرية تامة)
MOVIES_DB = [
    {
        "id": "night-of-the-living-dead",
        "title": "ليلة الموتى الأحياء (1968)",
        "category": "أفلام كلاسيكية",
        "year": "1968",
        "creator": "جورج روميرو",
        "description": "أحد أشهر أفلام الرعب والخيال الكلاسيكية في تاريخ السينما، متاح في الملك العام.",
        "embed_url": "https://archive.org/embed/night_of_the_living_dead",
        "thumb": "https://archive.org/services/img/night_of_the_living_dead"
    },
    {
        "id": "apollo-11-moon",
        "title": "وثائقي الهبوط على القمر - أبولو 11",
        "category": "علوم وفضاء",
        "year": "1969",
        "creator": "وكالة ناسا (NASA)",
        "description": "لقطات وثائقية أصلية من أرشيف ناسا توثق رحلة الإنسان الأولى إلى سطح القمر.",
        "embed_url": "https://archive.org/embed/Apollo11Moonwalk",
        "thumb": "https://archive.org/services/img/Apollo11Moonwalk"
    },
    {
        "id": "charlie-chaplin-kid",
        "title": "تشارلي شابلن - الصبي (The Kid)",
        "category": "أفلام كلاسيكية",
        "year": "1921",
        "creator": "تشارلي شابلن",
        "description": "تحفة سينمائية صامتة تجمع بين الكوميديا والدراما الإنسانية.",
        "embed_url": "https://archive.org/embed/TheKid1921",
        "thumb": "https://archive.org/services/img/TheKid1921"
    },
    {
        "id": "planet-earth-nature",
        "title": "أسرار الطبيعة والحياة البرية",
        "category": "طبيعة",
        "year": "2015",
        "creator": "أرشيف الطبيعة",
        "description": "جولة بصرية مذهلة تستكشف جمال الحياة البرية والتوازن البيئي.",
        "embed_url": "https://archive.org/embed/NatureDocumentarySample",
        "thumb": "https://archive.org/services/img/NatureDocumentarySample"
    }
]

HTML_HEADER = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>سينما الوثائقيات والأفلام الحرة</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #0f1014; color: #f1f1f1; line-height: 1.6; }
  .container { max-width: 1100px; margin: 0 auto; padding: 0 18px; }
  header { background: #181a20; padding: 16px 0; border-bottom: 2px solid #e50914; position: sticky; top: 0; z-index: 100; }
  .nav-wrap { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
  .logo { color: #e50914; font-size: 1.4rem; font-weight: bold; text-decoration: none; }
  .cats { display: flex; gap: 10px; flex-wrap: wrap; }
  .cats a { color: #ccc; text-decoration: none; font-size: 0.9rem; padding: 5px 12px; border-radius: 20px; background: #252830; }
  .cats a:hover { background: #e50914; color: #fff; }
  .search-box { display: flex; gap: 6px; }
  .search-box input { padding: 8px 14px; border-radius: 20px; border: none; background: #252830; color: #fff; outline: none; }
  .search-box button { padding: 8px 16px; border-radius: 20px; border: none; background: #e50914; color: #fff; cursor: pointer; font-weight: bold; }
  main { padding: 30px 0; min-height: 75vh; }
  h2 { margin-bottom: 20px; font-size: 1.3rem; border-right: 4px solid #e50914; padding-right: 12px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 20px; }
  .card { background: #181a20; border-radius: 12px; overflow: hidden; transition: 0.3s; border: 1px solid #252830; }
  .card:hover { transform: translateY(-5px); border-color: #e50914; }
  .card a { text-decoration: none; color: inherit; display: block; }
  .thumb { width: 100%; height: 155px; object-fit: cover; background: #222; display: block; }
  .info { padding: 14px; }
  .badge { display: inline-block; background: #e50914; color: #fff; font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; margin-bottom: 6px; }
  .info h3 { font-size: 1rem; margin-bottom: 6px; color: #fff; }
  .meta { font-size: 0.8rem; color: #999; }
  .player-box { background: #181a20; padding: 20px; border-radius: 14px; }
  .video-frame { width: 100%; aspect-ratio: 16 / 9; border: none; border-radius: 10px; background: #000; }
  .details { margin-top: 20px; }
  .details h1 { font-size: 1.5rem; color: #fff; margin-bottom: 10px; }
  .details p { color: #bbb; font-size: 0.95rem; margin-top: 10px; }
  .btn { display: inline-block; margin-top: 15px; padding: 10px 20px; background: #e50914; color: #fff; text-decoration: none; border-radius: 8px; font-weight: bold; }
  footer { text-align: center; padding: 20px; background: #181a20; color: #777; margin-top: 40px; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <div class="container nav-wrap">
    <a href="/" class="logo">🎬 سينما الوثائقيات الحرة</a>
    <div class="cats">
      <a href="/">الكل</a>
      <a href="/?cat=أفلام كلاسيكية">أفلام كلاسيكية</a>
      <a href="/?cat=علوم وفضاء">علوم وفضاء</a>
      <a href="/?cat=طبيعة">طبيعة</a>
    </div>
    <form action="/" method="get" class="search-box">
      <input type="text" name="q" placeholder="ابحث بالعربي...">
      <button type="submit">بحث</button>
    </form>
  </div>
</header>
<main class="container">
"""

HTML_FOOTER = """
</main>
<footer>
  <p>© 2026 منصة السينما والوثائقيات الحرة — تعمل محلياً بدون أي API خارجي</p>
</footer>
</body>
</html>
"""

@app.route("/")
def home():
    q = request.args.get("q", "").strip()
    cat = request.args.get("cat", "").strip()
    
    results = MOVIES_DB
    if cat:
        results = [m for m in results if m["category"] == cat]
    if q:
        results = [m for m in results if q in m["title"] or q in m["description"]]
        
    heading = f"نتائج البحث: {q}" if q else (f"قسم: {cat}" if cat else "🎥 أحدث الأفلام والوثائقيات المختارة")
    content = f"<h2>{heading}</h2>"
    
    if not results:
        content += "<p>لا توجد نتائج مطابقة لبحثك.</p>"
    else:
        content += "<div class='grid'>"
        for m in results:
            content += f"""
            <div class="card">
              <a href="/watch/{m['id']}">
                <img class="thumb" src="{m['thumb']}" alt="{m['title']}">
                <div class="info">
                  <span class="badge">{m['category']}</span>
                  <h3>{m['title']}</h3>
                  <div class="meta">📅 {m['year']} | 🎬 {m['creator']}</div>
                </div>
              </a>
            </div>
            """
        content += "</div>"
    return HTML_HEADER + content + HTML_FOOTER

@app.route("/watch/<movie_id>")
def watch(movie_id):
    movie = next((m for m in MOVIES_DB if m["id"] == movie_id), None)
    if not movie:
        return HTML_HEADER + "<h2>الفيلم غير موجود</h2><a href='/' class='btn'>العودة</a>" + HTML_FOOTER
        
    content = f"""
    <div class="player-box">
      <iframe class="video-frame" src="{movie['embed_url']}" allowfullscreen></iframe>
      <div class="details">
        <span class="badge">{movie['category']}</span>
        <h1>{movie['title']}</h1>
        <div class="meta">📅 سنة الإنتاج: {movie['year']} | 🎬 المخرج/المصدر: {movie['creator']}</div>
        <p>{movie['description']}</p>
        <a href="/" class="btn" style="background:#333;">← العودة للقائمة</a>
      </div>
    </div>
    """
    return HTML_HEADER + content + HTML_FOOTER

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
