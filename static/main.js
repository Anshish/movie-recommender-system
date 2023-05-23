const language_codes = {
  English: "en",
  Dutch: "nl",
  Spanish: "es",
  Korean: "ko",
  Finnish: "fi",
  Japanese: "ja",
  Norwegian: "no",
  Ukrainian: "uk",
  Chinese: "zh",
  Italian: "it",
  German: "de",
  Russian: "ru",
  Polish: "pl",
  Thai: "th",
  Icelandic: "is",
  French: "fr",
  Arabic: "ar",
  Romanian: "ro",
  Basque: "eu",
  Telugu: "te",
  Turkish: "tr",
  Indonesian: "id",
  Bengali: "bn",
  Persian: "fa",
  Swedish: "sv",
  Danish: "da",
  Macedonian: "mk",
  Tagalog: "tl",
  Portuguese: "pt",
  Hindi: "hi",
  Tamil: "ta",
  Catalan: "ca",
  Greek: "el",
  Serbian: "sr",
  Norwegian_Bokmal: "nb",
  Vietnamese: "vi",
  Malayalam: "ml",
  Hebrew: "he",
  Kannada: "kn",
  Czech: "cs",
  Dzongkha: "dz",
  Irish: "ga",
  Hungarian: "hu",
  Latin: "la",
};

const genres = [
  "Action",
  "Adventure",
  "Animation",
  "Comedy",
  "Crime",
  "Documentary",
  "Drama",
  "Family",
  "Fantasy",
  "History",
  "Horror",
  "Music",
  "Mystery",
  "Romance",
  "Science Fiction",
  "TV Movie",
  "Thriller",
  "War",
  "Western",
];

const userId = document.getElementById("userId").value;
console.log(userId);

// function to redirect user to details page for movie
function redirectToDetailsPage(title) {
  window.location.href = `/movie-details?userId=${encodeURIComponent(
    userId
  )}&title=${encodeURIComponent(title)}`;
}

// this function will redirect selected movie to it's detail page
function handleMovieClick(movieTitle) {
  console.log(movieTitle);
  fetch(
    `/movie-details?userId=${encodeURIComponent(
      userId
    )}&title=${encodeURIComponent(movieTitle)}`
  );
  // .then((response) => response.json())
  // .then((data) => {
  //   console.log(data);
  // })
  // .catch((error) => {
  //   console.error("error: ", error);
  // });
  redirectToDetailsPage(movieTitle);
}

// this function will generate movie elements and add click event
// listener upon them
function generateMovieElements(titles, posters, containerId) {
  const moviesContainer = document.getElementById(containerId);
  moviesContainer.innerHTML = "";

  for (let i = 0; i < titles.length; i++) {
    const movieElement = document.createElement("div");
    movieElement.className = "col-xs movie-list";

    // create image element for movie image
    const imageElement = document.createElement("img");
    imageElement.src = posters[i];
    imageElement.alt = titles[i];
    imageElement.className = "img-fluid movie-poster";
    movieElement.appendChild(imageElement);

    // create paragraph element for movie title
    const titleElement = document.createElement("p");
    titleElement.textContent = titles[i];
    titleElement.className = "movie-title";
    movieElement.appendChild(titleElement);

    // add click event listener to movie element
    movieElement.addEventListener("click", () => {
      handleMovieClick(titles[i]);
    });

    // append movie element to container
    moviesContainer.appendChild(movieElement);
  }
}

// this function will generate years for movies to be used in dropdown
function generateYearOptions() {
  const yearSelect = document.getElementById("year-select");
  const currentYear = 2023;
  const startYear = 1950;
  const endYear = currentYear;

  for (let i = endYear; i >= startYear; i--) {
    const option = document.createElement("option");
    option.value = i;
    option.textContent = i;
    yearSelect.appendChild(option);
  }
}

// this function will generate languages for movies to be used in dropdown
function generateLanguageOptions() {
  const languageSelect = document.getElementById("language-select");

  for (const language in language_codes) {
    const option = document.createElement("option");
    option.value = language;
    option.textContent = language;
    languageSelect.appendChild(option);
  }
}

// this function will generate genres for movies to be used in dropdown
function generateGenreOptions() {
  const genreSelect = document.getElementById("genre-select");

  for (const genre of genres) {
    const option = document.createElement("option");
    option.value = genre;
    option.textContent = genre;
    genreSelect.appendChild(option);
  }
}

// this function will generate titles for movies in search bar
function generateMovieTitles() {
  fetch("/get-titles")
    .then((response) => response.json())
    .then((movieTitles) => {
      const datalist = document.getElementById("movie-titles");
      datalist.innerHTML = "";

      movieTitles.forEach((title) => {
        const option = document.createElement("option");
        option.value = title;
        datalist.appendChild(option);
      });
    })
    .catch((error) => {
      console.error("Error: ", error);
    });
}

// function to generate popular movies
function generatePopular() {
  fetch("/get-popular")
    .then((response) => response.json())
    .then((data) => {
      const popular_movies_titles = data[0];
      const popular_movies_posters = data[1];
      generateMovieElements(
        popular_movies_titles,
        popular_movies_posters,
        "movies-popular"
      );
    });
}

// function to generate top-rated movies
function generateTopRated() {
  fetch("/get-top-rated")
    .then((response) => response.json())
    .then((data) => {
      const top_rated_movies_titles = data[0];
      const top_rated_movies_posters = data[1];
      generateMovieElements(
        top_rated_movies_titles,
        top_rated_movies_posters,
        "movies-top-rated"
      );
    });
}

// function to handle year selection change event
function handleYearSelection() {
  const selectedYear = yearSelect.value;

  fetch("/movies-by-year", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ year: selectedYear }),
  })
    .then((response) => response.json())
    .then((data) => {
      const movies_by_year_titles = data[0];
      const movies_by_year_posters = data[1];

      generateMovieElements(
        movies_by_year_titles,
        movies_by_year_posters,
        "movies-year"
      );
    })
    .catch((error) => {
      console.error("error:", error);
    });
}

// function to handle language selection change event
function handleLanguageSelection() {
  const selectedLanguage = languageSelect.value;

  fetch("/movies-by-language", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ language: language_codes[selectedLanguage] }),
  })
    .then((response) => response.json())
    .then((data) => {
      const movies_by_language_titles = data[0];
      const movies_by_language_posters = data[1];

      generateMovieElements(
        movies_by_language_titles,
        movies_by_language_posters,
        "movies-language"
      );
    })
    .catch((error) => {
      console.error("error:", error);
    });
}

// function to handle genre selection change event
function handleGenreSelection() {
  const selectedGenre = genreSelect.value;

  fetch("/movies-by-genre", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ genre: selectedGenre }),
  })
    .then((response) => response.json())
    .then((data) => {
      const movies_by_genre_titles = data[0];
      const movies_by_genre_posters = data[1];

      generateMovieElements(
        movies_by_genre_titles,
        movies_by_genre_posters,
        "movies-genre"
      );
    })
    .catch((error) => {
      console.error("error:", error);
    });
}

// this function will send selected movie to backend
function handleSearch(event) {
  event.preventDefault();

  // get search input value
  const searchInput = document.getElementById("search-input");
  const movieTitle = searchInput.value;
  console.log(movieTitle);

  // send search query to backend
  fetch(
    `/movie-details?userId=${encodeURIComponent(
      userId
    )}&title=${encodeURIComponent(movieTitle)}`
  )
    .then((response) => {
      if (response.ok) {
        redirectToDetailsPage(movieTitle);
      } else {
        var ele = document.getElementById("search-message");
        ele.textContent =
          "Sorry but this movie is not available in our database";
      }
    })
    .catch((error) => {
      console.error("error: ", error);
    });
}

// here we will add event listener to select tag for year
const yearSelect = document.getElementById("year-select");
yearSelect.addEventListener("change", handleYearSelection);

// here we will add event listener to select tag for language
const languageSelect = document.getElementById("language-select");
languageSelect.addEventListener("change", handleLanguageSelection);

// here we will add event listener to select tag for genre
const genreSelect = document.getElementById("genre-select");
genreSelect.addEventListener("change", handleGenreSelection);

// here we will add event listener to form search input
const searchForm = document.getElementById("input-form");
searchForm.addEventListener("submit", handleSearch);

// call function to generate years
generateYearOptions();

// call function to generate languages
generateLanguageOptions();

// call function to generate genres
generateGenreOptions();

// use this to show current year movies by default
const currentYear = 2023;
yearSelect.value = currentYear;
handleYearSelection();

// use this to show english language movies by default
const currentLanguage = "English";
languageSelect.value = currentLanguage;
handleLanguageSelection();

// use this to show Action movies by default
const currentGenre = "Action";
genreSelect.value = currentGenre;
handleGenreSelection();

// use this function to generate movie titles for search bar
generateMovieTitles();

// use this function to generate popular movies
generatePopular();

// use this function to generate top rated movies
generateTopRated();

window.onload = function () {
  if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
  }
};

var movieElements = document.getElementsByClassName("movie-list");

Array.from(movieElements).forEach(function (movieElement) {
  movieElement.addEventListener("click", function () {
    var movieTitleElement = this.querySelector(".movie-title");
    if (movieTitleElement) {
      var movieTitle = movieTitleElement.textContent;
      handleMovieClick(movieTitle);
      console.log(movieTitle);
    }
  });
});
