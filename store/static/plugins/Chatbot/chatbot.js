let chatbot = document.getElementById("chatbot");

let testP = document.querySelector("p");
let key = chatbot.dataset.key;
let user = chatbot.dataset.user;
var jwt = "";

let divLogo = document.createElement("div");
divLogo.id = "divLogo";
let divBot = document.createElement("div");
divBot.id = "divBot";
let closeSpan = document.createElement("span");

closeSpan.innerHTML = "X";
closeSpan.classList.add("bot-close-span");

divBot.appendChild(closeSpan);1

function closeBot(){
    divBot.style.display = "none"
    divLogo.style.display = "block";

    chatbot.style.width = "80px";
    chatbot.style.height = "80px";
}
closeSpan.addEventListener("click", function () {
    closeBot();
})
divBot.classList.add("bot-div-container");
divLogo.classList.add("bot-collapse");


// divBot.style.position = "absolute";
// divBot.style.background = "#313131";
// divBot.style.borderRadius = "50%";
// divBot.style.right = "0";
// divBot.style.bottom = "0";
// divBot.style.width = "80px";
// divBot.style.height = "80px";

chatbot.appendChild(divLogo);
chatbot.appendChild(divBot);

let img = document.createElement("img");
img.src = "http://127.0.0.1:8000/static/img/logo.png";
img.classList.add("bot-logo-img");

divLogo.append(img);
divBot.style.display = "none";


function expand(){
    divBot.style.display = "block";
    divLogo.style.display = "none";
    chatbot.style.width = "450px";
    chatbot.style.height = "510px";
}

divLogo.addEventListener("click", async function () {
    // divBot.style.display = "block";
    // this.style.display = "none";
    expand();
})


if (localStorage.getItem("jwt") == null) {
    url = `http://127.0.0.1:8000/chatbot/validation?key=${key}&user=${user}`;
}
else {
    url = `http://127.0.0.1:8000/chatbot/validation?key=${key}&user=${user}&jwt=${localStorage.getItem("jwt")}`;
}

fetch(url, {
    method: "GET",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
    credentials: "same-origin",
})
    .then(response => {
        console.log(response);
        return response.json();
    })
    .then(data => {
        console.log(data);
        if (data.status == 200) {
            jwt = data.token;
            if (localStorage.getItem("jwt") == null) {
                localStorage.setItem("jwt", data.token)
            }


            var chatbotMain = document.createElement("iframe");
            // chatbotMain.sandbox.add('allow-scripts');
            // chatbotMain.sandbox.add('allow-forms');

            console.log(chatbotMain.sandbox.toString())
            // Returns: "allow-scripts allow-forms"

            console.log(chatbotMain.outerHTML)
            // Returns: <iframe sandbox="allow-scripts allow-forms"></iframe>
            chatbotMain.classList.add("chatbot-main");
            divBot.appendChild(chatbotMain);
            chatbotMain.src = "http://127.0.0.1:8000/chatbot/chatbot_UI";

        }
        else {
            console.log("Error to Get Jwt");
        }
    });

// let chatbotHead = document.createElement("div");
// chatbotHead.innerHTML = "Chatbot";
// chatbotHead.classList.add("chatbot-head");
// chatbot.appendChild(chatbotHead);

// Create IE + others compatible event handler
var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
var eventer = window[eventMethod];
var messageEvent = eventMethod === "attachEvent" ? "onmessage" : "message";

// Listen to message from child window
eventer(messageEvent,function(e) {
  console.log('parent received message!:  ',e.data);

  if(e.data === "exit"){
      closeBot();
  }
},false);

function personMessage(str) {

    let personMessage = document.createElement("div");
    personMessage.innerHTML = str;
    personMessage.classList.add("chatbot-main-person");
    personMessage.classList.add("message");
    chatbotMain.appendChild(personMessage);

}
function botMessage(str) {

    let botMessage = document.createElement("div");
    botMessage.innerHTML = str;
    botMessage.classList.add("chatbot-main-bot");
    botMessage.classList.add("message");
    chatbotMain.appendChild(botMessage);
}



// personMessage("Hello World");
// personMessage("Hello ");
// personMessage("Hello ");
// personMessage("Hello ");

// let chatInput = document.createElement("div");
// chatInput.classList.add("chatbot-input");
// chatbot.appendChild(chatInput);

// let inputField = document.createElement("input");
// inputField.setAttribute("type", "text");
// inputField.classList.add("chatbot-input-textfield");
// chatInput.appendChild(inputField);

// let sendButton = document.createElement("button");
// sendButton.innerHTML = "Send";
// sendButton.classList.add("chatbot-input-button");
// chatInput.appendChild(sendButton);

// let closeButton = document.createElement("div");
// closeButton.innerHTML = "X";
// closeButton.classList.add("close-button");
// chatbotHead.appendChild(closeButton);

function getChatBot(product_id,quantity,order_session_id){


    if (localStorage.getItem("jwt") == null) {
        url = `http://127.0.0.1:8000/chatbot/validation?key=${key}&user=${user}`;
    }
    else {
        url = `http://127.0.0.1:8000/chatbot/validation?key=${key}&user=${user}&jwt=${localStorage.getItem("jwt")}`;
    }

    fetch(url, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        credentials: "same-origin",
    })
        .then(response => {
            console.log(response);
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.status == 200) {
                jwt = data.token;
                if (localStorage.getItem("jwt") == null) {
                    localStorage.setItem("jwt", data.token)
                }


                divBot.querySelector("iframe").remove();

                var chatbotMain = document.createElement("iframe");
                // chatbotMain.sandbox.add('allow-scripts');
                // chatbotMain.sandbox.toggle('allow-forms');

                console.log(chatbotMain.sandbox.toString())
                // Returns: "allow-scripts allow-forms"

                console.log(chatbotMain.outerHTML)
                // Returns: <iframe sandbox="allow-scripts allow-forms"></iframe>
                chatbotMain.classList.add("chatbot-main");
                divBot.appendChild(chatbotMain);
                chatbotMain.src = `http://127.0.0.1:8000/chatbot/set_product_quantity?quantity=${quantity}&product_id=${product_id}&jwt=${localStorage.getItem("jwt")}&identifier=${order_session_id}`;
                expand();
            }
            else {
                console.log("Error to Get Jwt");
            }
        });
}
