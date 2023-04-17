from flask import Blueprint, request, jsonify, make_response
import json
from src import db


students = Blueprint('students', __name__)
