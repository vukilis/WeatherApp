window.setTimeout(function() {
    $(".alert").fadeTo(500, 0) 
}, 3000);
// ####################################TIMER##################################################
function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
        if (timer == 0){
            location.reload();
        }
    }, 1000);
}

window.onload = function () {
    var fiveMinutes = 60 * 5,
        display = document.querySelector('#time');
    startTimer(fiveMinutes, display);
};
// ####################################day and night##################################################
var now = new Date();
if (now.getHours() > 6 && now.getHours() < 20) {
    document.body.className += " day";
} else {
    document.body.className += " night";
}