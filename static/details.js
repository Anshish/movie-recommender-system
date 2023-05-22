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
  fetch(`/movie-details?title=${encodeURIComponent(movieTitle)}`);
  redirectToDetailsPage(movieTitle);
}

// this function will generate titles for movies in search bar
function generateMovieTitlesDetails() {
  fetch("/get-titles")
    .then((response) => response.json())
    .then((movieTitles) => {
      const datalist = document.getElementById("movie-titles-details");
      datalist.innerHTML = "";

      movieTitles.forEach((title) => {
        const option = document.createElement("option");
        option.value = title;
        option.text = title;
        datalist.appendChild(option);
      });
    })
    .catch((error) => {
      console.error("Error: ", error);
    });
}

// this function will send selected movie to backend
function handleSearchDetails(event) {
  event.preventDefault();

  // get search input value
  const searchInput = document.getElementById("search-input-details");
  const movieTitle = searchInput.value;
  console.log(movieTitle);

  // send search query to backend
  fetch(
    `/movie-details?userId=${encodeURIComponent(
      userId
    )}&title=${encodeURIComponent(movieTitle)}`
  );
  if (movieTitle !== "") {
    redirectToDetailsPage(movieTitle);
  }
}

selected = document.getElementById("details-container");
// add click event listener to movie element
selected.addEventListener("click", () => {
  handleMovieClick(titles[i]);
});

// here we will add event listener to form search input
const searchForm = document.getElementById("input-form-details");
searchForm.addEventListener("submit", handleSearchDetails);

generateMovieTitlesDetails();

// Get the rating form
const ratingForm = document.getElementById("rating-form");

// Add event listener to the rating form
ratingForm.addEventListener("submit", (e) => {
  e.preventDefault();

  // Get the user rating input
  const ratingInput = document.getElementById("rating");
  const userRating = parseInt(ratingInput.value);

  // Validate the user rating
  if (isNaN(userRating) || userRating < 1 || userRating > 10) {
    alert("Please enter a valid rating between 1 and 10.");
    return;
  }
  const detailsContainer = document.getElementById("details-container");
  const movieTitle = detailsContainer.getAttribute("data-movie-title");
  console.log(movieTitle);
  console.log(userRating);
  // Create the request body
  const requestBody = {
    movie_title: movieTitle,
    rating: userRating,
    userId: userId,
  };

  // Make a POST request to the server
  fetch("/submit_rating", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message);
      updateAverageRating(data.new_average);
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  ratingInput.value = "";

  // Display a success message
  // alert("Thank you for submitting your rating!");
});

function updateAverageRating(newAverage) {
  const currentAverageElement = document.getElementById("current-average");
  currentAverageElement.textContent = newAverage.toFixed(1);
}
