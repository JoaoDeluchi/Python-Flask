# API Documentation

### Requirements

- Docker
- Docker compose

### Install

To install the dependencies, follow the command below:

`pipenv install`

### Environments
Please set `FLASK_ENV` into your operation system or favorite IDE

See below for values to `FLASK_ENV`:
* testing
* development

Next you need to configure the environment file `.env.development` to start development


########################################################################################################################


• Nestlé's e-commerce Documentation

•   This is a rest-api designed to meet the needs of nestle’s to trade with hbsis.

The chosen language for the back-end of project was:
•	Python

    The main libs and frameworks used were:
        •	Flask (https://flask.palletsprojects.com/en/1.1.x/)
        •	Flask-SQLalchemy (https://flasksqlalchemy.palletsprojects.com/en/2.x/)
        •	Psycopg2 (PostgreSQL database adapter)
        •	Openpyxl (https://openpyxl.readthedocs.io/en/stable/)
        •	Mypy (https://mypy.readthedocs.io/en/stable/)

    The DataBases chosen were:
        •	PostgreSQL
        •	SQLite

    The chosen language for the front-end of project was:
        •	Not defined yet

    How to manage the application:
        •	Firstly you have to create an User
        •	After you have to create a valid Provider
        •	After you have to create a valid Category
        •	After you have to create a valid Product Line
        •	After you have to create a valid Product
    Now you got all the objects that the Project needs to work, you can also import and export them to excel files


########################################################################################################################


Functionalities:

    ••• MODELS:

        Model is a file with a class used to create your database skeleton,
        with sqlalchemy you don't need to create the tables one by one into your SQL IDE.


    • models with "flasksqlalchemy" will be like this:
        Example:
        class Category(db.Model):
            __tablename__ = 'category'

            id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
            name = db.Column(db.String(80))
            profit_percent = db.Column(db.Float(2), default=0.0)
            created_at = db.Column(db.DateTime(timezone=True), default=func.now())
            updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
            is_active = db.Column(db.Boolean, unique=False, default=True)
            deleted_at = db.Column(db.DateTime(timezone=True), default=None)
            product_line = db.relationship('ProductLine', backref='product_line')

        • To create tables you need to use the "__tablename__"  sqlalchemy method.
        • You have to use "db.Column" (from database import db) to create the columns that you need.


    • Validation methods:
        Example:
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            for keys in kwargs:
                if keys == 'id' or keys == 'name':
                    if kwargs[keys] is None or kwargs[keys] == '':
                        raise NullOrNoneValueException()

        • The validation for this class is being done at the "__init__"  method, doing it you can validate your class
          before you instantiate it.
        • In this case we've validated if the field "id" and "name" wasn't duplicated and void or None.


    • Serialize method:
        Example:
        def serialize(self) -> dict:
            return {
                "id": self.id,
                "name": self.name,
                "profit_percent": self.profit_percent,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_active": self.is_active,
                "deleted_at": self.deleted_at
                    }

        • This method was made to serialize the class attributes into a Json dictionary.


    ••• ACTIONS:

        Action is a file that has methods that basically populate the database and do the crud.

    • Create method:
        Example:
        def create(data: dict) -> Category:
            return save(Category(**data))

        • This method was made to create the "Category" and save'em with the save method in repository.py file.
        • Using the unpacking (Category(**data)) trying to make the code cleaner.
        • The create method returns a Category type object.


    • Get methods:
        Examples:
        def get(filters: dict) -> List[Category]:
            return Category.query.filter_by(**filters).all()

        And

        def get_by_id(id: str) -> Category:
            category = Category.query.get(id)
            if category is None:
                raise CategoryDoNotExistException
            return category

        • These methods brings data from a specific place.
        • In this case we've used unpacking with (**filters) to get only the active categories.
        • The get method returns all the filtered objects that the user wants as a list.
        • The "get_by_id" method is almost as same as the "get" method but he bring objects by searching for their id


    • Update method:
        Example:
        def update(id: str, data: dict) -> Category:
            category = get_by_id(id)
            if category.is_active == False:
                raise CategoryInactiveException
            category.name = data.get('name')
            category.profit_percent = data.get('profit_percent')
            commit()
        return category

        • The update method get any category by its id if category is not inactive and after validate it it allows you
            to change the name and profit percent of category(this case).
        • After it this method returns a category with a new name and new profit percent.


    • Delete method:
        Example:
        def delete(id: str) -> NoReturn:
            category = get_by_id(id)
            category.is_active = False
            category.deleted_at = str(datetime.now())
            commit()

        • The delete method get a category by its id and disable it, changing the flag "is_active" to False,
            and saves the date that this category was "deleted".
        • In fact, this method does not delete the category, it remains in the database,
            but the user can no longer see it.


    • Upload method:
        Example:
        def upload_file(file: object) -> List[Category]:
            try:
                excel = ImportExcel(load_workbook(file))
            except:
                raise BadRequestException
            result = excel.read_cells('name', 'profit_percent')
            return [create(category) for category in result if all(category.values()) ,
    ->   and category['name'] not in [categories.name for categories in get({})]]

        • This method import data from an excel file to your database.
        • The try function tries to instantiate the "ImportExcel" class with an workbook that contains a file,
            if this is not possible, an exception is raised
        • If all works perfectly "Upload_File" will return a list with a list comprehension,
            validating if the name of the imported category is already in database.


    • Export method:
        Example:
        def export_file() -> str:
            excel = ExportExcel('categories')
            categories = get({})
            headers = [i for i in categories[0].serialize().keys()]
            headers.remove('id')
            [excel.save_table_sheet(1, i, headers[i - 1]) for i in range(1, len(headers) + 1)]
            row = 2
            for category in categories:
                column = 1
                data_category = category.serialize()
                data_category.pop('id')
                for value in data_category.values():
                    excel.save_table_sheet(row, column, value)
                    column += 1
                row += 1
            return excel.file_name

        • This method as we can see exports data to an excel spreadsheet, removing their id in header,
            cause we don't need it.
        • It serializes the exported category and remove the field and value for "id", and put the requested data into
            the excel format.
        • The return of this method is a brand new excel file with a name as you prefer.


    ••• VIEWS:

        View is a file where you build your http/https routes to do requests.category.

    • Post method:
        Example:
        @app_categories.route('/categories', methods=['POST'])
        def post() -> Tuple[Any, int]:
            payload = request.get_json()
            category = create_category(payload)
            return jsonify(category.serialize()), 201

        • This method is used to send a request to server to create a category ,
        ->   with the valid data that you gave in actions.
        • We have to use annotations to make the url path.
        • Annotation is a way to let explicit what is happening in that code
            and we write it using a "@" and the command needed.
        • Its return is a serialized category in a json format and the http/https code(if valid) as 201 (CREATED).


    • Get methods:
        Example:
        @app_categories.route('/categories', methods=['GET'])
        def get() -> Tuple[Any, int]:
            filters = request.args
            return jsonify([category.serialize() for category in get_category(filters)]), 200


        And:


        @app_categories.route('/categories/<id>', methods=['GET'])
        def get_by_id(id: str) -> Tuple[Any, int]:
            category = get_category_by_id(id)
            return jsonify(category.serialize()), 200


        And

        @app_categories.route('/categories:batchGet', methods=['GET'])
        def batchGet() -> Tuple[Any, int]:
            return send_file(export_file(),
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', True), 200

        • Get methods are all almost the same, so basically they get anything from anywhere,
            whether they use filtered or not.
        • For an example of a get with a filter we have the "get_by_id" method,
            which is given an id to search a category that has the same id that you provide.
        • The return is too a serialized category in json format with a http/https code 200(if the fields are valid).
        • The batchGet method was made to return a excel file from a get request.
        • Annotation is a way to let explicit what is happening in that code
            and we write it using a "@" and the command needed.


    • Put method:
        Example:
        @app_categories.route('/categories/<id>', methods=['PUT'])
        def put(id: str) -> Tuple[Any, int]:
            payload = request.get_json()
            category = update_category(id, payload)
            return jsonify(category.serialize()), 200

        • The PUT method is basically an data updater,
            which fetches data by its id and change the fields that you have permission to change.
        • The return is too a serialized category in json format with a http/https code 200(if the fields are valid).
        • Annotation is a way to let explicit what is happening in that code
            and we write it using a "@" and the command needed.


    • Delete method:
        Example:
        @app_categories.route('/categories/<id>', methods=['DELETE'])
        def delete(id: str) -> Tuple[Any, int]:
            delete_category(id)
            return jsonify(''), 204

        • The delete method just call the method form Actions which actually deletes(inactivate)
            a object as you want.
        • It returns "nothing" and http/https code 204(No Content) if it works
        • Annotation is a way to let explicit what is happening in that code
            and we write it using a "@" and the command needed.


    • As a REST-API you can test your data injection using POSTMAN(or another ide as you prefer),
        with your default route.
    • You can now check in your database if the data was saved.

########################################################################################################################

    ••• DATABASE •••

    • With an import from the python library(from database import db), it can create a session (_session = db.session).

    Repository example:

        from database import db

        _session = db.session


        def save(model: db.Model):
            _session.add(model)
            commit()
            return model


        def commit():
            _session.commit()


    • The save method is used to add a model to a session and save it.
    • The commit function is made to send the data of a session to a database.



••• .env.development •••

     Example of database connection file:
        HOST=localhost
        PORT= "your port here"
        DEBUG=True
        TESTING=False
        FLASK_ENV=development
        API_NAME= "your api name here"
        SECRET_KEY="your secret key here"
        DB_HOST= "your host here"
        DB_PORT= "your db port here"
        DB_USER= "your user here"
        DB_PASSWORD= "your db password here"
        DB_DATABASE= "your db name here"
        SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://${DB_DATABASE}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_DATABASE}
        SQLALCHEMY_TRACK_MODIFICATIONS=True


    • The env.development is a virtual environment which you put the equivalent data to make a database connection.
    • It is writed in bash to execute the connection (FLASK_ENV=development).



••• SETTINGS •••

    Example:
    import os
    from dotenv import load_dotenv

    _dotenv_name = '.env.'
    _env = os.getenv('FLASK_ENV')

    if _env is None or not len(_env):
        _env = 'testing'
    _dotenv_file = os.path.join(os.path.dirname(__file__), _dotenv_name + _env.lower())

    load_dotenv(dotenv_path=_dotenv_file, verbose=True)

    FLASK_APP = 'run'
    FLASK_ENV = _env
    DEBUG = os.getenv('DEBUG', True)
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', True)
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')


    • This module (os) provides a portable way of using operating system dependent functionality.
        Example: os.path.join(os.path.dirname(__file__).
    • The dotenv (.env) module reads the key-value pair from .env file and adds them to environment variable.
        It is great for managing app settings during development and in production using 12-factor principles.


                                                THAT'S ALL FOLKS!
