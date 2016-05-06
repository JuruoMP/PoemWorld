/**
 * Created by LiYuntao on 2016/3/27.
 */

function searchUrl() {
    var condition = $("#inputCondition").val();
    self.location = "/map/search/condition=" + condition;
}

function filterNode() {
    var size = $("#filterSize").val();
    size = parseInt(size);
    /*
    if(size < 6 || size > 24) {
        alert("请输入6-24之间的整数值");
        //return false;
    } else {
        refresh(size);
    }
    */
    refresh(size)
}
