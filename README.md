# Welcome to AvailabiliCalc

> Nuxt.js + Vuetify.js + Python project

AvailabiliCalc is a piece of software that aims to help the user to estimate the availability of a Data Center (DC) or Private Cloud (PC) from the design stage. It uses Reliability Block Diagrams (RBD) and Continuous Time Markov Chains (CTMC) to achieve it.

All the logic is processed in Python, using [AvailabiliPy](https://github/larrygf/availabilipy)* and the frontend is made using [Vue.js](https://vuejs.org) and [Nuxt.js](https://github.com/nuxt). The cool looking components are made using [Vuetify.js](https://github.com/vuetifyjs/vuetify). The folder structure is the one used by Nuxt, you can find more about this in the [Nuxt documentation](https://nuxtjs.org), so, in case you wanna do some tweaking, you know where to find the components and views. To achieve the communication between the HTML frontend and the Python backend, a small and really useful module named [Eel](https://github.com/ChrisKnott/Eel) was used.
>*The code for AvailabiliPy isn't uploaded yet because it still lacks some finishing touches. You can find the code inside the **availabilipy** folder in this repo. You can tweak it as much as you want since it's still a work in progress. If you have any suggestions or improvements you can write me to my email larrywtf609@gmail.com or fork the project and do it yourself 😄

## Starting the application

You have several ways of running the application, in development mode, as an application using python, and as a native application for your OS. For all of those cases, you'll start by running:

``` bash
#install python dependencies
$ pip install -r requirements.txt
```

This will guarantee that you'll have all the necessary dependencies to run the backend.

### Setting up the development environment

If you only want to mess with the backend, you can skip this part, as you already have all your backend dependencies installed from the previous step. From this point it's all frontend. First you'll need to:

``` bash
# install dependencies
$ npm install # Or yarn install

# serve with hot reload at localhost:3000
$ npm run dev # this step can take a while 
```

That will set the frontend running in port 3000 (if that port is not in use, if it's in use it will pick a random port, stay sharp 😉), if you open your browser you'll see the Welcome screen, but none of the basic functionalities will be available, for that you must start the Python script first:

```bash
# in a different terminal
$ python main.py
```

Having the project running in development mode guarantees that every change you make in the source code will be automatically loaded by your browser. Because of the way Eel works, it will still open a new window with the static view of the page, it's a minor set back, and I will probably try to find a workaround for this in the future.

### Setting up the production environment

#### Launching the application from Python

Assuming you didn't install the dependencies in the previous step, first thing you have to do is:

``` bash
# install dependencies
$ npm install # Or yarn install

# serve with hot reload at localhost:3000
$ npm run build # this step can take a while 
```

Once you have done that, the production webpage will be ready to serve in the **dist** folder. After that the only thing left to do is to run:

```bash
# whenever you want to launch the application
$ python main.py
```

#### Launching it as a native application

>More instructions coming soon

## General Usage

After launching the application you will be greeted with the **Welcome Screen**.

![Welcome screen](/Readme_files/welcome_screen.png)

From here you can either **Start** a new project or **Load** a previously saved one.

### Saving and loading

To **Save** a project you must click on the **blue** button on the top right corner of the screen, it will prompt you to type a name for the file. It will be saved under the **saves** folder of the project.

![Save dialog](/Readme_files/save_dialog.png)

To **load** a previously saved project you must click on the **green** button on the top right corner of the screen. It will output a list of all the saved projects under the **saves** folder on your root directory.

![Load dialog](/Readme_files/load_dialog.png)

### RBD view

The RBD view is the main view of the program, here is where you'll model your system, it gives you all the basic functionalities:

* Adding a block
* Adding a path
* Deleting a block
* Deleting a path
* Set a previously computed availability for a specific block
* "Attach" a CTMC to a block that will be solved giving you the availability for that block
* Find the availability for your system*

![RBD view](/Readme_files/node_rbd.png)

> *You won't be able to solve the system unless all blocks have an availability score.

### CTMC view

The CTMC view is very similar to the RBD view, it gives most of the same functionalities:

* Adding a node
* Adding a transition
* Deleting a node
* Deleting a transition
* Find the availability for the block to which the CTMC is attached to.
* It features a slider that will let you adjust the distance between the nodes to allow for a better visibility.

![CTMC view](/Readme_files/node_chain.png)

### FAQ view

The Frequently Asked Questions view has several common errors, and known bugs in the code. It gives a nice way to check how to do things from inside the application. Downside to this is that updating the FAQ takes time, and I'm really lazy, so it's very possible that changes are made in the code, or bugs are fixed and you can't see it in the FAQ. For a fairly accurate list of changes check the commits from the repo or check if the README.md has changed.

![FAQ view](/Readme_files/FAQ.png)

## Contributing to the project

>Contribution guide coming soon.