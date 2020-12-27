$(document).ready(function()

    {
	var yy = 0; //Initial field counter
	var list_maxField_rule = 100; //Input fields increment limitation
	
        //Once add button is clicked
	$('.list_add_button_rule').click(function()
	    {
	    //Check maximum number of input fields
	    if(yy < list_maxField_rule){ 
	        yy++; //Increment field counter
	        var list_fieldHTML_rule = '<div style="border: thin solid black"><div class="row"><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">Rule<input name="rule['+yy+'][]" type="text" placeholder="Add Rules" class="form-control"/></div></div><div class="col-xs-1 col-sm-7 col-md-1"><a href="javascript:void(0);" class="list_remove_button_rule btn btn-danger">Remove Rule</a></div></div></div>'; //New input field html 
	        $('.list_wrapper_rule').append(list_fieldHTML_rule); //Add field html
	    }
        });
    
        //Once remove button is clicked
        $('.list_wrapper_rule').on('click', '.list_remove_button_rule', function()
        {
           $(this).closest('div.row').remove(); //Remove field html
           yy--; //Decrement field counter
        });
});