from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('qaznews.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category_id INTEGER,
        image TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        link TEXT,
        image TEXT
    )''')

    c.execute('SELECT COUNT(*) FROM categories')
    if c.fetchone()[0] == 0:

        categories = ['Политика', 'Спорт', 'Бизнес', 'Фильмы', 'Культура', 'Технологии']
        for cat in categories:
            c.execute('INSERT INTO categories (name) VALUES (?)', (cat,))

        # (category_id, title, content, image_url)
        posts = [
            (1, 'Президент подписал новый закон об образовании',
             'Президент страны подписал новый закон, который кардинально меняет систему образования в стране. Закон предусматривает увеличение финансирования школ на 30 процентов, введение новых обязательных предметов по информационным технологиям и повышение зарплат учителям. Эксперты считают, что это важный шаг для развития всей страны. Реформа затронет более миллиона учеников по всей территории страны. Министерство образования уже начало активную подготовку к внедрению новых стандартов в учебный процесс.',
             'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&q=80'),
            (1, 'Парламент обсуждает государственный бюджет на следующий год',
             'На заседании парламента депутаты подробно обсуждают проект государственного бюджета на следующий финансовый год. Планируется значительное увеличение расходов на здравоохранение и социальную защиту населения. Оппозиция выражает несогласие с рядом ключевых статей расходов. Голосование по бюджету назначено на следующую неделю. Экономисты прогнозируют умеренный рост ВВП при условии принятия данного бюджета.',
             'https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=800&q=80'),
            (2, 'Сборная Казахстана победила в международном турнире',
             'Национальная сборная по футболу одержала уверенную победу в международном турнире, обыграв команду соперников со счётом 3 на 1. Голы в этом матче забили нападающие Нурланов, Сейткали и Байдаулет. Главный тренер команды остался очень доволен игрой своих футболистов. Следующий важный матч пройдёт в следующем месяце. Болельщики на стадионе встретили свою команду громкими овациями.',
             'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800&q=80'),
            (2, 'Казахстанский боксёр завоевал золото на Олимпийских играх',
             'Молодой и талантливый казахстанский боксёр Алибек Джаксыбеков завоевал долгожданную золотую медаль на Олимпийских играх. В финальном захватывающем поединке он победил своего грозного соперника по очкам. Это уже третья золотая медаль Казахстана на этих играх. Спортсмен от всего сердца поблагодарил своих тренеров и любимую семью за постоянную поддержку.',
             'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=800&q=80'),
            (3, 'Казахстанские компании привлекают крупные иностранные инвестиции',
             'Ряд ведущих казахстанских компаний успешно привлёк иностранные инвестиции на общую сумму более 500 миллионов долларов США. Крупные инвесторы из Европы и Азии активно проявляют интерес к горнодобывающей и энергетической отраслям экономики. Правительство страны создаёт максимально благоприятные условия для ведения бизнеса. Новые совместные проекты создадут тысячи высокооплачиваемых рабочих мест для граждан.',
             'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80'),
            (3, 'Фондовый рынок Казахстана показал значительный рост',
             'Казахстанский фондовый рынок зафиксировал существенный рост показателей на 4.5 процента по итогам торговой сессии. Акции крупнейших компаний страны значительно прибавили в своей рыночной цене. Финансовые аналитики связывают этот рост с позитивными макроэкономическими данными. Инвесторы настроены весьма оптимистично относительно перспектив развития рынка.',
             'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80'),
            (4, 'Казахстанский фильм получил престижную международную награду',
             'Художественный фильм известного казахстанского режиссёра Арлана Байсеитова получил главный приз на крупном международном кинофестивале. Эта картина рассказывает о непростой жизни простых людей в бескрайних степях Казахстана. Кинокритики со всего мира высоко оценили профессиональную работу оператора и всех актёров. Фильм выйдет в широкий прокат уже в следующем месяце.',
             'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&q=80'),
            (4, 'В Алматы открылся новый современный кинотеатр',
             'В крупнейшем городе страны Алматы торжественно открылся ультрасовременный кинотеатр с передовой технологией IMAX и системой объёмного звука Dolby Atmos. Первыми фильмами в новом кинотеатре стали самые свежие голливудские блокбастеры. Зрители уже успели высоко оценить потрясающее качество изображения и звука. Кинотеатр рассчитан на одновременный приём 600 посетителей.',
             'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=800&q=80'),
            (5, 'Праздник Наурыз прошёл с большим размахом в Астане',
             'Традиционный весенний праздник Наурыз был отмечен масштабными народными гуляниями в столице страны. На центральной площади города выступили народные ансамбли и современные популярные артисты. Для всех желающих было приготовлено традиционное угощение — вкусное наурыз-коже. Тысячи горожан с радостью приняли участие в праздновании. Мероприятие объединило людей совершенно разных поколений.',
             'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800&q=80'),
            (5, 'В Казахстане открылся новый музей современного искусства',
             'В солнечном городе Алматы торжественно открылся Музей современного искусства, где представлены яркие работы казахстанских и зарубежных художников. Богатая коллекция музея насчитывает более 500 уникальных экспонатов разных жанров. Особый интерес у посетителей вызывает специальный зал интерактивных инсталляций. Музей уже стал важнейшим культурным центром всего города.',
             'https://images.unsplash.com/photo-1578926375605-eaf7559b1458?w=800&q=80'),
            (6, 'Казахстан запускает национальную программу цифровизации',
             'Правительство Казахстана официально объявило о запуске масштабной государственной программы цифровизации всей экономики и государственных услуг. В рамках этой программы планируется постепенно перевести большинство госуслуг в удобный онлайн-формат. Общий бюджет программы составляет 1 триллион тенге. Реализация данной программы рассчитана на пять лет вперёд.',
             'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80'),
            (6, 'Казахстанские IT-специалисты создали инновационный стартап',
             'Группа молодых и амбициозных казахстанских программистов создала перспективный стартап в области искусственного интеллекта, который уже привлёк серьёзное внимание международных инвесторов. Разработанный продукт помогает малому бизнесу эффективно автоматизировать рутинные задачи. Первоначальные инвестиции в проект составили 2 миллиона долларов США. Команда активно планирует выйти на международный рынок уже в этом году.',
             'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&q=80'),
        ]

        for cat_id, title, content, image in posts:
            c.execute('INSERT INTO posts (category_id, title, content, image) VALUES (?, ?, ?, ?)',
                      (cat_id, title, content, image))

        # (title, description, link, image_url)
        ads_data = [
            ('Samsung Galaxy S24', 'Новейший смартфон уже в продаже! Закажи сейчас.', '#',
             'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=600&q=80'),
            ('Kaspi Bank', 'Кредит онлайн за 5 минут. Без залога и поручителей.', '#',
             'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600&q=80'),
            ('Новые квартиры в Алматы', 'Купи квартиру мечты от 25 млн тенге!', '#',
             'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600&q=80'),
            ('Beeline Казахстан', 'Самый быстрый интернет по всей стране!', '#',
             'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&q=80'),
            ('Halyk Bank', 'Откройте вклад и получайте до 14% годовых.', '#',
             'https://images.unsplash.com/photo-1601597111158-2fceff292cdc?w=600&q=80'),
            ('Air Astana', 'Летайте с нами! Лучшие цены на авиабилеты.', '#',
             'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=600&q=80'),
        ]
        for title, desc, link, image in ads_data:
            c.execute('INSERT INTO ads (title, description, link, image) VALUES (?, ?, ?, ?)',
                      (title, desc, link, image))

    conn.commit()
    conn.close()


# Главная страница — index.html
@app.route('/')
def index():
    conn = get_db()

    latest_posts = conn.execute('''
        SELECT p.id, p.title, p.content, p.image, p.created_at, c.name as category_name
        FROM posts p
        JOIN categories c ON p.category_id = c.id
        ORDER BY p.created_at DESC
        LIMIT 4
    ''').fetchall()

    all_posts = conn.execute('''
        SELECT p.id, p.title, p.content, p.image, p.created_at, c.name as category_name
        FROM posts p
        JOIN categories c ON p.category_id = c.id
    ''').fetchall()

    all_posts_list = list(all_posts)
    random_count = min(6, len(all_posts_list))
    random_posts = random.sample(all_posts_list, random_count)

    all_ads = list(conn.execute('SELECT * FROM ads').fetchall())
    ads = random.sample(all_ads, min(4, len(all_ads)))

    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()

    return render_template('index.html',
                           latest_posts=latest_posts,
                           random_posts=random_posts,
                           ads=ads,
                           categories=categories)


# Все новости — all-news.html
@app.route('/all-news')
def all_news():
    conn = get_db()

    posts = conn.execute('''
        SELECT p.id, p.title, p.content, p.image, p.created_at, c.name as category_name
        FROM posts p
        JOIN categories c ON p.category_id = c.id
        ORDER BY p.created_at DESC
    ''').fetchall()

    all_ads = list(conn.execute('SELECT * FROM ads').fetchall())
    ads = random.sample(all_ads, min(4, len(all_ads)))

    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()

    return render_template('all-news.html', posts=posts, ads=ads, categories=categories)


# Чтение постов — read-news.html
@app.route('/read-news/<int:post_id>')
def read_news(post_id):
    conn = get_db()

    post = conn.execute('''
        SELECT p.id, p.title, p.content, p.image, p.created_at, p.category_id, c.name as category_name
        FROM posts p
        JOIN categories c ON p.category_id = c.id
        WHERE p.id = ?
    ''', (post_id,)).fetchone()

    related_posts = conn.execute('''
        SELECT p.id, p.title, p.content, p.image, p.created_at, c.name as category_name
        FROM posts p
        JOIN categories c ON p.category_id = c.id
        WHERE p.category_id = ? AND p.id != ?
        ORDER BY RANDOM()
        LIMIT 4
    ''', (post['category_id'], post_id)).fetchall()

    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()

    return render_template('read-news.html', post=post, related_posts=related_posts, categories=categories)


# Новости по категории — news-by-category.html
@app.route('/news-by-category/<int:cat_id>')
def news_by_category(cat_id):
    conn = get_db()

    category = conn.execute('SELECT * FROM categories WHERE id = ?', (cat_id,)).fetchone()

    posts = conn.execute('''
        SELECT p.id, p.title, p.content, p.image, p.created_at, c.name as category_name
        FROM posts p
        JOIN categories c ON p.category_id = c.id
        WHERE p.category_id = ?
        ORDER BY p.created_at DESC
    ''', (cat_id,)).fetchall()

    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()

    return render_template('news-by-category.html', posts=posts, category=category, categories=categories)


# Страница поиска — search.html
@app.route('/search')
def search():
    categories = get_db().execute('SELECT * FROM categories').fetchall()
    return render_template('search.html', categories=categories)


# Результаты поиска — search-results.html
@app.route('/search-results')
def search_results():
    query = request.args.get('q', '').strip()

    conn = get_db()
    posts = []

    if query:
        posts = conn.execute('''
            SELECT p.id, p.title, p.content, p.image, p.created_at, c.name as category_name
            FROM posts p
            JOIN categories c ON p.category_id = c.id
            WHERE p.title LIKE ? OR p.content LIKE ?
            ORDER BY p.created_at DESC
        ''', (f'%{query}%', f'%{query}%')).fetchall()

    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()

    return render_template('search-results.html', posts=posts, query=query, categories=categories)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
