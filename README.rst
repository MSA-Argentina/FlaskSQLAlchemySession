Flask SQLAlchemy Session
========================
This is a Database Session storage interface for Flask with SQLAlchemy

How to use
----------
First you will have to create the sessions table
.. code-block:: sql 
    CREATE TABLE sessions (
      session_id CHAR(129) UNIQUE NOT NULL,
      atime      TIMESTAMP,
      data       TEXT);

Then you will have to connect the interface to your Flask application

.. code-block:: python
    from FlaskSQLAlchemySession import set_db_session_interface
    
    application.config['SQLALCHEMY_DATABASE_URI'] = "[your-sqllchemy-db-uri"
    set_db_session_interface(application)

Requirements
------------
 * Flask
 * Flask-SQLAlchemy

