from flask import Flask, render_template
from peewee import *
from werkzeug.security import generate_password_hash

app = Flask(__name__)
db = SqliteDatabase("project_tracker.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()


class Project(BaseModel):
    title = CharField()
    creator = ForeignKeyField(User, backref="created_projects")


class ProjectStep(BaseModel):
    description = CharField()
    status = CharField(default="TODO")
    project = ForeignKeyField(Project, backref="steps")


class ProjectContributor(BaseModel):
    project = ForeignKeyField(Project)
    contributor = ForeignKeyField(User)


class ProjectComment(BaseModel):
    comment = CharField()
    project = ForeignKeyField(Project, backref="comments")
    comment_creator = ForeignKeyField(User, backref="project_comments")


class StepComment(BaseModel):
    comment = CharField()
    step = ForeignKeyField(ProjectStep, backref="comments")
    comment_creator = ForeignKeyField(User, backref="step_comments")


@app.route("/")
def homepage():
    return render_template("index.html")


if __name__ == '__main__':
    db.connect()
    db.create_tables([User, Project, ProjectStep, ProjectContributor, ProjectComment, StepComment])
    app.run()
