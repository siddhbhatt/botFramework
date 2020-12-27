$(document).ready(function()

    {
	var yy = 0; //Initial field counter
	var list_maxField_input = 10; //Input fields increment limitation
	
        //Once add button is clicked
	$('.list_add_button_input').click(function()
	    {
	    //Check maximum number of input fields
	    if(yy < list_maxField_input){ 
	        yy++; //Increment field counter
	        var list_fieldHTML_input = '<div style="border: thin solid black"><div class="row"><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Input Data<input name="imdata['+yy+'][]" type="text" placeholder="Input Data Function" class="form-control"/></div></div><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Input Channel<input name="imchannel['+yy+'][]" type="text" placeholder="Input Channel" class="form-control"/></div></div><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Input User<input name="imuser['+yy+'][]" type="text" placeholder="User Name" class="form-control"/></div></div><div class="col-xs-1 col-sm-7 col-md-1"><a href="javascript:void(0);" class="list_remove_button_input btn btn-danger">Remove Input</a></div></div></div>'; //New input field html 
	        $('.list_wrapper_input').append(list_fieldHTML_input); //Add field html
	    }
        });
    
        //Once remove button is clicked
        $('.list_wrapper_input').on('click', '.list_remove_button_input', function()
        {
           $(this).closest('div.row').remove(); //Remove field html
           yy--; //Decrement field counter
        });
});