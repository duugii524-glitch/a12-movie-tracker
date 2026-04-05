# Enter your code here
#Student name: Dulamsuren Selenge

from peewee import *
from datetime import datetime

# Create database
db = SqliteDatabase('movies.db')


# Movie Model
class Movie(Model):
    name = CharField()
    year_released = IntegerField()
    status = CharField(default="Want to watch")
    rating = IntegerField(null=True)

    class Meta:
        database = db

    # Override create method for validation
    @classmethod
    def create(cls, **query):
        year = query.get('year_released')

        current_year = datetime.now().year

        # Validation
        if (
            len(str(year)) != 4 or
            year < 1888 or
            year > current_year
        ):
            print("Movie not saved because of an invalid year. Please provide a valid 4-digit year.")
            return None

        return super().create(**query)

    # Method to display info
    def get_info(self):
        return f"ID: {self.id} | Name: {self.name} | Year: {self.year_released} | Status: {self.status} | Rating: {self.rating}"

    # Method to rate movie
    def rate_movie(self, rating):
        self.status = "Watched"
        self.rating = rating
        self.save()


# Initialize database
db.connect()
db.create_tables([Movie])


# Menu function
def menu():
    print("\nMovie Tracker Menu:")
    print("1. Add a movie to the watchlist")
    print("2. View all movies")
    print("3. Update movie status to 'Watched' and provide a rating")
    print("4. View only watched movies with rating of 4 or above")
    print("5. Delete a movie")
    print("6. Exit")


# Main loop
while True:
    menu()
    choice = input("Choose an option (1-6): ")

    if choice == "1":
        name = input("\nEnter the movie name: ")
        year = int(input("Enter the year released: "))

        movie = Movie.create(name=name, year_released=year)

        if movie:
            print(f"\nMovie '{name}' added to the watchlist.")

    elif choice == "2":
        print()
        for movie in Movie.select():
            print(movie.get_info())

    elif choice == "3":
        movie_id = int(input("\nEnter the ID of the movie you've watched: "))
        rating = int(input("Enter your rating (1-5): "))

        movie = Movie.get_by_id(movie_id)
        movie.rate_movie(rating)

        print(f"\nMovie '{movie.name}' updated to 'Watched' with rating {rating}.")

    elif choice == "4":
        print()
        movies = Movie.select().where(Movie.rating >= 4)

        for movie in movies:
            print(movie.get_info())

    elif choice == "5":
        movie_id = int(input("\nEnter the ID of the movie to delete: "))

        movie = Movie.get_by_id(movie_id)
        name = movie.name
        movie.delete_instance()

        print(f"\nMovie '{name}' deleted successfully.")

    elif choice == "6":
        print("\nGoodbye!")
        break

    else:
        print("Invalid choice. Please choose again.")

