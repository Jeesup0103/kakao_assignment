var ws = new WebSocket("ws://localhost:8000/ws");
var username = "";
$(document).ready(function () {
  $.ajax({
    url: "/get-username",
    type: "GET",
    success: function (name) {
      username = name;
    },
  });
  fetchAndDisplayMessages();
  $(".chat").scrollTop($(".chat")[0].scrollHeight);

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

  $("#toggle-media-upload").click(function () {
    $("#media-upload-form").toggle();
  });

  // handle media inputs
  $("#media-upload-form").submit(function (e) {
    const mediaInput = $("#media-upload")[0];
    if (mediaInput.files.length === 0) {
      alert("파일을 선택해주세요");
    } else {
      const timeNow = new Date();
      const formattedTime =
        (timeNow.getHours() >= 12 ? " 오후 " : " 오전 ") +
        (timeNow.getHours() % 12 || 12) +
        ":" +
        (timeNow.getMinutes() < 10 ? "0" : "") +
        timeNow.getMinutes();
      const currentUrl = window.location.href;
      const match = currentUrl.match(/\/(\d+)$/);
      const chatlist_id = match[1];
      const formData = new FormData();
      formData.append("media", mediaInput.files[0]);
      formData.append("date", formattedTime);
      formData.append("chatlist_id", chatlist_id);
      for (var key of formData.keys()) {
        console.log(key);
      }
      for (var value of formData.values()) {
        console.log(value);
      }

      $.ajax({
        url: "/upload-media",
        type: "POST",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
          ws.send(JSON.stringify(response));
          window.location.reload();
        },
      });
    }
  });

  function fetchAndDisplayMessages() {
    var currentUrl = window.location.href;
    var match = currentUrl.match(/\/(\d+)$/);
    if (match) {
      var chatId = match[1];
      $.ajax({
        url: "/getchat/" + chatId,
        type: "get",
        success: function (messages) {
          $(".chat").empty();
          messages.forEach(function (message) {
            var messageElement;
            console.log(message);
            if (message.name === username) {
              messageElement = `
              <div class="mine">
                <div class="messageRow">
                  <div class="time">${message.date}</div>
                  ${
                    message.text
                      ? `<div class="myTalk text">${message.text}</div>`
                      : ""
                  }
                  ${
                    message.image_url
                      ? `<a href="/${message.image_url}" target="_blank">
                          <img src="/${message.image_url}" class="media">
                        </a>`
                      : ""
                  }
                  ${
                    message.video_url
                      ? `
                          <video controls class="media"><source src="/${message.video_url}" type="video/mp4"></video>
                        `
                      : ""
                  }
                </div>
              </div>
            `;
            } else {
              messageElement = `
              <div class="others">
                <div class="otherName">${message.name}</div>
                <div class="messageRow">
                  ${
                    message.text
                      ? `<div class="otherTalk text">${message.text}</div>`
                      : ""
                  }
                  ${
                    message.image_url
                      ? `<a href="/${message.image_url}" target="_blank">
                          <img src="/${message.image_url}" class="media">
                        </a>`
                      : ""
                  }
                  ${
                    message.video_url
                      ? `
                          <video controls class="media"><source src="/${message.video_url}" type="video/mp4"></video>
                        `
                      : ""
                  }
                  <div class="time">${message.date}</div>
                </div>
              </div>
            `;
            }
            $(".user1").append(messageElement);
          });
          $(".chat").scrollTop($(".chat")[0].scrollHeight);
        },
        error: function (xhr, status, error) {
          console.error("Error fetching messages:", error);
        },
      });
    }
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
      var currentUrl = window.location.href;
      var match = currentUrl.match(/\/(\d+)$/);
      console.log(match[1]);
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
        chatlist_id: match[1],
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
          <div class="messageRow">
            <div class="time">${data.date}</div>
            ${data.text ? `<div class="myTalk text">${data.text}</div>` : ""}
            ${
              data.image_url
                ? `<a href="/${data.image_url}" target="_blank">
                    <img src="/${data.image_url}" class="media">
                  </a>`
                : ""
            }
            ${
              data.video_url
                ? `
                    <video controls class="media"><source src="/${data.video_url}" type="video/mp4"></video>
                  `
                : ""
            }
          </div>
        </div>
      `;
    } else {
      messageElement = `
        <div class="others">
          <div class="otherName">${data.name}</div>
          <div class="messageRow">
            ${data.text ? `<div class="otherTalk text">${data.text}</div>` : ""}
            ${
              data.image_url
                ? `<a href="/${data.image_url}" target="_blank">
                    <img src="/${data.image_url}" class="media">
                  </a>`
                : ""
            }
            ${
              data.video_url
                ? `
                    <video controls class="media"><source src="/${data.video_url}" type="video/mp4"></video>
                  `
                : ""
            }
            <div class="time">${data.date}</div>
          </div>
        </div>
      `;
    }
    $(".user1").append(messageElement);
    $(".chat").scrollTop($(".chat")[0].scrollHeight);
  };
});
