# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Getting Started
### Installing Dependencies

Developers should have Python3, pip3, node, and npm installed. 

### Frontend dependencies
#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Find and download Node and npm (which is included) at: [https://nodejs.com/en/download](https://nodejs.org/en/download/).

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```
### Backend Dependencies 

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
``` 

## API Reference

### Error Handling
Errors are returned in the following json format:
```
{
    'success': False,
    'error': 404,
    'message': ' Not found.'
}
```
The API returns 4 types of errors:
- 400: bad request
- 404: not found
- 422: unprocessable
- 405: method not allowed

### Endpoints

##### GET '/categories'
- Returns a list of categories, success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Example: ```curl http://127.0.0.1:5000/categories```
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```
##### GET '/questions'
- Returns list of questions, categories and paginate in groups of 10
- Example: ```curl http://127.0.0.1:5000/questions```
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_page": "1 of 3",
    "total_questions": 22
}
```
##### GET '/questions?page=${page_num}'
- Paginate to the next page by passing page number
- Example: ```curl http://127.0.0.1:5000/questions?page=2``
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "Ronaldo",
            "category": 4,
            "difficulty": 4,
            "id": 24,
            "question": "best player in the world"
        },
        {
            "answer": "Ronaldso",
            "category": 4,
            "difficulty": 4,
            "id": 25,
            "question": "best player in the world"
        }
    ],
    "success": true,
    "total_page": "2 of 3",
    "total_questions": 22
```
##### DELETE '/questions/int:id'
- Deletes selected question by id
- Example: ```curl -X DELETE http://127.0.0.1:5000/questions/32```
```
{
    "deleted_question": 32,
    "success": true
}
```

##### POST '/questions'
- Create a new question. The new question must have all four information. 
- Example: ```curl -X POST - H "Content-Type: application/json" -d '{"question": "Who invented the personal computer?", "answer": "Steve Wozniak",  "category": "4", "difficulty": 2}' http://127.0.0.1:5000/questions```
- Created question:
```
{
    "question":"Who invented the personal computer?",
    "answer":"Steve Wozniak",
    "category": 4,
    "difficulty": 2
}
```
- JSON response
```
{
    "created": 26,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_page": "1 of 3",
    "total_questions": 21
}

```

##### POST '/questions/search'
- Search for a question using the submitted search term
- Returns a JSON object with paginated questions matching the search term
- Example: ```curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Who invented the personal computer?"}' http://127.0.0.1:5000/questions/search```

```
{
    "questions": [
        {
            "answer": "Steve Wozniak",
            "category": 1,
            "difficulty": 2,
            "id": 33,
            "question": "Who invented the personal computer?"
        }
    ],
    "success": true,
    "total_page": "1 of 1",
    "total_questions": 1
}
```

##### GET '/categories/int:id/questions'
- Get questions only in a specific category
- Example: ```curl http://127.0.0.1:5000/categories/4/questions```

```
{
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "Ronaldo",
            "category": 4,
            "difficulty": 4,
            "id": 24,
            "question": "best player in the world"
        },
        {
            "answer": "Ronaldso",
            "category": 4,
            "difficulty": 4,
            "id": 25,
            "question": "best player in the world"
        },
        {
            "answer": "Ronaldso",
            "category": 4,
            "difficulty": 4,
            "id": 26,
            "question": "best player in the world"
        }
    ],
    "success": true,
    "total_page": "1 of 1",
    "total_questions": 7
}
```

##### POST '/quizzes'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Example: ```curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [15], "quiz_category": {"type": "Geography", "id": "3"}}' http://127.0.0.1:5000/quizzes```
```
{
    "question": {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    "success": true
}
```
## Author and Acknowledgement
- The project and other files are credicted to [Udacity](https://www.udacity.com/)
Footer
© 2022 GitHub, Inc.