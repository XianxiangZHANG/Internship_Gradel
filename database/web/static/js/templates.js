$(document).ready(function() {
    $('#filterForm').on('submit', function() {
        $('#loading').show(); 
        $('#tableContainer').hide(); 
    });

    $('#resetButton').on('click', function() {
        window.location.href = window.location.pathname;
    });
});
