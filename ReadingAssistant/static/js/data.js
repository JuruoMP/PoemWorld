/**
 * Created by LiYuntao on 2016/3/27.
 */
///*
//$(document).ready(function() {
//    $("#searchBtn").click(function() {
//        search();
//    })
//});
//*/
//function search() {
//    var condition = $("#inputCondition").val();
//    console.log(condition);
//    $.ajax({
//        type: "GET",
//        /*
//        data: {
//            'csrfmiddlewaretoken': '{{csrf_token}}'
//        },
//        */
//        url: "search/",
//        data: "condition=" + condition,
//        cache: false,
//        success: function(result) {
//            //json = eval(result);
//            $("#inputCondition").html = result;
//        }
//    })
//}
//
//$(document).ready(function(){
//    $("#searchBtn").click(function(){
//        var condition = $("#inputCondition").val();
//
//        $.get("/search/",{'condition': condition}, function(ret){
//            $('#inputCondition').html(ret)
//        })
//    });
//});

function searchUrl() {
    var condition = $("#inputCondition").val();
    window.location.replace("map/search/condition=" + condition);
}

function generateUrl() {
    window.location.replace("/generatepoem/");
}
