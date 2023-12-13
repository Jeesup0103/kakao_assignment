$(document).ready(function () {
  // Handling the login form submission
  $("#loginForm").on("submit", function (event) {
    event.preventDefault();
    var userId = $("#userId").val();
    var password = $("#password").val();

    // AJAX call to send data to the server
    $.ajax({
      type: "POST",
      url: "/login", // replace with your actual login endpoint
      data: {
        userId: userId,
        password: password,
      },
      success: function (response) {
        window.location.href = "/register"; // change
      },
      error: function (error) {},
    });
  });

  // Handling the register button click
  $("#registerBtn").on("click", function () {
    var userId = $("#userId").val();
    var password = $("#password").val();
    var data = {
      userId: userId,
      password: password,
    };
    // register into db
    $.ajax({
      type: "POST",
      url: "/register", // replace with your actual registration endpoint

      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify(data),
      success: function (response) {
        // Handle success (e.g., show a success message or redirect)
      },
      error: function (error) {
        console.error("Error saving message:", error);
      },
    });
  });
});
