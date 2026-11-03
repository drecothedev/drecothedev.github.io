from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')
@app.route("/a2")
def hello_World():
    return render_template('a2/activity2.html')
@app.route("/a4")
def hello_ass4():
    return render_template('a4/activity4.html')
@app.route("/a5")
def hello_ass5():
    return render_template('a5/activity5.html')
@app.route("/a6")
def hello_ass6():
    return render_template('a6/activity6.html')


@app.route("/a7")
def activity7():
    return render_template("a7/activity7.html")


@app.route("/a8")
def activity8():
    return render_template("a8/activity8.html")


@app.route("/a9")
def activity9():
    return render_template("a9/activity9.html")


@app.route("/project")
def project_home():
    return render_template("project/index.html")


# Milestone 2 stays in this entry point so school deployments need no local imports.
CATEGORIES = [('all', 'All projects'), ('apps', 'iOS apps'), ('languages', 'Languages'), ('learning', 'Learning')]
PROJECTS = [
    dict(id='gemma', number=1, name='GEMMA', category='apps', type='iOS APP', stack='SWIFT / FIREBASE', exploration_minutes=30, image='gemma-360.webp', image_class='app-shot', alt='GEMMA mock interview app screenshot', short='Voice-powered interview practice. A space to prepare, speak, and grow.'),
    dict(id='jess', number=2, name='Jess', category='languages', type='LANGUAGE LAB', stack='SWIFT / INTERPRETERS', exploration_minutes=45, image='jess.svg', image_class='project-art', alt='Illustrative Jess language pipeline artwork', short='An interpreter built in Swift. Exploring the tools behind the tools.'),
    dict(id='sxmpler', number=3, name='Sxmpler', category='apps', type='AUDIO TOOL', stack='SWIFTUI / AUDIO', exploration_minutes=20, image='sxmpler-360.webp', image_class='app-shot', alt='Sxmpler audio analysis app screenshot', short='Find the key and tempo of a song. Music analysis, on-device.'),
    dict(id='swift', number=4, name='Swift Is My Life', category='learning', type='LEARNING JOURNAL', stack='SWIFT / SWIFTUI', exploration_minutes=15, image='swift.svg', image_class='project-art', alt='Illustrative Swift learning journal artwork', short='A shared journal of Swift fundamentals, SwiftUI, and concurrency.'),
    dict(id='worder', number=5, name='Worder', category='apps', type='DATA STRUCTURES', stack='SWIFT / SWIFTUI', exploration_minutes=10, image='worder.svg', image_class='project-art', alt='Illustrative Worder trie data structure artwork', short='A simple trie implementation. Discovering how words connect.'),
    dict(id='converter', number=6, name='Yen to USD', category='apps', type='EDUCATIONAL APP', stack='SWIFT / FUNDAMENTALS', exploration_minutes=5, image='converter.svg', image_class='project-art', alt='Illustrative yen to dollar conversion artwork', short='A small currency conversion project. Built to learn the fundamentals.'),
]

# Dimensions reserve image space before downloads; browsers select a suitable size.
for project in PROJECTS:
    if project['id'] in ['gemma', 'sxmpler']:
        project['image_width'] = 360
        project['image_height'] = 782 if project['id'] == 'gemma' else 739
        project['responsive_image'] = project['id']
    else:
        project['image_width'], project['image_height'] = 900, 700
        project['responsive_image'] = None

def register_project2(app):
    @app.template_filter('duration')
    def duration(value):
        return f'{value:,} min'

    @app.route('/project2')
    def project2_home():
        return render_template('project2/index.html', page='home')

    @app.route('/project2/products')
    def project2_products():
        category = request.args.get('category', 'all')
        if category not in dict(CATEGORIES):
            category = 'all'
        products = [p for p in PROJECTS if category == 'all' or p['category'] == category]
        return render_template('project2/products.html', page='products', products=products,
                               categories=CATEGORIES, category=category, category_label=dict(CATEGORIES)[category])

    @app.route('/project2/details')
    def project2_details():
        return render_template('project2/details.html', page='details', product=PROJECTS[0])

    @app.route('/project2/current-project')
    def project2_current():
        return render_template('project2/current.html', page='current')

    @app.route('/project2/cart')
    def project2_cart():
        items, invalid = [], False
        for product in PROJECTS[:2]:
            raw = request.args.get(product['id'] + '_qty', '1')
            try:
                quantity = int(raw)
                if not 1 <= quantity <= 99:
                    raise ValueError
            except (ValueError, TypeError):
                quantity, invalid = 1, True
            items.append(dict(product, quantity=quantity, row_total=product['exploration_minutes'] * quantity))
        total_minutes = sum(item['row_total'] for item in items)
        return render_template('project2/cart.html', page='cart', cart_items=items,
                               total_minutes=total_minutes,
                               error='Use a whole-number session count from 1 to 99. Invalid counts were reset to 1.' if invalid else None)

register_project2(app)


if __name__ == "__main__":
    app.run(debug=True)
