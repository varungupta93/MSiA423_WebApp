from msiapp import db


# Create a data model for the database to be setup for the app
class Weather(db.Model):
    __tablename__ = "weather"
    Date = db.Column("Date", db.String(30), primary_key=True)
    MeanAppTemp = db.Column(db.Float, unique=False, nullable=False)
    PrecipProb = db.Column("PrecipProb", db.Float, unique=False, nullable=False)
    PrecipIntensity = db.Column("PrecipIntensity", db.Float, unique=False, nullable=True)

    def __repr__(self):
        return '<Weather %r>' % self.title




def __repr__(self):
    return '<Weather %r>' %self.name
