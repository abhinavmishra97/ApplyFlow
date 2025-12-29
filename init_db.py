"""
Database initialization script
Run this after configuring your .env file
"""

from app import create_app, db
from app.models import User, Campaign, Company, EmailLog, RateLimit

def init_database():
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Verify tables
        print("\nVerifying tables...")
        tables = db.engine.table_names()
        print(f"✓ Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
        
        print("\n✓ Database initialization complete!")
        print("\nNext steps:")
        print("1. Run: python run.py (to start Flask server)")
        print("2. Run: celery -A celery_worker.celery worker --loglevel=info --pool=solo")
        print("3. Open: http://localhost:5000")

if __name__ == '__main__':
    init_database()
