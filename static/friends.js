$(document).ready(function () {
  $.ajax({
    url: "/get-username",
    type: "GET",
    success: function (name) {
      $("#username").text(name);
    },
  });
  // Load friends list on page load
  $.ajax({
    url: "/get-friends", // Replace with your API endpoint
    type: "GET",
    success: function (friends) {
      friends.forEach(function (friend) {
        $("#friend-list").append('<li class="friend-item">' + friend + "</li>");
      });
    },
  });

  // Handle friend selection
  $(document).on("click", ".friend-item", function () {
    var username = $("#username").text();
    var friendname = $(this).text();
    $.ajax({
      url: "/get-one-chat?user1=" + username + "&user2=" + friendname, // Replace with your API endpoint
      type: "GET",
      success: function (chat) {
        window.location.href = "/chat/" + chat.id;
      },
    });
  });

  // Add friend button functionality
  $("#add-friend-btn").click(function () {
    var friendUsername = prompt("Enter the username of the friend:");
    var data = { username: friendUsername };
    $.ajax({
      url: "/add-friend", // Replace with your API endpoint
      type: "POST",
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify(data),
      success: function (response) {
        window.location.href = "/friends";
      },
      error: function (error) {
        console.error("Error message:", error);
      },
    });
  });
});
