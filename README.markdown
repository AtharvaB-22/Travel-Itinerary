# Travel Itinerary System for Phuket and Krabi

## What This Project Does
Hi! I built this project to help people plan trips to Phuket and Krabi in Thailand. It’s a simple system that:
- Lets you make new trip plans with a start date and how many days you want to stay.
- Shows you all the trip plans you made.
- Gives you a ready-made plan for 2 to 8 days, with things to do, places to stay, where to eat, and how to get around.
- Recommends a plan based on how many days you want to travel.

I made this using Python and FastAPI, and it stores data in a database called SQLite.

## What You Need to Run This
Before you start, make sure you have these things on your computer:
- Python (I used version 3.11, but 3.8 or higher should work)
- Git (to copy my project)
- A code editor like VS Code

## How to Set It Up
Follow these steps to get the project running on your computer:

1. **Copy the Project**  
   Open your terminal and type this to download my project:
   ```
   git clone <your-repo-url>
   ```
   Replace `<your-repo-url>` with the link to my GitHub repo.

2. **Go to the Project Folder**  
   Move into the project folder by typing:
   ```
   cd Travel-Itinerary-Backend
   ```

3. **Make a Virtual Environment**  
   This keeps the project separate from other things on your computer. Type:
   ```
   python -m venv venv
   ```
   Then turn it on:  
   - On Windows: `venv\Scripts\activate`  
   - On Mac/Linux: `source venv/bin/activate`

4. **Install the Needed Tools**  
   I listed all the tools my project needs in a file called `requirements.txt`. To add them, type:
   ```
   pip install -r requirements.txt
   ```

5. **Set Up the Database**  
   My project uses SQLite to store data. I included a file called `seed.py` that adds some fake trip plans to start with. Run it by typing:
   ```
   python seed.py
   ```
   This will make a database file and add plans for trips from 2 to 8 days.

6. **Start the Project**  
   Now you can run the project! Type this:
   ```
   python main.py
   ```
   It will start a server on your computer at `http://localhost:8000`.

## How to Use the Project
Once the server is running, you can use these links to do different things:
- **Make a New Trip Plan**: Send a POST request to `http://localhost:8000/itineraries` with details like the trip name, start date, and how many days.
  - Example: `{"name": "My Phuket Trip", "start_date": "2023-12-01T00:00:00", "total_nights": 3, "recommended_for_nights": 3}`
- **See All Trip Plans**: Go to `http://localhost:8000/itineraries` to see a list of all plans.
- **Look at One Trip Plan**: Use `http://localhost:8000/itineraries/{id}` to see one plan. Replace `{id}` with the plan’s number, like `1`.
- **Get a Recommended Plan**: Use `http://localhost:8000/recommend/{nights}` to get a plan for a certain number of days. For example, `http://localhost:8000/recommend/2` gives a 2-day plan.
- **Get a Detailed Plan**: Use `http://localhost:8000/itineraries/detailed/{nights}` to see a full plan with things to do, places to stay, where to eat, and how to get around. For example, `http://localhost:8000/itineraries/detailed/3` gives a 3-day plan.

You can test these links using a tool like curl or Postman, or visit `http://localhost:8000/docs` to try them in your browser.

## Files in This Project
Here’s what each file does:
- `main.py`: This is the main file that runs the server and has all the links you can use.
- `models.py`: This has the setup for the database tables, like trips and days.
- `schemas.py`: This makes sure the data you send and get back looks right.
- `itineraries.py`: This has the detailed plans for trips from 2 to 8 days.
- `seed.py`: This adds starting data to the database.
- `config.py`: This has the database settings, like where to find the SQLite file.

## What’s Inside the Plans
The detailed plans for 2 to 8 days include:
- Things to do each day, like visiting beaches or going on tours.
- Places to stay, with options for fancy, normal, and cheap hotels.
- Places to eat, with ideas for local food spots.
- How to get around, like using taxis or boats.

For example, a 2-day plan in Phuket might tell you to visit Patong Beach, eat at a place called Nikita’s, and stay at a hotel like Selina Phuket.

## Problems I Had
- Sometimes the database didn’t save data the right way. I had to check my code and fix the tables to make it work.
- The links were slow at first because I was loading too much data. I changed the code to load things one at a time, and it got faster.

## What’s Next
I want to make this project better later by:
- Adding costs for the trip plans, like how much hotels and food might cost.
- Letting people change the money to their own country’s money, like dollars or euros.
- Making a front page so people can see the plans in a nicer way, not just through links.

**Thanks for checking out my project! If you have any questions, let me know. I hope you like it!**