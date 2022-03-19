host = "ws://172.17.100.224:8081/"
let ViewName = ""


function getWebSocketServer() {
  if (window.location.host === onraptor.github.io") {
    return "wss://webchatttt.herokuapp.com/";
  } else if (window.location.host === "localhost:8081") {
    return "ws://localhost:8001/";
  } else {
    throw new Error(`Unsupported host: ${window.location.host}`);
  }
}

function AddMessage(mess, align="center"){
                    if (!messages)
                        return;
                    $(`<li style="{ text-align: ${align} }"/>`).text(mess).appendTo('ul#messages');
                    $('ul#messages> li').slice(0, -50).remove();
                    $('ul#messages').scrollTop( $('ul#messages').get(0).scrollHeight );
}

function SetUsers(users){
    $("#users").empty()
    for (let user of users){
                    $("<li/>").text(user).appendTo('#users');
    }
}

window.addEventListener("DOMContentLoaded", () => {
    message_text = document.querySelector("#message");
    const websocket = new WebSocket(getWebSocketServer());

    $("#updateDetails").on('click', function() {
      document.getElementById("favDialog").showModal();
    });


  $("#message").on('keyup', function (e) {
    if ((e.key === 'Enter' || e.keyCode === 13) && $("#message").val() != "") {
    event = {
        type : "message",
        body : $("#message").val(),
        name : ViewName
    }
    websocket.send(JSON.stringify(event));
    $("#message").val("")
    }
  });
  $("#welcomeDialog").on('close', function () {
    ViewName = $("#join_name").val()
    event = {
    type : "joining",
    name: ViewName
    }
    websocket.send(JSON.stringify(event));
  });

  document.getElementById("favDialog").addEventListener('close', function () {
    const oldName = ViewName
    ViewName = $("#name").val()
    event = {
    type : "changedName",
    oldname : oldName,
    name : ViewName
    }
    websocket.send(JSON.stringify(event));
  });

  websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "message":
        if (event["align"] == "undefined"){
            AddMessage(event["body"]);
        }
        else{
            AddMessage(event["body"], event["align"]);
        }
        break;
      case "users":
        SetUsers(event["body"]);
    }
  };
  websocket.onopen = function(e) {
    document.getElementById('welcomeDialog').showModal();
};

websocket.onerror = function(error) {
  alert("Server down or error");
};
});
