from flask import Flask, render_template, request, abort

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

# Content is shared by Flask detail pages and the generated static export.
PROJECT_DETAILS = {
    'gemma': dict(
        repository='GemmaClean', lead='Practice builds confidence. Feedback builds skill.',
        description='An AI-powered mock interview app with voice interaction and personalized spoken feedback. Built for the University of Nevada, Reno’s Biggest Little Hackathon.',
        award='Best Completed Project · 2025',
        specs=[('Platform', 'iOS'), ('Language', 'Swift'), ('Backend', 'Firebase / Firestore'), ('Interaction', 'Voice input & spoken feedback')],
        notes_title='A place to find your voice.',
        notes='Start with the Swift app, then follow the voice input and output workflow and its Firebase integration. GEMMA explores how interview practice can feel more conversational.'),
    'jess': dict(
        repository='JessLangCLI', lead='The tools behind the tools.',
        description='An ongoing exploration of language design: a Swift interpreter with scanning, recursive-descent parsing, abstract syntax tree construction, and tree-walk interpretation. Inspired by Crafting Interpreters.',
        status='In development',
        specs=[('Language', 'Swift'), ('Focus', 'Programming languages'), ('Execution', 'Tree-walk interpreter'), ('Testing', 'XCTest')],
        notes_title='From source to meaning.',
        notes='Trace a piece of source through the scanner, parser, syntax tree, and interpreter. Focus on how each stage turns text into something the next stage can understand.'),
    'sxmpler': dict(
        repository='Sxmpler27', lead='Find the tempo. Unlock the sample.',
        description='An iOS app that detects the musical key and tempo of imported audio. Analysis runs on-device using Apple’s MusicUnderstanding framework, with an interface built in SwiftUI.',
        specs=[('Platform', 'iOS'), ('Interface', 'SwiftUI'), ('Audio', 'AVFoundation / MusicUnderstanding'), ('Concurrency', 'Swift async / await')],
        notes_title='Where music meets software.',
        notes='Follow the flow from importing an audio file to analyzing its key and BPM. Explore how asynchronous analysis updates the SwiftUI interface while keeping the audio on-device.'),
    'swift': dict(
        repository='Swift-Is-MyLife', lead='Learning Swift, one idea at a time.',
        description='A repository documenting my Swift learning journey, with examples covering Swift fundamentals, SwiftUI, and concurrency. A shared resource for learning and helping others along the way.',
        specs=[('Language', 'Swift'), ('Type', 'Learning resource'), ('Topics', 'Fundamentals / SwiftUI / concurrency'), ('Approach', 'Examples & explanations')],
        notes_title='A journal of learning.',
        notes='Choose a topic you’re curious about and work through its examples. This is an ongoing learning resource rather than a single finished application.'),
    'worder': dict(
        repository='Worder', lead='Words, one node at a time.',
        description='A simple trie implementation built with Swift and SwiftUI. A focused project for exploring a tree-shaped data structure for words and prefixes.',
        specs=[('Language', 'Swift'), ('Interface', 'SwiftUI'), ('Data structure', 'Trie'), ('Focus', 'Words & prefixes')],
        notes_title='Discover how words connect.',
        notes='Begin with the trie implementation and follow how words share paths through the structure. Then explore how the SwiftUI interface presents the data.'),
    'converter': dict(
        repository='YenToUSDConverter', lead='A small project. A useful exercise.',
        description='An educational yen-to-US-dollar conversion project built in Swift. A small exercise in expressing a calculation and presenting its result.',
        specs=[('Language', 'Swift'), ('Type', 'Educational project'), ('Conversion', 'Japanese yen → US dollars'), ('Focus', 'Swift fundamentals')],
        notes_title='Follow the calculation.',
        notes='Use this short code tour to follow the conversion calculation and how the result is presented. The project is intended for educational exploration.'),
}
for project in PROJECTS:
    project.update(PROJECT_DETAILS[project['id']])
    project['repository_url'] = 'https://github.com/drecothedev/' + project['repository']

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

    @app.route('/project2/details', defaults={'project_id': 'gemma'})
    @app.route('/project2/details/<project_id>')
    def project2_details(project_id):
        product = next((item for item in PROJECTS if item['id'] == project_id), None)
        if product is None:
            abort(404)
        return render_template('project2/details.html', page='details', product=product)

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
