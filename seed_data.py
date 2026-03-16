import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Add students
s1 = models.Student(name="Alice", email="alice@test.com")
s2 = models.Student(name="Bob", email="bob@test.com")
s3 = models.Student(name="Charlie", email="charlie@test.com")
db.add_all([s1, s2, s3])

# Add topics
t1 = models.Topic(title="Universal Basic Income", category="social")
t2 = models.Topic(title="Climate Change Regulations", category="political")
t3 = models.Topic(title="Healthcare Reform", category="social")
db.add_all([t1, t2, t3])
db.commit()

# Add results
r1 = models.Result(topic_id=t1.id, total_votes=0)
r2 = models.Result(topic_id=t2.id, total_votes=0)
r3 = models.Result(topic_id=t3.id, total_votes=0)
db.add_all([r1, r2, r3])

# Add rounds
ro1 = models.Round(topic_id=t1.id, round_number=1)
ro2 = models.Round(topic_id=t2.id, round_number=1)
ro3 = models.Round(topic_id=t3.id, round_number=1)
db.add_all([ro1, ro2, ro3])

db.commit()
db.close()

print("Database seeded completely!")
