from flask import Flask,render_template, session,request, url_for,jsonify, redirect
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
import uuid
import certifi


ca = certifi.where()
###############################################################
# 1. Create MongoDB client
url='mongodb+srv://admin-anshish:test123@cluster0.2gzry.mongodb.net/?retryWrites=true&w=majority'
client=MongoClient(url,tlsCAFile=certifi.where())

# 2. Create database
db=client['movie_database']

# 3. Create collections
users_collections=db['users']
preferences_collections=db['preferences']
metadata_collections=db['metadata']
ratings_collections=db['ratings']

 
###############################################################



###############################################################
# Importing files

# 1. Import movies dataset
file=open('./datasets/movies.pkl','rb')
movies=pickle.load(file)
file.close()


# # 2. Import popularity movies dataset
# file=open('./datasets/popularity.pkl','rb')
# popularity=pickle.load(file)
# file.close()
popularity=movies.sort_values('popularity',ascending=False)[0:20]


# 3. Import top-rated movies dataset
# file=open('./datasets/top_rated.pkl','rb')
# top_rated=pickle.load(file)
# file.close()
top_rated=movies.sort_values('weigh_avg_rating',ascending=False)



# 4. Import tfidf matrix for recommendations 
file=open('./datasets/matrix.pkl','rb')
matrix=pickle.load(file)
file.close()


# 5. Import data 
# file=open('./datasets/data.pkl','rb')
# data=pickle.load(file)
# file.close()
###############################################################

language_codes = {
  'English': "en",
  'Dutch': "nl",
  'Spanish': "es",
  'Korean': "ko",
  'Finnish': "fi",
  'Japanese': "ja",
  'Norwegian': "no",
  'Ukrainian': "uk",
  'Chinese': "zh",
  'Italian': "it",
  'German': "de",
  'Russian': "ru",
  'Polish': "pl",
  'Thai': "th",
  'Icelandic': "is",
  'French': "fr",
  'Arabic': "ar",
  'Romanian': "ro",
  'Basque': "eu",
  'Telugu': "te",
  'Turkish': "tr",
  'Indonesian': "id",
  'Bengali': "bn",
  'Persian': "fa",
  'Swedish': "sv",
  'Danish': "da",
  'Macedonian': "mk",
  'Tagalog': "tl",
  'Portuguese': "pt",
  'Hindi': "hi",
  'Tamil': "ta",
  'Catalan': "ca",
  'Greek': "el",
  'Serbian': "sr",
  'Norwegian_Bokmal': "nb",
  'Vietnamese': "vi",
  'Malayalam': "ml",
  'Hebrew': "he",
  'Kannada': "kn",
  'Czech': "cs",
  'Dzongkha': "dz",
  'Irish': "ga",
  'Hungarian': "hu",
  'Latin': "la",
}



###############################################################
# Extract lists

# 1. Extract popular movie titles and posters
popular_movie_posters=[]
popular_movie_titles=[]
count=0
for index,row in popularity.iterrows():
    if count==20:
        break
    else:
        popular_movie_posters.append('https://image.tmdb.org/t/p/original'+row['poster_path'])
        popular_movie_titles.append(row['title'])
        count+=1


# 2. Extract top rated movies titles and posters
top_rated_movie_posters=[]
top_rated_movie_titles=[]
count=0
for index,row in top_rated.iterrows():
    if count==20:
        break
    else:
        top_rated_movie_posters.append('https://image.tmdb.org/t/p/original'+row['poster_path'])
        top_rated_movie_titles.append(row['title'])
        count+=1


# 3. Get movies by year
def get_by_year(year):
    count=0
    movie_lis=[]
    poster_lis=[]
    for index,row in top_rated.iterrows():
        if count==20:
            break
        else:
            if row['release_year']==year:
                movie_lis.append(row['title'])
                poster_lis.append('https://image.tmdb.org/t/p/original'+row['poster_path'])
                count+=1
    return movie_lis,poster_lis


# 4. Get movies by language
def get_by_language(language):
    count=0
    titles_lis=[]
    posters_lis=[]
    for index,row in top_rated.iterrows():
        if count==20:
            break
        else:
            if row['original_language']==language:
                titles_lis.append(row['title'])
                posters_lis.append('https://image.tmdb.org/t/p/original'+row['poster_path'])
                count+=1
    return titles_lis,posters_lis


# 5. Get movies by genre

def get_by_genre(genre):
    count=0
    titles=[]
    posters=[]
    for index,row in top_rated.iterrows():
        if count==20:
            break
        else:
            for gen in row['genre']:
                if gen==genre:
                    titles.append(row['title'])
                    posters.append('https://image.tmdb.org/t/p/original'+row['poster_path'])
                    count+=1
    return titles,posters


# 6. Get movie title
def get_titles():
    titles=movies['title'].tolist()
    return titles


# 7. Get movie details
def get_details(title):
    details=movies.loc[movies['title']==title]
    # overview=' '.join(details['overview'].values[0])
    overview=details['overview'].values[0]
    poster='https://image.tmdb.org/t/p/original'+details['poster_path'].values[0]
    #vote=float(details['vote_average'].values[0])
    genres=details['genre'].values[0]
    year=int(details['release_year'].values[0])
    cast=details['cast'].values[0]
    crew=details['crew'].values[0][0]     
    # vote_count=int(details['vote_count'].values[0])
    result = metadata_collections.find_one({'movie_name': title})
    vote=round(result['vote_average'],1)
    movie_data={
        'title':title,
        'poster':poster,
        'overview':overview,
        'vote':vote,
        'genres':genres,
        'year':year,
        'cast':cast,
        'crew':crew,
    }
    return movie_data

# 8. Get Cosine Similarity
def get_cosine_similarity(matrix):
    similarity=cosine_similarity(matrix,matrix)
    return similarity
similarity=get_cosine_similarity(matrix)


# 8. Get recommendations
def get_recommendations(title):
    movie_index = movies[movies['title'] == title].index[0]  # this will give index of the movie in data frame
    distances = similarity[movie_index]  # this will give similarity score of given movie with other movies
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
                 1:16]  # this will give top 5 movies with highest similarity score and their index
    rec_title_lis=[]
    rec_poster_lis=[]
    for i in movie_list:
        movieTitle=movies.iloc[i[0]].title
        deets=movies.loc[movies['title']==movieTitle]
        pos='https://image.tmdb.org/t/p/original'+deets['poster_path'].values[0]
        rec_title_lis.append(movieTitle)
        rec_poster_lis.append(pos)
        recommended_movies=list(zip(rec_title_lis,rec_poster_lis))
    return recommended_movies


# 9. Get cast
def get_cast():
    cast_names = set()
    for cast_list in movies['cast']:
        cast_names.update(cast_list)
    cast_names = list(cast_names)
    cast_names.sort()
    return cast_names
cast_lis=get_cast()


# 10. Get directors
def get_directors():
    crew_names = set()
    for crew_list in movies['crew']:
        crew_names.update(crew_list)
    crew_names = list(crew_names)
    crew_names.sort()
    return crew_names
directors_lis=get_directors()


# 11. Get genres
def get_genres():
    genre_names = set()
    for genre_list in movies['genre']:
        genre_names.update(genre_list)
    genre_names = list(genre_names)
    genre_names.sort()
    return genre_names
genres_lis=get_genres()


# 12. Get languages
def get_languages():
    language_list = movies['original_language'].unique().tolist()
    language_list.sort()
    return language_list
languages_lis=["English","Dutch","Spanish","Korean","Finnish","Japanese","Norwegian","Ukrainian","Chinese","Italian","German","Russian","Polish","Thai","Icelandic","French","Arabic","Romanian","Basque","Telugu","Turkish","Indonesian","Bengali","Persian","Swedish","Danish","Macedonian","Tagalog","Portuguese","Hindi","Tamil","Catala","Greek","Serbian","Norwegian_Bokmal","Vietnamese","Malayalam","Hebrew","Kannada","Czech","Dzongkha","Irish","Hungarian","Latin",]


# 13. Get recommendations by preferences
def get_by_user(cast_lis,crew_lis,language_lis,genre_lis,adult_lis):
    frequency={}

    # for cast
    for index,row in movies.iterrows():
        cast=row['cast']
        crew=row['crew']
        original_language=row['original_language']
        genre=row['genre']
        adult=row['adult']
        count=0

        # for cast
        for i in cast:
            if i in cast_lis:
                count+=1
        
        # for crew
        for i in crew:
            if i in crew_lis:
                count+=1

        # for language
        lang=[]
        for i in language_lis:
            lang.append(language_codes[i])

        if original_language in lang:
            count+=1

        # for genre
        for i in genre:
            if i in genre_lis:
                count+=1

        if adult_lis==None:
            adult_lis=True
        elif adult_lis=="yes":
            adult_lis=True
        else:
            adult_lis=False
        if adult==adult_lis:
            count+=1

        frequency[row['title']]=count

    frequency = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))
    titles=[]
    posters=[]
    for i, (key, value) in enumerate(frequency.items()):
        if i >= 20:
            break
        title=key
        deets=movies.loc[movies['title']==title]
        pos='https://image.tmdb.org/t/p/original'+deets['poster_path'].values[0]
        titles.append(title)
        posters.append(pos)
    return [titles,posters]

def get_key_from_value(dictionary,value):
    for key,val in dictionary.items():
        if val==value:
            return key
    return None


# 14. Get deets
def get_deets(name):
    details=movies.loc[movies['title']==name]
    genres=details['genre'].values[0]
    cast=details['cast'].values[0]
    crew=details['crew'].values[0][0]
    language=details['original_language'].values[0]
    ori_lan=get_key_from_value(language_codes,language)
    return [cast,crew,genres,ori_lan]
###############################################################


app=Flask(__name__)
app.secret_key='spacecowboy'

@app.route('/')
def home():
    return render_template('login.html')


# end point to get popular movies
@app.route('/get-popular',methods=['GET'])
def get_popular():
    return jsonify(popular_movie_titles,popular_movie_posters)

# end point to get top-rated movies
@app.route('/get-top-rated',methods=['GET'])
def get_top_rated():
    return jsonify(top_rated_movie_titles,top_rated_movie_posters)



@app.route('/movies-by-year',methods=['POST'])
def fetch_movies_by_year():
    year=request.json.get('year')
    year=int(year)
    movies_by_year_titles,movies_by_year_posters=get_by_year(year)
    return jsonify(movies_by_year_titles,movies_by_year_posters)


@app.route('/movies-by-language',methods=['POST'])
def fetch_movies_by_language():
    language=request.json.get('language')
    movies_by_language_titles,movies_by_language_posters=get_by_language(language)
    return jsonify(movies_by_language_titles,movies_by_language_posters)


@app.route('/movies-by-genre',methods=['POST'])
def fetch_movies_by_genre():
    genre=request.json.get('genre')
    movies_by_genre_titles,movies_by_genre_posters=get_by_genre(genre)
    return jsonify(movies_by_genre_titles,movies_by_genre_posters)


# End point to handle movie details request
@app.route('/movie-details',methods=['GET'])
def get_movie_details():
    # Get movie title from query parameters
    title=request.args.get('title')
    print(title)

    userId=request.args.get('userId')
    print(userId)

    movie_details=get_details(title)

    recommended_movies=get_recommendations(title)

    # return render_template('details.html',movie_details=movie_details)
    return render_template('details.html',movie_details=movie_details,recommended_movies=recommended_movies,userId=userId)


# End point to get movie titles
@app.route('/get-titles',methods=['GET'])
def movie_titles():
    # Call get_titles function
    titles=get_titles()
    return jsonify(titles)


# End point for signup page
@app.route('/signup',methods=['GET','POST'])
def signup():
    userId=None
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        # Check if the user already exists
        existing_user=users_collections.find_one({'email':email})
        if existing_user:
            # user already exists, redirect to login page
            message='User with this email already exists. Please Login or Signup with new Email'
            return render_template('signup.html',error=message)

        # Generate unique userId
        userId=str(uuid.uuid4())

        # Save user info to user collection
        user={
            'userId':userId,
            'email':email,
            'password':password
        }
        users_collections.insert_one(user)
        return redirect(url_for('save_preferences',userId=userId))
    return render_template('signup.html')


# End point for preferences page
@app.route('/preferences/<userId>',methods=['GET','POST'])
def save_preferences(userId):
    print('this is user id',userId)
    if request.method=='POST':
        preferences = request.get_json()
        actors = preferences.get('actors')
        directors = preferences.get('directors')
        languages = preferences.get('languages')
        genres = preferences.get('genres')
        age = preferences.get('age')
        # save in db
        preferences={
            'userId':userId,
            'actors': actors,
            'directors': directors,
            'languages': languages,
            'genres': genres,
            'age':age
        }
        preferences_collections.insert_one(preferences)
        print('Redirecting to /welcome/'+userId)
        return redirect(url_for('welcome',userId=userId))
    return render_template('preferences.html',
                           actors=cast_lis,
                           directors=directors_lis,
                           languages=languages_lis,
                           genres=genres_lis,
                           userId=userId)


# End point for login route
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        
        email=request.form.get('email')
        password=request.form.get('password')

        # Check if user exists and password matches
        user=users_collections.find_one({'email':email,'password':password})
        if(user==None):
            error_message='User note found in database. Signup first'
            return render_template('login.html',error=error_message)
        print(user)
        userId=user['userId']
        print(userId)
        session['userId']=userId

        if user:
            userId=str(user['userId'])
            preferences=preferences_collections.find_one({
                'userId':userId
            })
            if preferences:
                # user preferences already exists, redirect to welcome page
                return redirect(url_for('welcome',userId=userId,preferences=preferences))
            else:
                # user preferences do not exists, redirect to preferences page
                return redirect(url_for('save_preferences',userId=userId))
        else:
            error_message='Invalid email or password'
        return render_template('login.html',error=error_message)
    return render_template('login.html')


# End point for welcome page
@app.route('/welcome/<userId>')
def welcome(userId):
    # Retrieve user preferences
    user_preferences=preferences_collections.find_one({'userId':userId})
    log=False
    if 'userId' in session:
        log=True
    # Extract lists
    actors=user_preferences.get('actors',[])
    directors=user_preferences.get('directors',[])
    languages=user_preferences.get('languages',[])
    genres=user_preferences.get('genres',[])
    adult=user_preferences.get('age',True)
    print(actors)
    print(directors)
    print(languages)
    print(genres)
    print(adult)

    flag=False
    if(len(actors)!=0 or len(directors)!=0 or len(languages)!=0 or len(genres)!=0 or adult!=None):
        flag=True
    
    if flag==True:
        titles,posters=get_by_user(actors,directors,languages,genres,adult)
        return render_template('index.html',userId=userId,rec_titles=titles,rec_posters=posters,flag=flag)
    else:
        return render_template('index.html',userId=userId,flag=flag)


# This to populate search bars in preferences page
@app.route('/lists')
def get_lists():
    actors_list=cast_lis
    directors_list=directors_lis
    languages_list=languages_lis
    genres_list=genres_lis
    return jsonify({
        'actors':actors_list,
        'directors':directors_list,
        'languages':languages_list,
        'genres':genres_list
    })

@app.route('/logout')
def logout():
    # Clear the user session or perform logout actions
    session.pop('userId',None)
    session.clear()
    return redirect(url_for('login'))

@app.route('/submit_rating',methods=['GET','POST'])
def submit_rating():
    movie_title=request.json.get('movie_title')
    rating=int(request.json.get('rating'))
    userId=request.json.get('userId')
    print('title',movie_title)
    print('user_rating',rating)
    print('userId',userId)

    result=metadata_collections.find_one({'movie_name':movie_title,'users':userId})

    current_vote_average=0
    current_vote_count=0
    message=''
    new_vote_average=0

    if result :
        print('you have rated this movie')
        message='You have already rated this movie'
        res=metadata_collections.find_one({'movie_name': movie_title})
        new_vote_average=res['vote_average']

    else:
        res=metadata_collections.find_one({'movie_name': movie_title})
        current_vote_average = res['vote_average']
        current_vote_count = res['vote_count']
        print('current vote average',current_vote_average)
        new_vote_average = ((current_vote_average * current_vote_count) + rating) / (current_vote_count + 1)
        print('new',new_vote_average)
        metadata_collections.update_one(
            {'movie_name':movie_title},
            {
                '$set':{'vote_average':new_vote_average},
                '$push':{'users':userId}
            },
            upsert=True
        )

        # Optionally, you can increment the vote_count field by 1
        metadata_collections.update_one(
            {'movie_name': movie_title},
            {'$inc': {'vote_count': 1}}
        )
        message='User rating is added successfully'
        
        if(rating>=6.0):
            actors,directors,genres,languages=get_deets(movie_title)
            print(actors)
            print(directors)
            print(genres)
            print(languages)
            age=None
            pref=preferences_collections.find_one({'userId':userId})
            if pref:
                # User exists, update their preferences
                preferences_collections.update_one(
                    {'userId': userId},
                    {'$addToSet': {
                        'actors': {'$each':actors},
                        'directors': directors,
                        'genres': {'$each':genres},
                        'languages': languages
                    }}
                )
            else:
                preferences={
                    'userId':userId,
                    'actors': actors,
                    'directors': directors,
                    'languages': languages,
                    'genres': genres,
                    'age':age
                }
                preferences_collections.insert_one(preferences)
            message = 'User rating is added successfully. Movie details added to preferences.'

    return jsonify({
        'new_average':new_vote_average,
        'message':message
    })

if __name__=='__main__':
    app.run(debug=True)

