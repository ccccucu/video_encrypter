from flask import Flask, Blueprint, views
from app.handler.users import *
from app.handler.confs import *
from app.handler.tasks import *
from app.handler.news import *
from app.handler.files import *
from app.handler.pdf_render import *
from app.handler.template import *
from app.handler.home_page import *