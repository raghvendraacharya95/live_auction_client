$(document).on('click','ul#ol_item_list li',function(){
	var item_id = $(this).data("item_id");
	window.open('/auction_room/'+item_id)	

});

// function init_socket(item_id){
// 	console.log("in init_socket")
//   str_item_id = item_id
//   var my_room='ROOM-AUCTION-ITEM='+str_item_id;
//   var namespace="/sink_auction";
//   console.log(my_room)
//   mysocket = io.connect('http://127.0.0.1:8082'+namespace);
//   mysocket.on('connect', function(res) {
//         console.log("in connect")
//         console.log(my_room)
//         // console.log("i am connected!!!!")                                    
//         mysocket.emit('join', {room:my_room});                    

//   });
//   mysocket.io.timeout(1000);
  
// //  console.log(mysocket);
//   mysocket.on('message', function(res) {
//         console.log("in message")
//         // console.log(my_room)
//         console.log("I am here")    
//         console.log(res);
//         // mysocket.emit('my_event', {data: 'I\'m connected1!'}); 
//         mysocket.send('my_event', {data: 'I\'m connected1! and sending message'});
//   });
// }

// $(document).ready(function(){
// 	setTimeout(function(){ init_socket(item_id);
// 	},10)
// });