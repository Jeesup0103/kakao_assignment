$(document).ready(function () {
  // Handling the login form submission
  $("#loginForm").on("submit", function (event) {
    event.preventDefault();
    var username = $("#userId").val();
    var password = $("#password").val();
    $.ajax({
      type: "POST",
      url: "/token",
      data: {
        username: username,
        password: password,
      },
      success: function (data, txtStatus, xhr) {
        window.location.href = "/chat"; // change
      },
      error: function (error) {
        console.error("Error message:", error.responseText);
      },
    });
  });

  // Handling the register button click
  $("#registerBtn").on("click", function () {
    var username = $("#userId").val();
    var password = $("#password").val();
    if (username && password) {
      var data = {
        username: username,
        password: password,
      };
      $.ajax({
        type: "POST",
        url: "/register",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(data),
        success: function (response) {
          $("#userId").val("");
          $("#password").val("");
        },
        error: function (error) {
          console.error("Error message:", error);
        },
      });
    } else {
      alert("Please enter a User ID and password.");
    }
  });
});
