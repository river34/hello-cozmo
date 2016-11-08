var hasGP = false;
var repGP;
var celebrating = true;
var picking = true;
var placing = true;
var able_to_place = true;
var helloing = false;
var tutoring = false;
var starting = false;
var cozmo_in = false;
var cozmo_tutorial = false;
var music = false;

function canGame() {
    return "getGamepads" in navigator;
}

function initGame() {
    if (helloing || tutoring || starting){
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

function helloGame() {
    if (tutoring || starting){
        return;
    }

    if (!helloing) {
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

    var text = 'Welcome ...';
    var cozmo_image = document.getElementById("cozmo_image");
    var speed = 10;
    cozmo_in = new CozmoIn(canvas, text, cozmo_image, speed, 20);
    setTimeout (function() {
        //
    }, 3000);
}

function tutorGame() {
    if (!tutoring)
    {
        return;
    }

    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.height, canvas.width);

    context.font = '30pt Calibri';
    context.textAlign = 'center';
    context.fillStyle = 'white';
    context.shadowColor = "black";
    context.shadowOffsetX = 1;
    context.shadowOffsetY = 1;

    var text = 'Cozmo needs power.';
    var text_2 = 'Tap the blinking cube to charge them up!';
    var cozmo_image = document.getElementById("cozmo_image");
    var cube_image = document.getElementById("cube_image_1");
    var mark_image = document.getElementById("cube_image_2");
    var speed = 10;
    cozmo_tutorial = new CozmoTutorial(canvas, text, text_2, cozmo_image, cube_image, mark_image, speed, 20);
    music = document.getElementById("background_music");
    music.play();
}

function CozmoIn(canvas, text, cozmo_image, speed, period)
{
    this.canvas = canvas;
    this.text = text;
    this.cozmo_image = cozmo_image;
    this.speed = speed;
    this.cozmo_pos = 0;
    this.period = period;
    var self = this; // This is to pass the reference into setInterval
    this.interval = setInterval(function() { self.doMove(); }, this.period);
    this.doMove = function()
    {
        if (this.cozmo_pos < 400){
            this.cozmo_pos += this.speed;
            var context = this.canvas.getContext("2d");
            context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            context.shadowOffsetX = 0;
            context.shadowOffsetY = 0;
            context.drawImage(this.cozmo_image, canvas.width / 2 - cozmo_image.width + this.cozmo_pos, canvas.height / 2 - cozmo_image.height / 2 + 50);
            context.shadowOffsetX = 1;
            context.shadowOffsetY = 1;
            context.fillText(this.text, canvas.width / 2, canvas.height / 2);
        }
        else if (this.cozmo_pos < 600){
            this.cozmo_pos += this.speed/3;
            var context = this.canvas.getContext("2d");
            context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            context.shadowOffsetX = 0;
            context.shadowOffsetY = 0;
            context.drawImage(this.cozmo_image, canvas.width / 2 - cozmo_image.width + this.cozmo_pos, canvas.height / 2 - cozmo_image.height / 2 + 50);
            context.shadowOffsetX = 1;
            context.shadowOffsetY = 1;
            context.fillText(this.text, canvas.width / 2, canvas.height / 2);
        }
        else if (this.cozmo_pos < 1000){
            this.cozmo_pos += this.speed;
            var context = this.canvas.getContext("2d");
            context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            context.shadowOffsetX = 0;
            context.shadowOffsetY = 0;
            context.drawImage(this.cozmo_image, canvas.width / 2 - cozmo_image.width + this.cozmo_pos, canvas.height / 2 - cozmo_image.height / 2 + 50);
            context.shadowOffsetX = 1;
            context.shadowOffsetY = 1;
            context.fillText(this.text, canvas.width / 2, canvas.height / 2);
        }
        else {
            clearInterval(this.interval);
            tutoring = true;
            tutorGame();
        }
    };
}

function CozmoTutorial(canvas, text, text_2, cozmo_image, cube_image, mark_image, speed, period)
{
    this.canvas = canvas;
    this.text = text;
    this.text_2 = text_2;
    this.cozmo_image = cozmo_image;
    this.cube_image = cube_image;
    this.mark_image = mark_image;
    this.speed = speed;
    this.cozmo_pos = 0;
    this.cube_pos = 720;
    this.period = period;
    var self = this; // This is to pass the reference into setInterval
    this.interval = setInterval(function() { self.doMove(); }, this.period);
    this.interval_index = 0;
    this.doMove = function()
    {
        if (this.cozmo_pos < 400){
            this.cozmo_pos += this.speed;
            var context = this.canvas.getContext("2d");
            context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            context.shadowOffsetX = 0;
            context.shadowOffsetY = 0;
            context.drawImage(this.cozmo_image, canvas.width / 2 - cozmo_image.width + this.cozmo_pos, canvas.height / 2 - cozmo_image.height / 2 + 50);
            context.shadowOffsetX = 1;
            context.shadowOffsetY = 1;
            context.fillText(this.text, canvas.width / 2, canvas.height / 2 - 120);
        }
        else {
            self.doMoveCube();
        }
    };
    this.doMoveCube = function()
    {
        if (this.cube_pos > 320){
            this.cube_pos -= this.speed;
            var context = this.canvas.getContext("2d");
            context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            context.shadowOffsetX = 0;
            context.shadowOffsetY = 0;
            context.drawImage(this.cozmo_image, canvas.width / 2 - cozmo_image.width + this.cozmo_pos, canvas.height / 2 - cozmo_image.height / 2 + 50);
            context.drawImage(this.cube_image, canvas.width / 2 - cube_image.width + this.cube_pos, canvas.height / 2 - cube_image.height / 2 + 50);
            context.shadowOffsetX = 1;
            context.shadowOffsetY = 1;
            context.fillText(this.text, canvas.width / 2, canvas.height / 2 - 120);
        }
        else {
            self.doBlink();
        }
    };
    this.markVisible = true;
    this.doBlink = function()
    {
        var context = this.canvas.getContext("2d");
        if(this.markVisible)
        {
            context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            context.shadowOffsetX = 0;
            context.shadowOffsetY = 0;
            context.drawImage(this.cozmo_image, canvas.width / 2 - cozmo_image.width + this.cozmo_pos, canvas.height / 2 - cozmo_image.height / 2 + 50);
            context.drawImage(this.cube_image, canvas.width / 2 - cube_image.width + this.cube_pos, canvas.height / 2 - cube_image.height / 2 + 50);
            context.shadowOffsetX = 1;
            context.shadowOffsetY = 1;
            context.fillText(this.text, canvas.width / 2, canvas.height / 2 - 120);
            context.fillText(this.text_2, canvas.width / 2, canvas.height / 2 - 60);
            this.interval_index ++;
            if (this.interval_index > 25){
                this.markVisible = false;
                this.interval_index = 0;
            }
        }
        else
        {
            this.drawMark();
        }
    }
    this.drawMark = function()
    {
        var context = this.canvas.getContext("2d");
        context.shadowOffsetX = 0;
        context.shadowOffsetY = 0;
        context.drawImage(this.mark_image, canvas.width / 2 - cube_image.width + this.cube_pos, canvas.height / 2 - cube_image.height / 2 + 50);

        this.interval_index ++;
        if (this.interval_index > 25){
            this.markVisible = true;
            this.interval_index = 0;
        }
    };
}

function startGame() {
    if (!starting)
    {
        return;
    }

    clearInterval(cozmo_in.interval);
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
}

function buttonDown() {
    var gp = navigator.getGamepads()[0];

    if (!helloing)
    {
        gp.buttons
            .filter((button, index) => button.pressed && index === 1)
            .forEach(function (button, index) {
                // console.log ("starting");
                helloing = true;
                helloGame();
            });
    }
    // super-big-button
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
