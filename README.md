## Minesweeper API
A simple API to give the posiility to play this retro game

## Features

* User token authentication
* Extensively tested and documented
* Ability to 'flag' a cell with a question mark or red flag
* Detect when game is over
* Time tracking
* Ability to start a new game and preserve/resume the old ones
* Ability to select the game parameters: number of rows, columns, and mines
* Ability to support multiple users/accounts


## Install application
Before starting I recommend using virtualenv when installing the dependencies
### Clone repository 
```bash
	git clone https://github.com/ludeasch/minesweeper.git
```
### Install dependencies 
```bash
	cd minesweeper
	pip install -r requirement.txt
```
### Run migrations
```bash
	python manage.py migrate
```
### Run application
```bash
	python manage.py runserver
```

## Documentation

See the [`doc` directory](doc/) for more detailed documentation.

