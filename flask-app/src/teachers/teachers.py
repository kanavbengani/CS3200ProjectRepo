from flask import Blueprint, request, jsonify, make_response
import json
from src import db


teachers = Blueprint('students', __name__)
