function createAList(itemList){
    // $("#all_pages").html("");
    var ul = document.createElement('ul');
    ul.setAttribute('id','ol_item_list');
    ul.setAttribute('class','list-group')
    // itemList = ['a','b','c','d']
    itemList.forEach(renderItemList);
    function renderItemList(element, index) {
        var li = document.createElement('li');
        li.setAttribute('class','item');
        li.setAttribute('class','list-group-item')
        var args=element.split(" ").slice(1);
        // $(li).data("item_id",element)
        $(li).data("item_id",args)
        ul.appendChild(li);
        li.innerHTML=li.innerHTML + '<a href="#">'+element+'</a>';
    }
    return ul;
    console.log(ul)
}


function setHtml(id,html){
$("#"+id).html(html);
}