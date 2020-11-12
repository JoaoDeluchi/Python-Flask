from app.domain.tasks.models import Task
from database.repo import save, commit
from uuid import uuid4
from typing import NoReturn


def create(data):
    return save(Task(id=str(uuid4()), title=data['title']))


def get():
    return Task.query.filter(Task.is_active == True)


def get_by_id(id):
  return Task.query.filter(Task.id == id).first()


def get_by_name(name):
  return Task.query.filter(Task.name == name).first()


def update(id, data):
  task = get_by_id(id)
  task.title = data.get('title')
  commit()
  return task


def delete(id):
  task = get_by_id(id)
  task.is_active = False
  commit()
