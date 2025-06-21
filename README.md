GMap: Graph-to-Map
================
GMap is a system for visualizing graphs as maps.

Basic Setup
--------
      source venv/bin/activate

1. Install the python dependencies listed using pip:

        pip install -r requirements.txt

2. Install [graphviz](http://graphviz.org/Download..php) and [graph-tool](https://graph-tool.skewed.de/)

3. Set up Django settings (optional).
Edit `DATABASES`, `SECRET_KEY`, `ALLOWED_HOSTS` and `ADMINS` in `gmap_web/settings.py`

4. Compile the extranal libraries by running (optional)

        make -C ./external/eba
        make -C ./external/ecba
        make -C ./external/mapsets

5. Create Django databases:

        python3 manage.py makemigrations
        python3 manage.py migrate

6. Run the server:

        python manage.py runserver

7. Access the interface at `http://localhost:8000`

License
--------
Code is released under the [MIT License](MIT-LICENSE.txt).