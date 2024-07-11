$(document).ready(function() {
    $('#filterForm').on('submit', function() {
        $('#loading').show();  // 显示加载动画
        $('#tableContainer').hide();  // 隐藏表格
    });

    $('#resetButton').on('click', function() {
        window.location.href = window.location.pathname;  // 重置表单
    });
});
