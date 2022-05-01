from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
    session,
    abort,
    flash,
    g,
)
import sqlite3
from flask_bcrypt import Bcrypt

DATABASE = "couterra.db"
TABLE = "User"

app = Flask(__name__)
app.secret_key = b"secretkey"

bcrypt = Bcrypt(app)


def get_db():
    db = getattr(g, "database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute(
            """create table if not exists {} (
            username TEXT PRIMARY KEY, 
            password TEXT, 
            firstName TEXT, 
            lastName TEXT)""".format(
                TABLE
            )
        )
    db.row_factory = make_dicts
    return db


def make_dicts(cursor, row):
    print("Make_dicts", "Cursor:", cursor.description, "row:", row)
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def query_db(query, args=(), one=False):
    print("Query value:", query, "Args value:", args)
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ethical-brands")
def ethicalbrands():
    sql_names = """
    SELECT company_name
    FROM couterra
    ORDER BY company_name ASC
    """
    sql_countries = """
    SELECT country
    FROM couterra
    ORDER BY company_name ASC
    """
    sql_cities = """
    SELECT city
    FROM couterra
    ORDER BY company_name ASC
    """
    sql_websites = """
    SELECT website
    FROM couterra
    ORDER BY company_name ASC
    """
    names = query_db(sql_names)
    countries = query_db(sql_countries)
    cities = query_db(sql_cities)
    websites = query_db(sql_websites)
    return render_template("ethical-brands.html",
                        company_names=names,
                        all_countries=countries,
                        all_cities=cities,
                        all_websites=websites)  


@app.route("/fashion-exchange")
def fashionexchange():
    return render_template("fashion-exchange.html")


@app.route("/contact", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        msg = request.form["message"]
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO feedback(name, email, message) VALUES (?,?,?)",
                [name,email,msg],
            )
            db.commit()
        except sqlite3.InterfaceError as err:
            flash("Feedback not added.")
    return render_template("contact.html")


@app.route("/find")
def find():
    sql_photos = """
    SELECT photo
    FROM post
    ORDER BY brand ASC
    """
    sql_emails = """
    SELECT email
    FROM post
    ORDER BY brand ASC
    """
    sql_brands = """
    SELECT brand
    FROM post
    ORDER BY brand ASC
    """
    sql_sizes = """
    SELECT size
    FROM post
    ORDER BY brand ASC
    """
    sql_conditions = """
    SELECT condition
    FROM post
    ORDER BY brand ASC
    """
    sql_extras = """
    SELECT extra
    FROM post
    ORDER BY brand ASC
    """
    photos = query_db(sql_photos)
    emails = query_db(sql_emails)
    brands = query_db(sql_brands)
    sizes = query_db(sql_sizes)
    conditions = query_db(sql_conditions)
    extras = query_db(sql_extras)
    return render_template("find.html",
                        all_photos=photos,
                        all_emails=emails,
                        all_brands=brands,
                        all_sizes=sizes,
                        all_conditions=conditions,
                        all_extras=extras)  


    return render_template("find.html")


@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        photo = request.form["photo"]
        email = request.form["email"]
        brand = request.form["brand"]
        size = request.form["size"]
        condition = request.form["condition"]
        extra = request.form["extra"]
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO post(photo, email, brand, size, condition, extra) VALUES (?,?,?,?,?,?)",
                [photo,email,brand,size,condition,extra],
            )
            db.commit()
        except sqlite3.InterfaceError as err:
            flash("Item not posted.")
    return render_template("post.html")


if __name__ == "__main__":
    app.run(debug=True)
