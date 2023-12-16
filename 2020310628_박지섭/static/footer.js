$(document).ready(function () {
  $("#friends-btn").click(function () {
    window.location.href = "/friends";
  });

  $("#chats-btn").click(function () {
    window.location.href = "/chatlist";
  });

  $("#logout-btn").click(function () {
    $.ajax({
      url: "/logout",
      type: "GET",
      success: function (name) {
        window.location.href = "/login";
      },
    });
  });
});
