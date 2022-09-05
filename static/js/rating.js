var my_dict = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12
};

// function function1()
// {
//     $("#exampleFormControlSelect").change(function () {
//         const selectedSubject = $("#exampleFormControlSelect option:selected").val().split(' ');
//         const date = selectedSubject[2] + "-" + my_dict[selectedSubject[1]] + "-" + selectedSubject[0];
//
//         $.ajax({
//             url: '/statistic/' + date + '/',
//             success: function (data) {
//                 $(".rating").html(data.result);
//                 console.log(data.result);
//             },
//         })
//     });
// }
//
// function function2()
// {
//     $("#exampleFormControlSelect").change(function () {
//         const selectedSubject = $("#exampleFormControlSelect option:selected").val().split(' ');
//         const date = selectedSubject[2] + "-" + my_dict[selectedSubject[1]] + "-" + selectedSubject[0];
//
//         $.ajax({
//             url: '/meters_table/' + date + '/',
//             success: function (data) {
//                 $(".meters").html(data.result_2);
//                 console.log(data.result_2);
//             },
//         })
//     });
// }

window.onload = function () {
    $("#exampleFormControlSelect").change(function () {
        const selectedSubject = $("#exampleFormControlSelect option:selected").val().split(' ');
        const date = selectedSubject[2] + "-" + my_dict[selectedSubject[1]] + "-" + selectedSubject[0];

        $.ajax({
            url: '/statistic/' + date + '/',
            success: function (data) {
                $(".rating").html(data.result);
                console.log(data.result);
            },
        })
    });
};
// window.addEventListener("load", function2)
// window.addEventListener("load", function1)