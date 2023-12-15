$(document).ready(function () {
  $.ajax({
    url: "/get-username",
    type: "GET",
    success: function (name) {
      $("#username").text(name);
    },
  });
  // Load chat list on page load
  $.ajax({
    url: "/get-chatlist", // Replace with your API endpoint
    type: "GET",
    success: function (chatlist) {
      chatlist.forEach(function (chat) {
        $("#chatlist-list").append(
          '<li class="chatlist-item">' +
            '<div class="chatlist-info"><strong>' +
            chat.opponent_username +
            "</strong></div>" +
            '<div class="chat-latest-message">' +
            chat.latest_message +
            "</div>" +
            "</li>"
        );
      });
    },
  });

  // Handle friend selection
  $(document).on("click", ".chatlist-item", function () {
    var username = $("#username").text();
    var friendname = $(".chatlist-info").text();
    $.ajax({
      url: "/get-one-chat?user1=" + username + "&user2=" + friendname, // Replace with your API endpoint
      type: "GET",
      success: function (chat) {
        window.location.href = "/chat/" + chat.id;
      },
    });
  });
});
