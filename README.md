# PizzaShop
A simple pizzeria site. 
Authorized users can edit their profile info and choose pizzas. 
Superusers can also add pizzas and edit them.

#### Getting the code
```
> git clone https://github.com/seraya-ov/pizza
```

#### Running

Installing python requirements and running the app.

```
> cd pizza
> pip install -r requirements.txt
> python manage.py makemigrations
> python manage.py migrate
> python manage.py runserver

```
Now you can access the project running on `localhost:8000/`.
