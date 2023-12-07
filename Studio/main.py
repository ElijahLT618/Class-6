from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'studiotemplates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True 

terrible_movies = [
    "Sherk 2",
    "Pitch Perfect",
    "Paul Blart: Mall Cop 1/2",
    "Coraline",
    "Look Who's Talking Now"
]

def get_current_watchlist():
   
    return [ "Star Wars", "Lord of The Rings", "Friday", "Paul" ]

def get_watched_movies():
 
    return [ "Forest Gump", "Hot Fuzz", "Renfield" ]

@app.route("/rating-confirmation", methods=['POST'])
def rate_movie():
    movie = request.form['movie']
    rating = request.form['rating']

    if movie not in get_watched_movies():
    
        error = "'{0}' is not in your Watched Movies list, so you can't rate it!".format(movie)

        return redirect("/?error=" + error)

    return render_template('rating-confirmation.html', movie=movie, rating=rating)


@app.route("/ratings", methods=['GET'])
def movie_ratings():
    return render_template('ratings.html', movies = get_watched_movies())


@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    if crossed_off_movie not in get_current_watchlist():

        error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)

        return redirect("/?error=" + error)

    return render_template('crossoff.html', crossed_off_movie=crossed_off_movie)


@app.route("/add", methods=['POST'])
def add_movie():

    new_movie = request.form['new-movie']

    if (not new_movie) or (new_movie.strip() == ""):
        error = "Please specify the movie you want to add."
        return redirect("/?error=" + error)

    if new_movie in terrible_movies:
        error = "Trust me, you don't want to add '{0}' to your Watchlist".format(new_movie)
        return redirect("/?error=" + error)

    new_movie_escaped = cgi.escape(new_movie, quote=True)

    return render_template('add-confirmation.html', movie=new_movie)


@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('edits.html', watchlist=get_current_watchlist(), error=encoded_error and cgi.escape(encoded_error, quote=True))

app.run()