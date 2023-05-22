var userId = document.getElementById("userId").value;
console.log(userId);

let selectedAge;

function displaySelectedItems(listId, selectElement) {
  var selectedOptions = selectElement.selectedOptions;
  var selectedItemsElement = document.getElementById(listId);
  selectedItemsElement.innerHTML = "";
  for (var i = 0; i < selectedOptions.length; i++) {
    var li = document.createElement("li");
    li.textContent = selectedOptions[i].value;
    selectedItemsElement.appendChild(li);
  }
}

function savePreferences(event) {
  event.preventDefault();

  var actorsSelect = document.getElementById("actorsInput");
  var directorsSelect = document.getElementById("directorsInput");
  var languagesSelect = document.getElementById("languagesInput");
  var genresSelect = document.getElementById("genresInput");

  var selectedActors = [];
  for (var i = 0; i < actorsSelect.options.length; i++) {
    if (actorsSelect.options[i].selected) {
      selectedActors.push(actorsSelect.options[i].value);
    }
  }

  var selectedDirectors = [];
  for (var i = 0; i < directorsSelect.options.length; i++) {
    if (directorsSelect.options[i].selected) {
      selectedDirectors.push(directorsSelect.options[i].value);
    }
  }

  var selectedLanguages = [];
  for (var i = 0; i < languagesSelect.options.length; i++) {
    if (languagesSelect.options[i].selected) {
      selectedLanguages.push(languagesSelect.options[i].value);
    }
  }

  var selectedGenres = [];
  for (var i = 0; i < genresSelect.options.length; i++) {
    if (genresSelect.options[i].selected) {
      selectedGenres.push(genresSelect.options[i].value);
    }
  }

  selectedAge =
    document.querySelector('input[name="age"]:checked')?.value || null;

  // Display selected options
  displaySelectedItems("selectedActors", actorsSelect);
  displaySelectedItems("selectedDirectors", directorsSelect);
  displaySelectedItems("selectedLanguages", languagesSelect);
  displaySelectedItems("selectedGenres", genresSelect);

  var payload = {
    actors: selectedActors,
    directors: selectedDirectors,
    languages: selectedLanguages,
    genres: selectedGenres,
    age: selectedAge,
  };

  fetch("/preferences/" + userId, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => {
      if (response.ok) {
        console.log("preferences saved successfully");
        window.location.href = "/welcome/" + userId;
      } else {
        console.log("failed to save preferences");
      }
    })
    .catch((error) => {
      console.error("error: ", error);
    });
}

// Bind the savePreferences function to the submit button click event
document
  .getElementById("preferencesForm")
  .addEventListener("submit", savePreferences);
