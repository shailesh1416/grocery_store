var detailModal = $("#orderDetailsModal");


$(function () {
    //Json data by api call for order table
    $.get(orderListApiUrl, function (response) {
        if(response) {
            var table = '';
            var totalCost = 0;
            $.each(response, function(index, order) {
                totalCost += parseFloat(order.total);
                cancleBtn = ''
                switch (order.status) {
                    case 2:
                        orderStatus = '<span class="badge badge-danger p-2" style="width:100px">Canceled</span>'
                        break;
                    case 1:
                        orderStatus =  '<span class="badge badge-success p-2" style="width:100px">Done</span>'
                        break
                    default:
                        orderStatus =  '<span class="badge badge-primary p-2" style="width:100px">Pending</span>'
                        cancleBtn = '<span class="btn btn-sm btn-danger mx-2 order-cancle">Cancle</span>'
                        break;
                }
                table += '<tr data-id="'+ order.order_id+'">' +
                    '<td>'+ order.datetime +'</td>'+
                    '<td>'+ order.order_id +'</td>'+
                    '<td>'+ order.customer_name +'</td>'+
                    '<td>'+ order.total.toFixed(2) +' Rs</td>'+
                    '<td><span class="btn btn-sm btn-warning mx-2 order-details" data-toggle="modal" data-target="#orderDetailsModal">Details</span>'+
                    cancleBtn+'</td>'+
                    '<td class="d-flex justify-content-center">'+orderStatus+'</td></tr>';
            });
            table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>'+ totalCost.toFixed(2) +' Rs</b></td></tr>';
            $("table").find('tbody').empty().html(table);
        }
    });
});

// getting order details
var orderId
$(document).on("click", ".order-details", function (event){
    var tr = $(this).closest('tr');
        var data = {
            order_id : tr.data('id')
        };
        orderId = data
    
});



detailModal.on('show.bs.modal', function(){
    //JSON data by API call
    $.get(orderDetailApiUrl, orderId,function (response) {
        if(response) {
            
            var options = "";
                $.each(response, function(index, order) {
                    options += '<tr>'+
                                '<td >'+ order.product_name +'</td>'+ 
                                '<td >'+ order.quantity +'</td>'+ 
                                '<td >'+ order.total_price +'</td></tr>';
                });

                $("#order_detail_table").empty().html(options);
               

                
        }
    });
});


// cancle order

$(document).on("click", ".order-cancle", function (){
    var tr = $(this).closest('tr');
    var data = {
        order_id : tr.data('id')
    };
    var isCancle = confirm("Are you sure to cancle order no :"+ tr.data('id') );
    if (isCancle) {
        callApi("POST", orderCancleApiUrl, data);
    }
});

$(document).on("click", "#order-done", function (){
    callApi("POST", orderDoneApiUrl, orderId);
});