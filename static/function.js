var ws = new WebSocket("ws://localhost:8000/ws");

$(document).ready(function () {
  var username = "";

  $(".replybox-user1").on("submit", function (event) {
    event.preventDefault();
    handleSubmitUser1();
  });

  $(".replybox-user1 .reply-text").on("keyup", function (event) {
    if (event.keyCode === 13 && !event.shiftKey) {
      if (!event.shiftKey) {
        event.preventDefault();
        handleSubmitUser1();
      } else {
        $(this).val($(this).val() + "\n");
      }
    }
  });

  $(".IDsend-btn").click(function (event) {
    event.preventDefault();
    username = $(".username").val();
    if (username) {
      username = username.trim();
      fetchAndDisplayMessages();
      $(".username").val("");
    } else {
      alert("Please enter a User ID.");
    }
  });

  function fetchAndDisplayMessages() {
    $.ajax({
      url: "/getchat",
      type: "get",
      success: function (messages) {
        $(".chat").empty();
        messages.forEach(function (message) {
          var messageElement;
          if (message.name === username) {
            messageElement = `
              <div class="mine">
                <div class="time">${message.date}</div>
                <div class="myTalk text" style="white-space: pre-wrap;">${message.text}</div>
              </div>
            `;
            $(".user1").append(messageElement);
          } else {
            messageElement = `
              <div class="others">
                <div class="otherName">${message.name}</div>
                <div class="messageRow">
                  <div class="otherTalk text" style="white-space: pre-wrap;">${message.text}</div>
                  <div class="time">${message.date}</div>
                </div>

              </div>
            `;
            $(".user1").append(messageElement);
          }
        });
        $(".chat").scrollTop($(".chat")[0].scrollHeight);
      },
      error: function (xhr, status, error) {
        console.error("Error fetching messages:", error);
      },
    });
  }

  function handleSubmitUser1() {
    if (!username) {
      alert("Please set your User ID first.");
      return;
    }
    var message = $(".replybox-user1").find(".reply-text").val();
    var trimmedMsg = message;
    trimmedMsg = trimmedMsg.trim();
    if (trimmedMsg) {
      message = message.replace(/\n/g, "<br>");
      const timeNow = new Date();
      const formattedTime =
        (timeNow.getHours() >= 12 ? " 오후 " : " 오전 ") +
        (timeNow.getHours() % 12 || 12) +
        ":" +
        (timeNow.getMinutes() < 10 ? "0" : "") +
        timeNow.getMinutes();
      var data = {
        name: username,
        text: message.replace(/\n/g, "<br>"),
        date: formattedTime,
      };
      ws.send(JSON.stringify(data));
      $.ajax({
        url: "/postchat",
        type: "post",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(data),
        success: function (response) {},
        error: function (xhr, status, error) {
          console.error("Error saving message:", error);
        },
      });
    }
    $(".replybox-user1").find(".reply-text").val("");
  }

  ws.onmessage = function (event) {
    var data = JSON.parse(event.data);
    var messageElement;
    if (data.name === username) {
      messageElement = `
      <div class="mine">
        <div class="time">${data.date}</div>
        <div class="myTalk text" style="white-space: pre-wrap;">${data.text}</div>
      </div>
    `;
    } else {
      messageElement = `
      <div class="others">
        <div class="otherName">${data.name}</div>
        <div class="messageRow">
          <div class="otherTalk text" style="white-space: pre-wrap;">${data.text}</div>
          <div class="time">${data.date}</div>
        </div>
      </div>
    `;
    }
    $(".user1").append(messageElement);
    $(".chat").scrollTop($(".chat")[0].scrollHeight);
  };
});
