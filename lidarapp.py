import sqlalchemy as sa
import sqlalchemy.orm as so

from  app import app, db

from app.models import User, Post, Experiment, MeasurementCh1, MeasurementCh2

@app.shell_context_processor
def make_shell_context():
  return {'sa': sa, 'so': so, 'db': db, 'User': User, 
          'Post': Post, 'Experiment':Experiment,
          'MeasurementCh1':MeasurementCh1,
          'MeasurementCh2':MeasurementCh2}



