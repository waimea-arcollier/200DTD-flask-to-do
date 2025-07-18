#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db import connect_db
from app.helpers.errors import register_error_handlers, not_found_error


# Create the app
app = Flask(__name__)

# Setup a session for messages, etc.
init_session(app)

# Handle 404 and 500 errors
register_error_handlers(app)


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
    with connect_db() as client:
        sql = "SELECT id, name, priority, complete FROM tasks ORDER BY priority desc"
        result = client.execute(sql)
        tasks = result.rows
    return render_template("pages/home.jinja", tasks=tasks)


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")


#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add/")
def add_task():
    # Get the data from the form
    name  = request.form.get("name")
    priority = request.form.get("priority")

    # Sanitize the inputs
    name = html.escape(name)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO tasks (name, priority) VALUES (?, ?)"
        values = [name, priority]
        client.execute(sql, values)

        # Go back to the home page
        flash(f"Task '{name}' added", "success")
        return redirect("/")


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_a_thing(id):
    with connect_db() as client:
        # Delete the thing from the DB
        sql = "DELETE FROM tasks WHERE id=?"
        values = [id]
        client.execute(sql, values)

        # Go back to the home page
        flash("Task deleted", "warning")
        return redirect("/")


@app.post("/complete/<int:id>")
def complete_task(id):
    with connect_db() as client:
         # Delete the thing from the DB
         sql = "UPDATE tasks SET complete = 1 WHERE id=?"
         values = [id]
         client.execute(sql, values)

         # # Go back to the home page
         return redirect("/")

@app.post("/uncomplete/<int:id>")
def uncomplete_task(id):
    with connect_db() as client:
         # Delete the thing from the DB
         sql = "UPDATE tasks SET complete = 0 WHERE id=?"
         values = [id]
         client.execute(sql, values)

         # # Go back to the home page
         return redirect("/")

