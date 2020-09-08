# minesweeper

Django project implementing a rest api and an user interface for a minesweeper game.

The user interface for playing the game is implemented in reactjs in a diferent repo:

    https://github.com/kverdecia/minesweeper_react

User registration views are implemented as normal django views.

A demo of the application is published in:

    https://minesweeper.kavosoft.com/

The logic of the game is implemented in minesweeper.minesweeper.Board.

Boards are serialized on the model Board.

TODO: Timetracking

## Api endpoints

* GET /api/v1/boards/:
    Returns a list of boards created by the user.
* POST /api/v1/boards/:
    Create a board. You must pass an object similar to {"rows": 10, "columns": 10, "mines": 14}
* GET /api/v1/boards/{boardId}/: Returns the board.
* PUT /api/v1/boards/{boardId}/: Modifies the board. Use it to mark or reveal a cell. In both cases you need to pass the row and column of the cell and the operation name. For example:

    * {"row": 0, "column": 4, "operation": "mark_cell"}
    * {"row": 3, "column": 1, "operation": "reveal_cell"}
* DELETE /api/v1/boards/{boardId}/: Deletes the board.

NOTE: Right now you can only use basic authentication to call the endpoints.

You can access to the api documentation in this urls:

* /swagger.yaml
* /swagger.json
* /swagger/
* /redoc/

## Models

The model Board in the minesweeper application provides the storage and logic to play with a mine sweeper board. To create an instance of this model class you have to pass the rows, columns and mines count and it will generate a random board. Then you can use the methods:

* mark_cell: marks a cell and save the model.
* reveal_cell: reveals a cell and save the model.
* display_board: returns a board object that can be used to create a visual representation of the board.

NOTE: this methods depends on the class minesweeper.Board in the same application in the project.
