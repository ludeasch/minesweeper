# Game API
This is the documentation related to how to use the game APIs.

## New Board
Endpoint to create a new game

**User token authentication required**

*/api/v1/mineswepper/new/*

**Method:** POST

**Parameters:**

Name | description | min values|
------ | ------ |------ |
`rows` | int  | 9
`columns` |int | 9
`mines`	|int	| 1
`title`	|string	| -


**Returns:** json game object

**Example:**
```python
	{
		'id': 2, 
		'date_added': '2021-02-19T19:29:52.302559Z',
		'title': 'test board',
		'updated': '2021-02-19T19:29:52.302581Z',
		'state': 0, 
		'duration_seconds': 0,
		'total_duration_seconds': 0
	}
```


## List Boards
Endpoint to list all games that was created for the current  user logged 

**User token authentication required**

*/api/v1/mineswepper/*

**Method:** GET

**Returns:** json list of games

**Example:**
```python
	[
		{
			'id': 2, 
			'date_added': '2021-02-19T19:29:52.302559Z',
			'title': 'test board',
			'updated': '2021-02-19T19:29:52.302581Z',
			'state': 0, 
			'duration_seconds': 0,
			'total_duration_seconds': 0
		},
		...
	]
```


## Get Board
Endpoint to return a especific game.

**User token authentication required**

*/api/v1/mineswepper/game/{ID}/*

**Method:** GET

**Parameters:**

name | description |
------ | ------ |
`ID` | id of the game instance  | 

**Returns:** json game object

**Example:**
```python
	{
		'id': 1,
		'date_added': '2021-02-19T19:42:51.219345Z',
		'title': 'title',
		'updated': '2021-02-19T19:42:51.219379Z',
		'board_view': 
			[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
			 ],
		'state': 0, 
		'duration_seconds': 0,
		'total_duration_seconds': 0
	}

```

## Click Board
Endpoint to handler the click event.

**User token authentication required**

*/api/v1/mineswepper/game/{ID}/click_box/*

**Method:** POST

**Parameters:**

name | description | min values|
------ | ------ | ------ |
`click_type` | string | 'reveal', 'flag', 'question' |
`x` | int  | 0
`y` | int  | 0

**Returns:** json game object

**Example:**
```python
	{
		'id': 1,
		'date_added': '2021-02-19T19:42:51.219345Z',
		'title': 'title',
		'updated': '2021-02-19T19:42:51.219379Z',
		'board_view': 
			[['!', '?', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
			 ],
		'state': 0, 
		'duration_seconds': 0,
		'total_duration_seconds': 0
	}

```
## Change state
Endpoint to change the game state. You can just change the state between pause and start

Name | description | min values|
------ | ------ |------ |
`new`  | int | 0 |
`start` | int  | 1
`paused` |int | 2
`won`	|int	| 4
`lose`	|int	| 5

**User token authentication required**

*/api/v1/mineswepper/game/{ID}/set_state/*

**Method:** POST

**Parameters:**

name | description | min values|
------ | ------ | ------ |
`state` | int | 1 or 2 |

**Returns:** json game object

**Example:**
```python
	{
		'id': 1,
		'date_added': '2021-02-19T19:42:51.219345Z',
		'title': 'title',
		'updated': '2021-02-19T19:42:51.219379Z',
		'board_view': 
			[['!', '?', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
			 ],
		'state': 2, 
		'duration_seconds': 21,
		'total_duration_seconds': 213213
	}

```
