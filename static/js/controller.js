var hasGP = false;
var repGP;
var celebrating = true;
var picking = true;
var placing = true;
var able_to_place = true;
var tutoring = false;
var starting = false;
var cozmo_tutorial = false;

function canGame() {
    return "getGamepads" in navigator;
}

function initGame() {
    if (tutoring || starting){
        return;
    }

    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.height, canvas.width);

    context.font = '40pt Calibri';
    context.textAlign = 'center';
    context.fillStyle = 'white';
    context.shadowColor = "black";
    context.shadowOffsetX = 1;
    context.shadowOffsetY = 1;

    context.fillText('Hello, Cozmo', canvas.width / 2, canvas.height / 2);
}

function tutorGame() {
    if (!tutoring){
        return;
    }

    if (starting){
        return;
    }

    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.height, canvas.width);

    context.font = '40pt Calibri';
    context.textAlign = 'center';
    context.fillStyle = 'white';
    context.shadowColor = "black";
    context.shadowOffsetX = 1;
    context.shadowOffsetY = 1;

    context.fillText('Remote Control', canvas.width / 2, canvas.height / 2);

    setTimeout (function() {
        context.font = '30pt Calibri';
        context.clearRect(0, 0, canvas.height, canvas.width);
        var image_1 = document.getElementById("image_1");
        var image_2 = document.getElementById("image_3");
        var text = 'To direct Cozmo ...';
        cozmo_tutorial = new CozmoTutorial(canvas, text, image_1, image_2, 500);
        setTimeout (function() {
            var image_1 = document.getElementById("image_1");
            var image_2 = document.getElementById("image_4");
            var text = 'To pick up something ...';
            cozmo_tutorial.text = text;
            cozmo_tutorial.image_1 = image_1;
            cozmo_tutorial.image_2 = image_2;
            setTimeout (function() {
                var image_1 = document.getElementById("image_1");
                var image_2 = document.getElementById("image_2");
                var text = 'To start ...';
                cozmo_tutorial.text = text;
                cozmo_tutorial.image_1 = image_1;
                cozmo_tutorial.image_2 = image_2;
            }, 3000);
        }, 3000);
    }, 3000);
}

function CozmoTutorial(canvas, text, image_1, image_2, period)
{
    this.textVisible = true;
    this.canvas = canvas;
    this.text = text;
    this.image_1 = image_1;
    this.image_2 = image_2;
    this.period = period;
    var self = this; // This is to pass the reference into setInterval
    this.interval = setInterval(function() { self.doBlink(); }, this.period);
    this.doBlink = function()
    {
        var context = this.canvas.getContext("2d");
        if(this.textVisible)
        {
            context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            context.fillText(this.text, canvas.width / 2, canvas.height / 2 - 200);
            context.drawImage(this.image_1, canvas.width / 2 - image_1.width / 2, canvas.height / 2 - image_1.height / 2 + 50);
            this.textVisible = false;
        }
        else
        {
            this.drawText();
        }
    };
    this.drawText = function()
    {
        var context = this.canvas.getContext("2d");
        context.drawImage(this.image_2, canvas.width / 2 - image_2.width / 2, canvas.height / 2 - image_2.height / 2 + 50);
        this.textVisible = true;
    };
}

function startGame() {
    if (!starting)
    {
        return;
    }

    clearInterval(cozmo_tutorial.interval);
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.height*2, canvas.width*2);

    context.font = '40pt Calibri';
    context.textAlign = 'center';
    context.fillStyle = 'white';
    context.shadowOffsetX = 1;
    context.shadowOffsetY = 1;

    context.fillText('Game starts!', canvas.width / 2, canvas.height / 2);

    setInterval(updateCozmo , 100); // repeat every X ms

    setTimeout (function() {
        showInstruction();
    }, 3000);
}

function showInstruction() {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.height*2, canvas.width*2);

    context.font = '30pt Calibri';
    context.textAlign = 'center';
    context.fillStyle = 'white';
    context.shadowOffsetX = 1;
    context.shadowOffsetY = 1;

    context.fillText('1. Use the controller to pick up the cubes.', canvas.width / 2, canvas.height / 2 - 60);
    context.fillText('2. Use Cozmo to carry the cubes past the police.', canvas.width / 2, canvas.height / 2);
    context.fillText('3. Steal as many cubes as you can.', canvas.width / 2, canvas.height / 2 + 60);
}

function buttonDown() {
    var gp = navigator.getGamepads()[0];

    // super-big-button
    if (!tutoring)
    {
        gp.buttons
            .filter((button, index) => button.pressed && index === 1)
            .forEach(function (button, index) {
                // console.log ("tutoring");
                tutoring = true;
                tutorGame();
            });
    }
    else if (!starting)
    {
        gp.buttons
            .filter((button, index) => button.pressed && index === 17)
            .forEach(function (button, index) {
                // console.log ("starting");
                starting = true;
                startGame();
            });
    }
    else {
        // circle button pressed
        gp.buttons
            .filter((button, index) => button.pressed && index === 1)
            .forEach(function (button, index) {
                // console.log ("headDown");
                handleKeyActivityKeyCode(1, "keydown");
            });

        gp.buttons
            .filter((button, index) => !button.pressed && index === 1)
            .forEach(function (button, index) {
                // console.log ("headDown");
                handleKeyActivityKeyCode(1, "keyup");
            });

        // squre button pressed
        gp.buttons
            .filter((button, index) => button.pressed && index === 2)
            .forEach(function (button, index) {
                // console.log ("headDown");
                handleKeyActivityKeyCode(2, "keydown");
            });

        gp.buttons
            .filter((button, index) => !button.pressed && index === 2)
            .forEach(function (button, index) {
                // console.log ("headDown");
                handleKeyActivityKeyCode(2, "keyup");
            });

        // triangle button pressed
        gp.buttons
            .filter((button, index) => button.pressed && index === 3)
            .forEach(function (button, index) {
                // console.log ("up");
                handleKeyActivityKeyCode(3, "keydown");
            });

        // cross button pressed
        gp.buttons
            .filter((button, index) => button.pressed && index === 0)
            .forEach(function (button, index) {
                // console.log ("down");
                handleKeyActivityKeyCode(0, "keydown");
            });

        // forward button pressed
        gp.buttons
            .filter((button, index) => button.pressed && index === 12)
            .forEach(function (button, index) {
                // console.log ("forward");
                handleKeyActivityKeyCode(12, "keydown");
            });

        gp.buttons
            .filter((button, index) => !button.pressed && index === 12)
            .forEach(function (button, index) {
                // console.log ("forward");
                handleKeyActivityKeyCode(12, "keyup");
            });

        // back button pressed
        gp.buttons
            .filter((button, index) => button.pressed && index === 13)
            .forEach(function (button, index) {
                // console.log ("back");
                handleKeyActivityKeyCode(13, "keydown");
            });

        gp.buttons
            .filter((button, index) => !button.pressed && index === 13)
            .forEach(function (button, index) {
                // console.log ("back");
                handleKeyActivityKeyCode(13, "keyup");
            });

        // left button pressed
        gp.buttons
            .filter((button, index) => button.pressed && index === 14)
            .forEach(function (button, index) {
                // console.log ("left");
                handleKeyActivityKeyCode(14, "keydown");
            });

        gp.buttons
            .filter((button, index) => !button.pressed && index === 14)
            .forEach(function (button, index) {
                // console.log ("left");
                handleKeyActivityKeyCode(14, "keyup");
            });

        // right button pressed
        gp.buttons
            .filter((button, index) => button.pressed && index === 15)
            .forEach(function (button, index) {
                // console.log ("right");
                handleKeyActivityKeyCode(15, "keydown");
            });

        gp.buttons
            .filter((button, index) => !button.pressed && index === 15)
            .forEach(function (button, index) {
                // console.log ("right");
                handleKeyActivityKeyCode(15, "keyup");
            });
    }
}

function postHttpRequest(url, dataSet)
{
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.send( JSON.stringify( dataSet ) );

    // console.log("POST JSON : " + JSON.stringify( dataSet ));

    if (xhr.readyState === xhr.DONE) {
        if (xhr.status === 200) {
            // console.log(xhr.response);
            // console.log(xhr.responseText);
            return true;
        }
    }
}

function updateCozmo()
{
    postHttpRequest("updateCozmo", {} )
}

function handleKeyActivity (e, actionType)
{
    var keyCode  = (e.keyCode ? e.keyCode : e.which);
    var hasShift = (e.shiftKey ? 1 : 0)
    var hasCtrl  = (e.ctrlKey  ? 1 : 0)
    var hasAlt   = (e.altKey   ? 1 : 0)

    postHttpRequest(actionType, {keyCode, hasShift, hasCtrl, hasAlt})

    // console.log(actionType + " : " + keyCode);
}

function handleKeyActivityKeyCode (keyCode, actionType)
{
    var keyCode  = keyCode
    var hasShift = 0
    var hasCtrl  = 0
    var hasAlt   = 0

    // console.log(actionType + " : " + keyCode);

    return postHttpRequest(actionType, {keyCode, hasShift, hasCtrl, hasAlt})
}

$(document).ready(function() {

    if(canGame()) {

        var prompt = "To begin using your gamepad, connect it and press any button!";

        $("#gamepadPrompt").text(prompt);

        $(window).on("gamepadconnected", function() {
            hasGP = true;
            $("#gamepadPrompt").html("Gamepad connected!");
            // console.log("connection event");
            epGP = window.setInterval(buttonDown,100);
        });

        $(window).on("gamepaddisconnected", function() {
            // console.log("disconnection event");
            $("#gamepadPrompt").text(prompt);
            window.clearInterval(repGP);
        });

        //setup an interval for Chrome
        var checkGP = window.setInterval(function() {
            // console.log('checkGP');
            if(navigator.getGamepads()[0]) {
                if(!hasGP) $(window).trigger("gamepadconnected");
                window.clearInterval(checkGP);
            }
        }, 500);

        initGame();
    }

});

// document.addEventListener("keydown", function(e) { handleKeyActivity(e, "keydown") } );
