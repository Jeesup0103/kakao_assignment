$(document).ready(function () {
  // Load friends list on page load
  $.ajax({
    url: "/get-friends", // Replace with your API endpoint
    type: "GET",
    success: function (friends) {
      console.log(friends);
      friends.forEach(function (friend) {
        $("#friend-list").append('<li class="friend-item">' + friend + "</li>");
      });
    },
  });

  // Handle friend selection
  $(document).on("click", ".friend-item", function () {
    var friendId = $(this).data("id");
    $.ajax({
      url: "/api/get-chat/" + friendId, // Replace with your API endpoint
      type: "GET",
      success: function (chatData) {
        // Update the chat container with the chat data
        // ...
      },
    });
  });

  // Add friend button functionality
  $("#add-friend-button").click(function () {
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
