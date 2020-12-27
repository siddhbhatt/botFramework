$(document).ready(function()

    {
	var yy = 0; //Initial field counter
	var list_maxField_nextvar = 100; //Input fields increment limitation
	
        //Once add button is clicked
	$('.list_add_button_nextvar').click(function()
	    {
	    //Check maximum number of input fields
	    if(yy < list_maxField_nextvar){ 
	        yy++; //Increment field counter
	        var list_fieldHTML_nextvar = '<div style="border: thin solid black"><div class="row"><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Journey Name<input name="njourneyName['+yy+'][]" type="text" placeholder="Next Journey Name" class="form-control"/></div></div><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Block Name<input name="nblockName['+yy+'][]" type="text" placeholder="Next Block Name" class="form-control"/></div></div><div class="col-xs-1 col-sm-7 col-md-1"><a href="javascript:void(0);" class="list_remove_button_nextvar btn btn-danger">Remove Set Variable</a></div></div></div>'; //New input field html 
	        $('.list_wrapper_nextvar').append(list_fieldHTML_nextvar); //Add field html
	    }
        });
    
        //Once remove button is clicked
        $('.list_wrapper_nextvar').on('click', '.list_remove_button_nextvar', function()
        {
           $(this).closest('div.row').remove(); //Remove field html
           yy--; //Decrement field counter
        });
});