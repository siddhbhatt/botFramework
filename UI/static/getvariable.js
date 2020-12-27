$(document).ready(function()

    {
	var yy = 0; //Initial field counter
	var list_maxField_getvar = 10; //Input fields increment limitation
	
        //Once add button is clicked
	$('.list_add_button_getvariable').click(function()
	    {
	    //Check maximum number of input fields
	    if(yy < list_maxField_getvar){ 
	        yy++; //Increment field counter
	        var list_fieldHTML_getvar = '<div style="border: thin solid black"><div class="row"><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Variable Name<input name="variableName['+yy+'][]" type="text" placeholder="Varaible Name" class="form-control"/></div></div><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Value<input name="value['+yy+'][]" type="text" placeholder="Value for Variable" class="form-control"/></div></div><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Scope<input name="scope['+yy+'][]" type="text" placeholder="Scope of Variable" class="form-control"/></div></div><div class="col-xs-1 col-sm-7 col-md-1"><a href="javascript:void(0);" class="list_remove_button_getvariable btn btn-danger">Remove Get Variable</a></div></div></div>'; //New input field html 
	        $('.list_wrapper_getvariable').append(list_fieldHTML_getvar); //Add field html
	    }
        });
    
        //Once remove button is clicked
        $('.list_wrapper_getvariable').on('click', '.list_remove_button_getvariable', function()
        {
           $(this).closest('div.row').remove(); //Remove field html
           yy--; //Decrement field counter
        });
});