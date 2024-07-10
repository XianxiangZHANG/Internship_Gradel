var mybutton = document.getElementById("topBtn");

window.onscroll = function() {
    scrollFunction();
};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}


function topFunction() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}


function goBack() {
    window.history.back();
}
document.addEventListener("DOMContentLoaded", function() {
    var filterForm = document.getElementById("filterForm");
    if (filterForm) {
        filterForm.addEventListener("submit", function() {
            document.getElementById("loading").style.display = "block";
            document.getElementById("NoMessage").style.display = "none";
            document.getElementById('normalTable').style.display = 'none';
        });
    }

    var resetButton = document.getElementById("resetButton");
    if (resetButton) {
        resetButton.addEventListener("click", function() {
            window.location.href = window.location.pathname;
        });
    }
});
// document.getElementById("filterForm").addEventListener("submit", function() {
//     document.getElementById("loading").style.display = "block";
//     document.getElementById("NoMessage").style.display = "none";
//     document.getElementById('normalTable').style.display = 'none';
// });


// document.getElementById("resetButton").addEventListener("click", function() {
//     window.location.href = window.location.pathname;
// });