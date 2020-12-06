<h1 align = "center">Book Soundtrack Creator</h1>
projects-01-book-soundtrack-creator created by GitHub Classroom

## Features
* **Login with Spotify** - Using the Spotify API we are able to request user login to access user data.
* **Session tracking** - Allows each user to have a customized experience by checking for certain primary keys as they navigate through the app.
* **Project Gutenberg Book Search / Selector** - Using the Gutendex API we are able to pull in books from the public domain. This page also gives the user the option to import a book.
* **Spotify Soundtrack creation** - Using the user’s Spotify data and the book’s emotion, a soundtrack can be created for the book.
* **Book emotion creator** - Using sentiment analysis we are able to determine the overall emotion of the book.
* **Book ranking** - Users can vote for their favorite books and the highest voted books go to the popular books page!
* **Profile page / Logout** - Here users can see which Spotify account they are signed into and then logout of Book Soundtrack Creator.

## Testing 

For testing we did mostly manual testing after each new feature. After the code was pushed onto the main branch, we would all go through, run the code and test it's core functionality as well as how it fit into the flow of things. We developed a list on Trello that was for bugs/errors in the program. Django has really good error/debugging pages integrated into it. Once the bug was on the list, whoever was responsible for that section of the code would open the ticket and begin working on it. We repeated this cycle until all of our main functionality was done. Then we launched the app on an AWS webserver, this gave us the ability to send the website to our friends to do rounds of testing. While people used the app we were able to see messages on the terminal of their activity, and any errors that came up. Each user is assigned a user ID when they begin using the app. This ID is printed out with every signifcant status update so that we were able to track the users as the navigated through our app. We did multiple rounds of this kind of testing until we were confident that all bugs had been resolved. Below you can see an example of one of the readouts from the server as two users navigated the sight. 


## Project Overview

## Vision Statement

For avid readers of books who want to dive into the mood of their books, the Book Soundtrack Creator is an application that takes the entered title of a book and creates a playlist that matches the feeling the novel gives off. Unlike other applications that allow you to only create playlists that you think are right for your book, our product provides you with a generated playlist that matches the tone of the book with just the ease of entering the title and hitting create. 

## Personas

Andrew:

Alec, age 34, is a librarian who works for a grade school in the greater Philadelphia area. He keeps track of all books coming in and out of the library, as well as teaching kids, ages 10 to 13, how the library organization system works and about famous books through history. He was born in Washington D.C where both of his parents worked in the Library of Congress, sharing their love of books with him every night. After completing a degree in history at Temple University, he moved to the suburbs of Philadelphia to get his career started. When he gets home, he does all the necessary tasks of an adult in his 30s but when its time to relax, he pulls out his books and starts reading till its time to sleep.

Alec is very connected to the internet and applications to make the library organization much easier, as well as learn more about the books he wants to teach his students about. Alec might use the Book Soundtrack Creator to not only learn more about the mood and tones of the books he likes to read, but to also explain books better to his students through the generated playlists. The use of the application would especially help him understand books he never read before as well, explaining the feeling of the books entered before he even gets to read anything about them.

Jake:

Anthony, age 30, hosts a large YouTube channel and business in which he reviews music, albums, etc. While he is based in NYC his YouTube channel attracts users and music listeners from all over. He was born in Brooklyn where both of his parents were musicians and music teachers. He has a degree in music but does not create/release much of his own music but instead provides commentary on the music industry.

Anthony, who has typically done daily/weekly music analysis videos and album reviews until this point, is now thinking about creating a new series of videos based on the mood/data of music as well as suggesting book recommendations relative to music. Anthony could use Book Soundtrack Creator in multiple ways. He could use it to determine if his initial analysis of a book and music pair is accurate. If he is uncertain of what music would pair well with a book this app could provide a solution. Lastly, as he reviews books and music, Book Soundtrack Creator can create a public playlist he can share with his followers.

Aathira:

Sara, 23 years old, has a book club and they want to listen to music while they have their meetings. This book club is based in Philadelphia and has an extensive reading list. She was born in Bethlehem and has recently started her organization when she moved to Philadelphia last year. She has a degree in art history and is currently working for the Philadelphia Museum of Art where she holds her meetings. 

Sara, who wants to make her meetings moore dynamic and cohesive is thinking about incorporating this application with her weekly book selection. It is another way for her to connect with the other club members by having them discover new music together that relates to the book that they are reading. This application will just go ahead and create a playlist that matches the tone of the book automatically instead of Sara picking out songs on her own which takes up a lot of her time. With a playlist automatically generated she will be able to devote more time into topics to discuss during the reading sessions. 

Tyler:

Natalie, age 16, is a high school student in rural Pennsylvania. She plays sports and maintains good grades in school. She is involved in many after school activities, including book club. Her dad is a mechanic and her mom is a teacher who both share a passion for music and books. Natalie has also always been a big movie fan. Something that she always thought was missing from books was a soundtrack that plays like it does in movies. In her free time she really loves reading. When she found Book Soundtrack Creator, she realized that it was the perfect mix between her love for music and her love for books. 

Natalie really loves the app because she is able to really connect with her book club, especially now that everything is virtual. They are able to share playlists and find the perfect playlist for the books that they are reading and discussing. It is also perfect for Natalie’s little sister who loves getting read bedtime stories. Using Book Soundtrack Creator, Natalie is able to play songs in the background while reading to her sister before bedtime. 

Alex:

Sean, age 27, is a young entrepreneur and owns a record label in which he produces music, and hires bands/artists to play his music to make records. Although his business is based out of Atlanta, GA, his record label continues to attract new talent because of the music he produces (many of which soar to the top of the Billboards). He was born in New Orleans, LA, where he grew up around music and was exposed to many famous local artists in his early years. 

Sean, who tends to create single hits, is now thinking of putting together a whole album of songs for an artist and wants to give the album a "concept" or "mood". He starts to turn to book reading to give him ideas for new lyrics and album concepts. Also, due to the number of songs that Sean has created throughout his career, he is starting to run out of ideas and needs a platform that could give him new ideas through books that pinpoint a specific mood and concept, while also giving him ideas for new song lyrics. Sean might use the Book Soundtrack Creator to create playlists using books that he likes the concept/theme of, and then look to the playlist that is put together by the software to get new inspiration.
## Link to a feature list (backlog) for the whole project for your project board
link(https://trello.com/b/ORiO8Kk0/book-soundtrack-creator)

## Set up instructions

link(https://docs.djangoproject.com/en/3.1/intro/tutorial01/)
