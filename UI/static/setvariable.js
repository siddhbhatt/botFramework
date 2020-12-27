$(document).ready(function()

    {
	var yy = 0; //Initial field counter
	var list_maxField_setvariable = 100; //Input fields increment limitation
	
        //Once add button is clicked
	$('.list_add_button_setvariable').click(function()
	    {
	    //Check maximum number of input fields
	    if(yy < list_maxField_setvariable){ 
	        yy++; //Increment field counter
	        var list_fieldHTML_setvariable = '<div style="border: thin solid black"><div class="row"><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Variable Name<input name="svariableName['+yy+'][]" type="text" placeholder="Set Varaible Name" class="form-control"/></div></div><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Value<input name="svalue['+yy+'][]" type="text" placeholder="Set Value for Variable" class="form-control"/></div></div><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Scope<input name="sscope['+yy+'][]" type="text" placeholder="Set Scope of Variable" class="form-control"/></div></div><div class="col-xs-1 col-sm-7 col-md-1"><a href="javascript:void(0);" class="list_remove_button_setvariable btn btn-danger">Remove Set Variable</a></div></div></div>'; //New input field html 
	        $('.list_wrapper_setvariable').append(list_fieldHTML_setvariable); //Add field html
	    }
        });
    
        //Once remove button is clicked
        $('.list_wrapper_setvariable').on('click', '.list_remove_button_setvariable', function()
        {
           $(this).closest('div.row').remove(); //Remove field html
           yy--; //Decrement field counter
        });
});