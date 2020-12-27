$(document).ready(function()

    {
	var zz = 0; //Initial field counter
	var list_maxField_api = 10; //Input fields increment limitation
	
        //Once add button is clicked
	$('.list_add_button_api').click(function()
	    {
	    //Check maximum number of input fields
	    if(zz < list_maxField_api){ 
	        zz++; //Increment field counter
	        var list_fieldHTML_api = '<div style="border: thin solid black"><div class="row"><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">End Point URL:<input name="apiurl['+zz+'][]" type="text" placeholder="https://hostname:portnumber" class="form-control"/></div></div><div class="col-xs-2 col-sm-2 col-md-2"><div class="form-group">Choose a API Type:<select name="apitype['+zz+'][]" id="db" class="form-control"><option value="">..</option><option value="GET">GET</option><option value="POST">POST</option><option value="POST">PUT</option></select></div></div><div class="col-xs-3 col-sm-3 col-md-3"><div class="form-group">API Params Array:<input name="apiparams['+zz+'][]" type="text" placeholder="[{key: null, value: null}]" class="form-control"/></div></div><div class="col-xs-4 col-sm-4 col-md-4"><div class="form-group">Output Tag<input name="apiouttag['+zz+'][]" type="text" placeholder="[{map:{name:null,path:[],outputFormat:null,outputTag:null}}]" class="form-control"/></div></div><div class="col-xs-1 col-sm-7 col-md-1"><a href="javascript:void(0);" class="list_remove_button_api btn btn-danger">Remove API</a></div></div></div>'; //New input field html 
	        $('.list_wrapper_api').append(list_fieldHTML_api); //Add field html
	    }
        });
    
        //Once remove button is clicked
        $('.list_wrapper_api').on('click', '.list_remove_button_api', function()
        {
           $(this).closest('div.row').remove(); //Remove field html
           zz--; //Decrement field counter
        });
});