# Episodes
TV show Episode tracker built using django and bootstrap4.<br/>
Episodes allows you to keep track of your favourite tv shows either continuing or ending and also provide you with recommendations based on your likings using machine learning using libraries like pandas, sci-kit learn, numpy etc.
Using http://thetvdb.com/ for metadata.
Inspired from https://github.com/jamienicol/episodes

Requirements:

 * python 2/3
 * django
 * sklearn
 * requests
 * pandas

To use clone the production branch, install requirements, run the following terminal commands:

    $ sudo pip3 install -r requirements.txt
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    $ python3 manage.py runserver
    
![alt tag](https://raw.githubusercontent.com/guptachetan1997/Episodes/master/1.jpeg)
![alt tag](https://raw.githubusercontent.com/guptachetan1997/Episodes/master/2.jpeg)
![alt tag](https://raw.githubusercontent.com/guptachetan1997/Episodes/master/3.jpeg)
![alt tag](https://raw.githubusercontent.com/guptachetan1997/Episodes/master/4.jpeg)

## Using docker
You can build the image with 

```docker build -t episodes .```

and run it with

```docker run --rm -ti -v YOUR_DIRECTORY_FOR_SQLITE_FILE:/data -p 8000:8000 episodes```

Todo:
* run daemonized
* set timezone/mount settings
* optimize image size
