book_wish_list 
By Erik Enderlein
---
### Description

Flask micro api for running storing books, users, and their wishlists of books.

Deployed api link:
http://book-wish-list.herokuapp.com/

Deployed swagger docs:
http://book-wish-list.herokuapp.com/swagger/

### Setup and running localhost
requirements:
docker
docker-compose

Clone the repo to a local environment. 

run this command:
./scripts/run

The swagger docs will be available at this url:
http://127.0.0.1:5678/swagger/

### Run tests

run this command:
./scripts/run_tests


Both of these commands involve the use of environmental secrets, which are normally gitignored, and not stored in github. However, as this is a demo project, the secrets for the database have been intentionally pushed, for ease of use, and so I do not need to transfer the secrets to anyone wishing to run the app or tests locally.



## Design and Technology choices
### Technology choices:

* Flask: I decided to use flask (with flask restplus) as the core framework for this project. This is in large part because the scope of the project is small, and thus, a lightweight framework that is easy to spin up and develop is most ideal. I also chose flask because I am extremely confident and familiar with it, which me to focus more on the technology of the project that I was not as familiar with (sqlalchemy). 

* sqlalchemy: At my current workplace, we have an internal system for handling sql queries in python, which I have grown accustomed to. I used sqlalchemy a little bit while in school, but do not have a strong recollection of how it worked from back then. I saw this project as an excellent opportunity to experiment with an unfamiliar technology for managing database models without writing any of my own sql. Aside from my own personal growth, sqlalchemy was a strong choice for this, as the scope of the project called for two tables with a many-to-many relationship, something that falls very easily into sqlalchemy's toolkit. The application of the tool to the project ended up being very simple and intuitive.

* gunicorn: This is my one of my favorite WSGI servers, as it is easy to configure and use, works great with flask, and scales much better and more smoothly than flask's built in run server. It is a natural choice for deploying small flask web-apps.

* heroku: I deployed with heroku because it is an easy to use, free service that let me spend less time on the devops side of the work and more on actually coding my project. While I am familiar with AWS and kubernetes, AWS will really quickly transition to charging money if you are not careful (not ideal for a little demo project) and kubernetes seemed way too overkill for what the scope of this project required.

* docker: I don't like taking any chances with my code and deployments, and docker is great for letting me circumvent all risks of the oh so common "but it worked on my computer!" issue. The localhost run script, test script, and heroku deployment all make use of docker, so that the code runs the same way, no matter where it is, every time.

* postgres: My go-to database system. It has an easy to use extension in heroku, and I'm already very familiar with its specific sql syntax, which made debugging and understanding database happenings easy.

* pytest: A staple testing framework for python. Works great with flask. No reason not to use it!


### Design choices:
I tried to keep my code as modular as humanly possible, in separating out all of the systems into their own separate places, which kept the code clean, document size small, and confusion low.

Sqlalchemy is conducive to creating a separate model page for each of its models, which was a clear choice for Users and Books. I initially created a 'models' folder to house them, but that be came not 'entirely' true when I also created the wishlist table. I thus renamed the folder to 'tables' to better represent that each folder within represented a different one of the three tables in the database.

With the two primary models, it only made sense to keep them both in their own individual controller folders. Flask restplus' 'namespace' system made that extremely easy, and allowed for the industry standard api routing of '<BASE_URL>/<MODEL_TYPE>/<ID>' to naturally occur in my code without any need for coercing. 

For the sake of cleaner code, I separated helper functions and parsers into different files, so they could be easily imported and used where needed. 

I chose to have all of my responses the api makes to the user be through the single api_response function. This way, all of my responses are always consistent, and if I ever have reason to change the formatting of the responses, changing it there will edit all responses for the entire app, saving me the effort of hunting down every endpoint's return statement.

I made heavy use of decorators for this project, as I see them as a clean and reliable way to add common logic to my functions, without having to deal with lots of excess code, or myriad callstack issues. The error_wrapper decorator allowed me to capture all of the possible errors in one place. This allowed for smooth development, as all of my bug fixing stack traces took me to the same place. It also allowed for clean and readable code, as I don't need to program in error handling into any individual function, since it has them all covered. 

Once I got the auth system working for the first view, it was a similarly natural choice to put it into a decorator, so that all user views that require auth would have it built in. 

I decided to implement swagger documentation on the api because, at my work, we use many apis that do and do not have swagger. And the ones with swagger are a LOT easier to use.

I decided to deploy my application partly as a means of showing that I was comfortable with docker->deployment pipelines, and partly as risk prevention. Having a deployed site of my app that I can verify works removes the disastrous consequences the localhost app crashing/not starting when I am trying to show this project to people.
