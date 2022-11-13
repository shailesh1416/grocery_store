var productModal = $("#productModal");
var productEditModal = $("#editModal");

    $(function () {

        //JSON data by API call
        $.get(productListApiUrl, function (response) {
            if(response) {
                var table = '';
                $.each(response, function(index, product) {
                    table += '<tr data-id="'+ product.product_id +'" data-name="'+ product.name +'" data-unit="'+ product.uom_id +'" data-price="'+ product.price_per_unit +'">' +
                        '<td>'+ product.name +'</td>'+
                        '<td>'+ product.uom_name +'</td>'+
                        '<td>'+ product.rate +'</td>'+
                        '<td><span class="btn btn-xs btn-danger delete-product">Delete</span>'+
                        '<span class="btn btn-xs btn-warning mx-2 edit-product" data-toggle="modal" data-target="#editModal">Edit</span></td></tr>';
                });
                $("table").find('tbody').empty().html(table);
            }
        });
    });


    
    // Save Product
    $("#saveProduct").on("click", function () {
        // If we found id value in form then update product detail
        var data = $("#productForm").serializeArray();
        var requestPayload = {
            product_name: null,
            uom_id: null,
            price_per_unit: null
        };
        for (var i=0;i<data.length;++i) {
            var element = data[i];
            switch(element.name) {
                case 'name':
                    requestPayload.product_name = element.value;
                    break;
                case 'uoms':
                    requestPayload.uom_id = element.value;
                    break;
                case 'price':
                    requestPayload.rate = element.value;
                    break;
            }
        }
        callApi("POST", productSaveApiUrl, {
            'data': JSON.stringify(requestPayload)
        });
    });


    // Edit Product
    $("#editProduct").on("click", function () {
        // If we found id value in form then update product detail
        var data = $("#editProductForm").serializeArray();
        var requestPayload = {
            id:null,
            product_name: null,
            uom_id: null,
            price_per_unit: null
        };
        for (var i=0;i<data.length;++i) {
            var element = data[i];
            switch(element.name) {
                case 'id':
                    requestPayload.id = element.value;
                    break;
                case 'name':
                    requestPayload.product_name = element.value;
                    break;
                case 'uoms':
                    requestPayload.uom_id = element.value;
                    break;
                case 'price':
                    requestPayload.rate = element.value;
                    break;
            }
        }
        callApi("POST", productEditApiUrl, {
            'data': JSON.stringify(requestPayload)
        });
        $('#editModal').modal('hide');
        // alert(`Product edited Successfully`)
    });

    $(document).on("click", ".delete-product", function (){
        var tr = $(this).closest('tr');
        var data = {
            product_id : tr.data('id')
        };
        var isDelete = confirm("Are you sure to delete "+ tr.data('name') +" item?");
        if (isDelete) {
            callApi("POST", productDeleteApiUrl, data);
        }
    });

    productModal.on('hide.bs.modal', function(){
        $("#id").val('0');
        $("#name, #unit, #price").val('');
        productModal.find('.modal-title').text('Add New Product');
    });

    productModal.on('show.bs.modal', function(){
        //JSON data by API call
        $.get(uomListApiUrl, function (response) {
            if(response) {
                var options = '<option value="">--Select--</option>';
                $.each(response, function(index, uom) {
                    options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
                });
                $("#uoms").empty().html(options);
            }
        });
    });

    // uom in editmodel
    var uom_data
    var uom_ID 
    $(document).on("click", ".edit-product", function (){
        var tr = $(this).closest('tr');
        var data = {
            product_id : tr.data('id')
        };
        uom_data=data
    });

    productEditModal.on('show.bs.modal', function(){
        //JSON data by API call
        $.get(productGetApiUrl,uom_data,function (response) {  
            console.log(response['data'])
            $('#editProductId').val(response['data'].id)
            $('#editProductName').val(response['data'].name)
            uom_ID = response['data'].uom_name
            $('#editProductRate').val(response['data'].rate)
        })
        $.get(uomListApiUrl,function (response) {
            if(response) {
                var options = '<option value="">--Select--</option>';
                $.each(response, function(index, uom) {
                    if(uom.uom_id==uom_ID){
                        options += '<option value="'+ uom.uom_id +'"selected>'+ uom.uom_name +'</option>';
                    }else{
                        options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
                    }
                });
                $("#editProductUom").empty().html(options);
            }
        });
    });