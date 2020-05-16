This project is a code generator for Laravel ^7.x.

The main purpose of this code generator is simplify the repeatitive operations involve in the setup.
This project generate simple code for:
<br>
<br>
->Models
<br>
->Controllers
<br>
->Views
<br>
->Components (optional and it works with Vuejs)
<br>
<br>
In the init.py you define the project config, the database config and the structure that you want to use. 
To define models, controllers, and views you have to create a dictionary with the fields, features, constraints.
In order to setup you have to run the python script "python ./init.py". 
<br>
<br>
If you run the example code "init.py" it creates a project named "Test" including Vuejs and basically is an app which create posts and users using Ajax.
