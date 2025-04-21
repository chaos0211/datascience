from app import create_app, db
from app.routes.generate_fake_data import generate_fake_data_logic

app = create_app()

with app.app_context():
    generate_fake_data_logic()