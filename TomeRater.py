"""
IMPROVEMENTS ADDED:
- Error checking:
  - print error if add user email already exists
  - print error if ISBN already exists and request a new one
  - print error if user email invalid and request a new one

- Dunder methods:
  - __repr__ method for Tome_Rater to display summary stats

- Analysis methods:
  - return an ordered list of books and read counts X items long
  - return a user's highest rated book
  - recommend a book to a user based on a similar user's books
"""

class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("User's email updated to " + address)

    def __repr__(self):
        return ("User " + self.name + ", email: " + self.email + ", books read: " + str(len(self.books)))

    def __eq__(self, other_user):
        if (self.email == other_user.email) and (self.name == other_user.name):
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        ratings_list = []
        for rating in self.books.values():
            if rating:
              ratings_list.append(rating)
        average_rating = sum(ratings_list) / len(ratings_list)
        return average_rating


class Book():
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("ISBN updated to " + str(self.isbn))

    def add_rating(self, rating):
        if 0 <= rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid rating")

    def get_average_rating(self):
        return sum(self.ratings) / len(self.ratings)

    def __eq__(self, other_book):
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return (self.title + " by " + self.author)


class Non_fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return (self.title + " a " + self.level + " manual on " + self.subject)


class TomeRater():
  def __init__(self):
    self.users = {}
    self.books = {}
    self.isbns = []

  #Method to avoid duplicate ISBNs
  def check_unique_isbn(self, isbn):
    if isbn in self.isbns:
      print("ISBN already exists: "+str(isbn))
      print("Please enter a new ISBN: ")
      #request a new ISBN
      isbn = int(input())
      self.check_unique_isbn(isbn)
      return True #As a unique ISBN will have been provided
    else:
      #Add the ISBN to the list
      self.isbns.append(isbn)
      return True

  #Method to validate email address, similar to above:
  def validate_email(self, email):
    if '@' not in email or '.' not in email:
      print(email+" is not a valid email. Please provide another: ")
      email = str(input())
      self.validate_email(email)
      return email
    return email

  def __repr__(self):
    return("Tome Rater currently has "+str(len(self.users))+" users and "+str(len(self.books))+" books.")

  def create_book(self, title, isbn):
    #Check to see ISBN doesn't already exist
    if self.check_unique_isbn(isbn) == True:
      return Book(title, isbn)

  def create_novel(self, title, author, isbn):
    #Check to see ISBN doesn't already exist
    if self.check_unique_isbn(isbn) == True:
      return Fiction(title, author, isbn)

  def create_non_fiction(self, title, subject, level, isbn):
    #Check to see ISBN doesn't already exist
    if self.check_unique_isbn(isbn) == True:
      return Non_fiction(title, subject, level, isbn)

  def add_book_to_user(self, book, email, rating=None):
    if email in self.users.keys():
      self.users[email].read_book(book, rating)
      #Added if statement below as sometimes books don't have rating
      if rating:
        book.add_rating(rating)
      if book not in self.books.keys():
        self.books[book] = 1
      else:
        self.books[book] += 1
    else:
      print("No user with email "+email+"!")

  def add_user(self, name, email, user_books=None):
    #check format of email is valid
    email = self.validate_email(email)
    #avoid duplicate emails
    if email in self.users.keys():
      print("A user with email "+email+" already exists.")
    else:
      self.users[email] = User(name, email)
      if user_books:
        for book in user_books:
          self.add_book_to_user(book, email)

#Tome_Rater analysis methods
  def print_catalog(self):
    for book in self.books:
      print(book)

  def print_users(self):
    for user in self.users:
      print(user)

  def most_read_book(self):
    read_count = 0
    most_read_book = None
    for book in self.books:
      if self.books[book] > read_count:
        most_read_book = book
        read_count = self.books[book]
    #print(read_count)
    return most_read_book

  def highest_rated_book(self):
    #start at -1 because books can have a rating of 0
    highest_rating = -1
    highest_rated_book = None
    for book in self.books:
      if book.get_average_rating() > highest_rating:
        #print("current highest: " + str(book))
        highest_rated_book = book
        highest_rating = book.get_average_rating()
    return highest_rated_book

  def most_positive_user(self):
    most_positive_user = None
    highest_average_rating = 0
    for user in self.users:
      if self.users[user].get_average_rating() > highest_average_rating:
        most_positive_user = user
        highest_average_rating = self.users[user].get_average_rating()
    return most_positive_user

  #method to return ordered list of n most read books
  def most_read_books(self, n):
    sorted_list = sorted(self.books, key=self.books.get, reverse=True)
    sorted_list_with_numbers = []
    for book in sorted_list:
      sorted_list_with_numbers.append(str(book) +": "+str(self.books[book]))
    return sorted_list_with_numbers[0:n]

  #method to return a user's highest rated book
  def users_favourite_book(self, email):
    highest_rating = -1
    favourite_book = None
    for book in self.users[email].books:
      #skip unrated books
      if self.users[email].books[book] == None:
        continue
      #Make it the top book if rated higher
      if self.users[email].books[book] > highest_rating:
        highest_rating = self.users[email].books[book]
        favourite_book = book
    return favourite_book

  #method to recommend a book based on favourite book
  #please note to test this you need to add more books to users
  def recommend_book(self, email):
    #get favourite book
    fave_book = self.users_favourite_book(email)
    #find someone else who rated that book highly
    #first make an empty list to store books in
    same_fave_book_list = []
    #Look through all users
    for user in self.users:
      #remove self from list of users
      if user == email:
        continue
      #detect if another user has the same favourite book
      if self.users_favourite_book(user) == fave_book:
        for book in self.users[user].books:
          #skip unrated books
          if self.users[user].books[book] == None:
            continue
          #skip the same favourite book
          if book == fave_book:
            continue
          #Add any other books rated >= 3
          elif self.users[user].books[book] >= 3:
            same_fave_book_list.append(book)
          else:
            continue
      #skip users without the same favorite book
      else:
        continue
    #if the resulting list is not empty (it is True), return it
    if same_fave_book_list:
      return same_fave_book_list
    else:
      return "No recommendations available"
      